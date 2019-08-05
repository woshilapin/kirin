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
from flask_restful import Resource

import logging
from datetime import datetime
from kirin.utils import make_rt_update, record_call
from kirin.exceptions import KirinException
from kirin import core
from kirin.core import model


class AbstractSNCFResource(Resource):
    def __init__(self, nav_wrapper, timeout, contributor, builder):
        self.navitia_wrapper = nav_wrapper
        self.navitia_wrapper.timeout = timeout
        self.contributor = contributor
        self.builder = builder

    def process_post(self, input_raw, contributor_type, is_new_complete=False):

        # create a raw rt_update obj, save the raw_input into the db
        rt_update = make_rt_update(input_raw, contributor_type, contributor=self.contributor)
        start_datetime = datetime.utcnow()
        try:
            # assuming UTF-8 encoding for all input
            rt_update.raw_data = rt_update.raw_data.encode("utf-8")

            # raw_input is interpreted
            trip_updates = self.builder(self.navitia_wrapper, self.contributor).build(rt_update)
            record_call("OK", contributor=self.contributor)
        except KirinException as e:
            rt_update.status = "KO"
            rt_update.error = e.data["error"]
            model.db.session.add(rt_update)
            model.db.session.commit()
            record_call("failure", reason=str(e), contributor=self.contributor)
            raise
        except Exception as e:
            rt_update.status = "KO"
            rt_update.error = e.message
            model.db.session.add(rt_update)
            model.db.session.commit()
            record_call("failure", reason=str(e), contributor=self.contributor)
            raise

        _, log_dict = core.handle(rt_update, trip_updates, self.contributor, is_new_complete=is_new_complete)
        duration = (datetime.utcnow() - start_datetime).total_seconds()
        log_dict.update({"duration": duration})
        record_call("Simple feed publication", **log_dict)
        logging.getLogger(__name__).info("Simple feed publication", extra=log_dict)

        return "OK", 200
