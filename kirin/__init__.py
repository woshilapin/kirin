# coding=utf-8

# Copyright (c) 2001-2015, Canal TP and/or its affiliates. All rights reserved.
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
import os

from kirin import exceptions

# remplace blocking method by a non blocking equivalent
# this enable us to use gevent for launching background task
# Note: there is a conflict between py.test and gevent
# http://stackoverflow.com/questions/8774958/keyerror-in-module-threading-after-a-successful-py-test-run
# so we need to remove threading from the import
import sys

if str("threading") in sys.modules:
    del sys.modules[str("threading")]
# end of conflict's patch


from flask import Flask
import logging.config
from flask_script import Manager
from kirin.helper import KirinRequest

app = Flask(__name__)
app.config.from_object(str("kirin.default_settings"))  # type: ignore
if "KIRIN_CONFIG_FILE" in os.environ:
    app.config.from_envvar(str("KIRIN_CONFIG_FILE"))  # type: ignore
app.request_class = KirinRequest

from kirin import new_relic

new_relic.init(app.config[str("NEW_RELIC_CONFIG_FILE")])

if app.config[str("USE_GEVENT")]:
    from gevent import monkey

    monkey.patch_all()

from flask_cache import Cache

# register the cache instance and binds it on to your app
app.cache = Cache(app)

manager = Manager(app)

from redis import Redis

redis_client = Redis(
    host=app.config[str("REDIS_HOST")],
    port=app.config[str("REDIS_PORT")],
    db=app.config[str("REDIS_DB")],
    password=app.config[str("REDIS_PASSWORD")],
)

# activate a command
import kirin.command.load_realtime

from kirin.core import model

db = model.db
db.init_app(app)


# We need to log all kinds of patch, all patch must be done as soon as possible
logger = logging.getLogger(__name__)
if str("threading") not in sys.modules:
    logger.info("threading is deleted from sys.modules")
logger.info("Configs: %s", app.config)


from kirin.rabbitmq_handler import RabbitMQHandler

rabbitmq_handler = RabbitMQHandler(app.config[str("RABBITMQ_CONNECTION_STRING")], app.config[str("EXCHANGE")])

import kirin.api
from kirin import utils

if str("LOGGER") in app.config:
    logging.config.dictConfig(app.config[str("LOGGER")])
else:  # Default is std out
    handler = logging.StreamHandler(stream=sys.stdout)
    app.logger.addHandler(handler)
    app.logger.setLevel("INFO")
