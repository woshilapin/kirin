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

import logging
import requests
from kirin import gtfs_realtime_pb2
import navitia_wrapper
from kirin.tasks import celery
from kirin.utils import should_retry_exception, make_kirin_lock_name, get_lock
from kirin.gtfs_rt import model_maker
from retrying import retry
from kirin import app

TASK_STOP_MAX_DELAY = app.config['TASK_STOP_MAX_DELAY']
TASK_WAIT_FIXED = app.config['TASK_WAIT_FIXED']


class InvalidFeed(Exception):
    pass


@celery.task(bind=True)
@retry(stop_max_delay=TASK_STOP_MAX_DELAY,
       wait_fixed=TASK_WAIT_FIXED,
       retry_on_exception=should_retry_exception)
def gtfs_poller(self, config):
    func_name = 'gtfs_poller'
    logger = logging.LoggerAdapter(logging.getLogger(__name__), extra={'contributor': config['contributor']})
    logger.debug('polling of %s', config['feed_url'])

    contributor = config['contributor']
    lock_name = make_kirin_lock_name(func_name, contributor)
    with get_lock(logger, lock_name, app.config['REDIS_LOCK_TIMEOUT_POLLER']) as locked:
        if not locked:
            logger.warning('%s for %s is already in progress', func_name, contributor)
            return

        response = requests.get(config['feed_url'], timeout=config.get('timeout', 1))
        response.raise_for_status()

        nav = navitia_wrapper.Navitia(url=config['navitia_url'], token=config['token'])\
                             .instance(config['coverage'])
        nav.timeout = 5

        proto = gtfs_realtime_pb2.FeedMessage()
        proto.ParseFromString(response.content)
        model_maker.handle(proto, nav, contributor)
        logger.info('%s for %s is finished', func_name, contributor)