# Copyright (c) 2001-2018, Canal TP and/or its affiliates. All rights reserved.
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

import six
from flask_restful import Resource

import logging
from datetime import datetime

from kirin.new_relic import record_custom_parameter, must_log_apm, is_invalid_input_exception
from kirin.utils import make_rt_update, record_call, set_rtu_status_ko, allow_reprocess_same_data
from kirin.exceptions import KirinException, InvalidArguments
from kirin import core
from kirin.core import model


class AbstractSNCFResource(Resource):
    def __init__(self, nav_wrapper, timeout, contributor, builder):
        self.navitia_wrapper = nav_wrapper
        self.navitia_wrapper.timeout = timeout
        self.contributor = contributor
        self.builder = builder

    def process_post(self, input_raw, contributor_type, is_new_complete=False):
        start_datetime = datetime.utcnow()
        rt_update = None
        log_dict = {"contributor": self.contributor}
        status = "OK"

        try:
            # create a raw rt_update obj, save the raw_input into the db
            rt_update = make_rt_update(input_raw, contributor_type, contributor=self.contributor)
            # assuming UTF-8 encoding for all input
            rt_update.raw_data = rt_update.raw_data.encode("utf-8")

            # raw_input is interpreted
            trip_updates = self.builder(self.navitia_wrapper, self.contributor).build(rt_update)
            _, handler_log_dict = core.handle(
                rt_update, trip_updates, self.contributor, is_new_complete=is_new_complete
            )
            log_dict.update(handler_log_dict)

        except Exception as e:
            status = "failure"
            allow_reprocess = True
            if is_invalid_input_exception(e):
                status = "warning"  # Kirin did his job correctly if the input is invalid and rejected
                allow_reprocess = False  # reprocess is useless if input is invalid

            if rt_update is not None:
                error = e.data["error"] if (isinstance(e, KirinException) and "error" in e.data) else e.message
                set_rtu_status_ko(rt_update, error, is_reprocess_same_data_allowed=allow_reprocess)
                model.db.session.add(rt_update)
                model.db.session.commit()
            else:
                # rt_update is not built, make sure reprocess is allowed
                allow_reprocess_same_data(self.contributor)

            log_dict.update({"exc_summary": six.text_type(e), "reason": e})

            record_custom_parameter("reason", e)  # use __str__() to have complete details
            raise  # filters later for APM

        finally:
            log_dict.update({"duration": (datetime.utcnow() - start_datetime).total_seconds()})
            record_call(status, **log_dict)
            if status == "OK":
                logging.getLogger(__name__).info(status, extra=log_dict)
            elif status == "warning":
                logging.getLogger(__name__).warning(status, extra=log_dict)
            else:
                logging.getLogger(__name__).error(status, extra=log_dict)

        return "OK", 200
