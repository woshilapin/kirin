# coding: utf8
#
# Copyright (c) 2020, Canal TP and/or its affiliates. All rights reserved.
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

from kirin import app, db
from kirin.command.piv_worker import PivWorker
from kirin.core.model import RealTimeUpdate
from kirin.core.types import ConnectorType
from kirin.piv.piv import get_piv_contributor
from tests.integration.conftest import PIV_CONTRIBUTOR_ID, PIV_EXCHANGE_NAME, PIV_QUEUE_NAME

from amqp.exceptions import NotFound
from kombu import Connection, Exchange, Queue
import pytest
import threading
from retrying import retry


@retry(stop_max_delay=20000, wait_exponential_multiplier=100)
def wait_until(predicate):
    assert predicate()


def is_exchange_created(connection, exchange_name, exchange_type="fanout"):
    try:
        channel = connection.channel()
        channel.exchange_declare(exchange_name, exchange_type, nowait=False, passive=True)
    except NotFound as e:
        return False
    except Exception as e:
        raise e
    return True


def is_queue_created(connection, queue_name):
    try:
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, nowait=False, passive=True)
    except NotFound as e:
        return False
    except Exception as e:
        raise e
    return True


@pytest.fixture(scope="session", autouse=True)
def broker_connection(rabbitmq_docker_fixture):
    return Connection(rabbitmq_docker_fixture.url)


@pytest.fixture(scope="session", autouse=True)
def mq_handler(rabbitmq_docker_fixture, broker_connection):
    return rabbitmq_docker_fixture.create_rabbitmq_handler(PIV_EXCHANGE_NAME, "fanout")


def create_exchange(broker_connection, exchange_name):
    exchange = Exchange(
        exchange_name,
        durable=True,
        delivery_mode=2,
        type="fanout",
        auto_delete=False,
        no_declare=False,
    )
    exchange.declare(channel=broker_connection.channel())


# Use scope 'function' so the Exchange is recreated for every test.
# It is useful because some tests are deleting the Exchange.
@pytest.fixture(scope="function", autouse=True)
def init_piv_exchange(broker_connection):
    create_exchange(broker_connection, PIV_EXCHANGE_NAME)
    assert is_exchange_created(broker_connection, PIV_EXCHANGE_NAME)


def launch_piv_worker(pg_docker_fixture):
    import kirin
    from kirin import app, db, manager
    from tests.conftest import init_flask_db
    from tests.integration.conftest import PIV_CONTRIBUTOR_ID

    with app.app_context():
        # re-init the db by overriding the db_url
        init_flask_db(pg_docker_fixture)
        contributor = get_piv_contributor(PIV_CONTRIBUTOR_ID)
        with PivWorker(contributor) as worker:
            worker.run()


class PivWorkerTest:
    def __init__(self, test_client, broker_url, broker_connection, pg_docker_fixture):
        self.test_client = test_client
        self.broker_url = broker_url
        self.broker_connection = broker_connection
        self.pg_docker_fixture = pg_docker_fixture

    def __enter__(self):
        # Launch a PivWorker
        self.thread = threading.Thread(target=launch_piv_worker, args=(self.pg_docker_fixture,))
        self.thread.start()
        wait_until(lambda: self.thread.is_alive())
        # Check that PivWorker is ready (a good hint is when queue is created)
        wait_until(lambda: is_queue_created(self.broker_connection, PIV_QUEUE_NAME))

    def __exit__(self, type, value, traceback):
        # Remove the contributor
        self.test_client.delete("/contributors/{}".format(PIV_CONTRIBUTOR_ID))
        # PivWorker should die eventually when no PIV contributors is available
        wait_until(lambda: not self.thread.is_alive())


def test_mq_message_received_and_stored(
    test_client, pg_docker_fixture, rabbitmq_docker_fixture, broker_connection, mq_handler
):
    with PivWorkerTest(test_client, rabbitmq_docker_fixture.url, broker_connection, pg_docker_fixture):
        # Check that PivWorker is creating the queue
        wait_until(lambda: is_queue_created(broker_connection, PIV_QUEUE_NAME))

        # Check that MQ message is received and stored in DB
        mq_handler.publish(str('{"key": "Some valid JSON"}'), PIV_CONTRIBUTOR_ID)
        wait_until(lambda: RealTimeUpdate.query.count() == 1)
