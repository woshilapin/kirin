# coding=utf-8

# Copyright (c) 2001-2014, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# [matrix] channel #navitia:matrix.org (https://app.element.io/#/room/#navitia:matrix.org)
# https://groups.google.com/d/forum/navitia
# www.navitia.io

from __future__ import absolute_import, print_function, unicode_literals, division
import logging
from datetime import datetime

import requests
import six

from kirin.core import model
from kirin.core.abstract_builder import wrap_build
from kirin.core.types import ConnectorType
from kirin.cots.model_maker import as_duration

from kirin.tasks import celery
from kirin.utils import (
    should_retry_exception,
    make_kirin_lock_name,
    get_lock,
    manage_db_error,
    manage_db_no_new,
    build_redis_etag_key,
    record_input_retrieval,
    make_kirin_last_call_dt_name,
)
from kirin.gtfs_rt import KirinModelBuilder
from retrying import retry
from kirin import app, redis_client
from kirin import new_relic


TASK_STOP_MAX_DELAY = app.config[str("TASK_STOP_MAX_DELAY")]
TASK_WAIT_FIXED = app.config[str("TASK_WAIT_FIXED")]


class InvalidFeed(Exception):
    pass


def _is_newer(config):
    logger = logging.LoggerAdapter(logging.getLogger(__name__), extra={"contributor": config["contributor"]})
    contributor = config["contributor"]
    try:
        head = requests.head(config["feed_url"], timeout=config.get("timeout", 1))

        new_etag = head.headers.get("ETag")
        if not new_etag:
            return True  # unable to get a ETag, we continue the polling

        etag_key = build_redis_etag_key(contributor)
        old_etag = redis_client.get(etag_key)

        if new_etag == old_etag:
            logger.info("get the same ETag of %s, skipping the polling for %s", etag_key, contributor)
            return False

        redis_client.set(etag_key, new_etag)

    except Exception as e:
        logger.debug(
            "exception occurred when checking the newer version of gtfs for %s: %s",
            contributor,
            six.text_type(e),
        )
    return True  # whatever the exception is, we don't want to break the polling


def _is_last_call_too_recent(func_name, contributor, minimal_call_interval):
    # retrieve last_call_datetime from redis
    str_dt_format = "%Y-%m-%d %H:%M:%S.%f"

    last_exe_dt_name = make_kirin_last_call_dt_name(func_name, contributor)
    last_exe_dt_str = redis_client.get(last_exe_dt_name)
    last_exe_dt = datetime.strptime(last_exe_dt_str, str_dt_format) if last_exe_dt_str else None
    now = datetime.utcnow()

    if last_exe_dt and now <= last_exe_dt + as_duration(minimal_call_interval):
        return True

    # store last_call_datetime in redis
    # to avoid storing things forever in redis: set an expiration duration of (interval + "security" margin)
    redis_client.set(last_exe_dt_name, now.strftime(str_dt_format), ex=minimal_call_interval + 10)
    return False


@new_relic.agent.function_trace()  # trace it specifically in transaction times
def _retrieve_gtfsrt(config):
    start_dt = datetime.utcnow()
    resp = requests.get(config["feed_url"], timeout=config.get("timeout", 1))
    duration_ms = (datetime.utcnow() - start_dt).total_seconds() * 1000
    record_input_retrieval(contributor=config["contributor"], duration_ms=duration_ms)
    return resp


@celery.task(bind=True)  # type: ignore
@retry(stop_max_delay=TASK_STOP_MAX_DELAY, wait_fixed=TASK_WAIT_FIXED, retry_on_exception=should_retry_exception)
def gtfs_poller(self, config):
    func_name = "gtfs_poller"
    contributor = (
        model.Contributor.query_existing()
        .filter_by(id=config.get("contributor"), connector_type=ConnectorType.gtfs_rt.value)
        .first()
    )

    logger = logging.LoggerAdapter(logging.getLogger(__name__), extra={"contributor": contributor.id})

    lock_name = make_kirin_lock_name(func_name, contributor.id)
    with get_lock(logger, lock_name, app.config[str("REDIS_LOCK_TIMEOUT_POLLER")]) as locked:
        if not locked or not config.get("feed_url"):
            new_relic.ignore_transaction()
            return

        retrieval_interval = config.get("retrieval_interval", 10)
        if _is_last_call_too_recent(func_name, contributor.id, retrieval_interval):
            # do nothing if the last call is too recent
            new_relic.ignore_transaction()
            return

        logger.debug("polling of %s", config.get("feed_url"))

        # We do a HEAD request at the very beginning of polling and we compare it with the previous one to check if
        # the gtfs-rt is changed.
        # If the HEAD request or Redis get/set fail, we just ignore this part and do the polling anyway
        if not _is_newer(config):
            new_relic.ignore_transaction()
            manage_db_no_new(connector="gtfs-rt", contributor=contributor.id)
            return

        try:
            response = _retrieve_gtfsrt(config)
            response.raise_for_status()
        except Exception as e:
            manage_db_error(
                data="",
                connector="gtfs-rt",
                contributor=contributor.id,
                error="Http Error",
                is_reprocess_same_data_allowed=True,
            )
            logger.debug(six.text_type(e))
            return

        wrap_build(KirinModelBuilder(contributor), response.content)
        logger.info("%s for %s is finished", func_name, contributor.id)
