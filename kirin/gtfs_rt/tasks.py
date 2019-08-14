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
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io

from __future__ import absolute_import, print_function, unicode_literals, division
import logging
import requests
import six

from kirin import gtfs_realtime_pb2

from kirin.tasks import celery
from kirin.utils import should_retry_exception, make_kirin_lock_name, get_lock, manage_db_error, manage_db_no_new
from kirin.gtfs_rt import model_maker
from retrying import retry
from kirin import app, redis
from kirin import new_relic
from google.protobuf.message import DecodeError
import navitia_wrapper


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

        etag_key = "|".join([contributor, "polling_HEAD"])
        old_etag = redis.get(etag_key)

        if new_etag == old_etag:
            logger.info("get the same ETag of %s, skipping the polling for %s", etag_key, contributor)
            return False

        redis.set(etag_key, new_etag)

    except Exception as e:
        logger.debug(
            "exception occurred when checking the newer version of gtfs for %s: %s",
            contributor,
            six.text_type(e),
        )
    return True  # whatever the exception is, we don't want to break the polling


@celery.task(bind=True)  # type: ignore
@retry(stop_max_delay=TASK_STOP_MAX_DELAY, wait_fixed=TASK_WAIT_FIXED, retry_on_exception=should_retry_exception)
def gtfs_poller(self, config):
    func_name = "gtfs_poller"
    logger = logging.LoggerAdapter(logging.getLogger(__name__), extra={"contributor": config["contributor"]})
    logger.debug("polling of %s", config["feed_url"])

    contributor = config["contributor"]
    lock_name = make_kirin_lock_name(func_name, contributor)
    with get_lock(logger, lock_name, app.config[str("REDIS_LOCK_TIMEOUT_POLLER")]) as locked:
        if not locked:
            new_relic.ignore_transaction()
            return

        # We do a HEAD request at the very beginning of polling and we compare it with the previous one to check if
        # the gtfs-rt is changed.
        # If the HEAD request or Redis get/set fail, we just ignore this part and do the polling anyway
        if not _is_newer(config):
            new_relic.ignore_transaction()
            manage_db_no_new(connector="gtfs-rt", contributor=contributor)
            return

        try:
            response = requests.get(config["feed_url"], timeout=config.get("timeout", 1))
            response.raise_for_status()

        except Exception as e:
            manage_db_error(
                data="", connector="gtfs-rt", contributor=contributor, status="KO", error="Http Error"
            )
            logger.debug(six.text_type(e))
            return

        nav = navitia_wrapper.Navitia(
            url=config["navitia_url"],
            token=config["token"],
            timeout=5,
            cache=redis,
            query_timeout=app.config.get(str("NAVITIA_QUERY_CACHE_TIMEOUT"), 600),
            pubdate_timeout=app.config.get(str("NAVITIA_PUBDATE_CACHE_TIMEOUT"), 600),
        ).instance(config["coverage"])

        proto = gtfs_realtime_pb2.FeedMessage()
        try:
            proto.ParseFromString(response.content)
        except DecodeError:
            manage_db_error(proto, "gtfs-rt", contributor=contributor, status="KO", error="Decode Error")
            logger.debug("invalid protobuf")
        else:
            model_maker.handle(proto, nav, contributor)
            logger.info("%s for %s is finished", func_name, contributor)
