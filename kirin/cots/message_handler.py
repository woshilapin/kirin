# coding=utf-8
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
import logging

import pybreaker
import requests as requests

from kirin import app
from flask.globals import current_app

from kirin.exceptions import ObjectNotFound, UnauthorizedOnSubService, SubServiceError


class MessageHandler:
    """
    class managing calls to ParIV-Motif external service providing cause messages associated to
    SNCF realtime feed COTS

    The service's authentication is done via Oauth2.0

    curl example to check/test that external service is working:
    # first get a token
    curl -H 'X-API-Key: {api_key}' -d 'client_id={client_id}' -d 'client_secret={client_secret}'
         -d 'grant_type={grant_type}' -X POST '{token_url}'
    # then retrieve the whole message referential using the 'access_token' value obtained
    curl -H 'X-API-Key: {api_key}' -H 'Authorization: Bearer {access_token}'
         -X GET '{resource_url}'

    All variables are provided on connector's init, except for the {access_token}

    So in practice it will look like:
    curl -H 'X-API-Key: ef876876-6543se' -d 'client_id=username' -d 'client_secret=password'
         -d 'grant_type=client_credentials' -X POST 'https://motif.sncf/oauth/token'
    curl -H 'X-API-Key: ef876876-6543se' -H 'Authorization: Bearer fzkS.Ekb4S.QA'
         -X GET 'https://motif.sncf/api/delayLabels'
    """

    def __init__(self, api_key, resource_server, token_server, client_id, client_secret, grant_type, timeout):
        self.api_key = api_key
        self.resource_server = resource_server
        self.token_server = token_server
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type
        self.timeout = timeout
        self.breaker = pybreaker.CircuitBreaker(
            fail_max=current_app.config["COTS_PAR_IV_CIRCUIT_BREAKER_MAX_FAIL"],
            reset_timeout=current_app.config["COTS_PAR_IV_CIRCUIT_BREAKER_TIMEOUT_S"],
        )

    def __repr__(self):
        """
        Allow this class to be cacheable
        """
        return "{}.{}.{}.{}".format(self.__class__, self.resource_server, self.token_server, self.client_id)

    def _service_caller(self, method, url, headers, data=None):
        try:
            kwargs = {"timeout": self.timeout, "headers": headers}
            if data:
                kwargs.update({"data": data})
            response = self.breaker.call(method, url, **kwargs)
            if not response or response.status_code != 200:
                logging.getLogger(__name__).error(
                    "COTS cause message sub-service, Invalid response, "
                    "status_code: {}".format(response.status_code)
                )
                if response.status_code == 401:
                    raise UnauthorizedOnSubService(
                        "Unauthorized on COTS message sub-service {} {}".format(method, url)
                    )
                raise ObjectNotFound(
                    "non 200 response on COTS cause message " "sub-service {} {}".format(method, url)
                )
            return response
        except pybreaker.CircuitBreakerError as e:
            logging.getLogger(__name__).error("COTS cause message sub-service dead (error: {})".format(e))
            raise SubServiceError("COTS cause message sub-service circuit breaker open")
        except requests.Timeout as t:
            logging.getLogger(__name__).error("COTS cause message sub-service timeout (error: {})".format(t))
            raise SubServiceError("COTS cause message sub-service timeout")
        except (UnauthorizedOnSubService, ObjectNotFound):
            raise  # Do not change exceptions that were just raised
        except Exception as e:
            logging.getLogger(__name__).exception(
                "COTS cause message sub-service handling " "error : {}".format(str(e))
            )
            raise SubServiceError(str(e))

    @app.cache.memoize(timeout=app.config.get("COTS_PAR_IV_TIMEOUT_TOKEN", 60 * 60))
    def _get_access_token(self):
        headers = {"X-API-Key": str(self.api_key)}
        data = {"client_id": self.client_id, "client_secret": self.client_secret, "grant_type": self.grant_type}

        response = self._service_caller(method=requests.post, url=self.token_server, headers=headers, data=data)
        if not response:
            return None
        content = response.json()
        access_token = content.get("access_token")
        if not access_token:
            logging.getLogger(__name__).error("COTS cause message sub-service, no access_token in response")
            return None
        return access_token

    def _call_webservice(self):
        access_token = self._get_access_token()
        if access_token is None:
            raise SubServiceError("Impossible to get a token for COTS cause message sub-service")
        headers = {"X-API-Key": self.api_key, "Authorization": "Bearer {}".format(access_token)}
        resp = self._service_caller(method=requests.get, url=self.resource_server, headers=headers)
        messages = {}
        if not resp:
            return messages
        for m in resp.json():
            if "id" in m and "labelExt" in m:
                messages[m["id"]] = m["labelExt"]
        return messages

    @app.cache.memoize(timeout=app.config.get("COTS_PAR_IV_CACHE_TIMEOUT", 60 * 60))
    def _call_webservice_safer(self):
        try:
            return self._call_webservice()
        except UnauthorizedOnSubService:
            # if call was unauthorized, the token is probably expired, so: delete cache and retry
            app.cache.delete_memoized(MessageHandler._get_access_token)
            return self._call_webservice()

    def get_message(self, index):
        if self.token_server and self.resource_server:
            try:
                return self._call_webservice_safer().get(index)
            except Exception as e:
                logging.getLogger(__name__).exception(
                    "COTS cause message sub-service handling " "error : {}".format(str(e))
                )
                return None
