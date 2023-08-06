# -*- coding:utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from networkapiclient.ApiGenericClient import ApiGenericClient


class Healthcheck(ApiGenericClient):

    def __init__(self, networkapi_url, user, password, user_ldap=None):
        """Class constructor receives parameters to connect to the networkAPI.
        :param networkapi_url: URL to access the network API.
        :param user: User for authentication.
        :param password: Password for authentication.
        """

        super(Healthcheck, self).__init__(
            networkapi_url,
            user,
            password,
            user_ldap
        )

    def inserir(self, identifier, healthcheck_type, healthcheck_request, healthcheck_expect, destination, old_healthcheck_id=None):

        uri = "api/healthcheck/insert/"

        data = dict()
        data['identifier'] = identifier
        data['healthcheck_type'] = healthcheck_type
        data['healthcheck_request'] = healthcheck_request
        data['healthcheck_expect'] = healthcheck_expect
        data['destination'] = destination
        data['old_healthcheck_id'] = old_healthcheck_id

        return self.post(uri, data=data)

