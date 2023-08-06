# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import time

import requests
import urllib3

from kadi_apy.lib.exceptions import KadiAPYConfigurationError
from kadi_apy.lib.exceptions import KadiAPYRequestError


class KadiAPI:
    """Base manager class for the API.

    Manages the host and the personal access token (PAT) to use for all API requests,
    which need to be specified as class variables or as environment variables
    ``KADI_HOST``  and ``KADI_PAT``.
    """

    # The host to use for the API.
    host = None

    # The personal access token (PAT) to use for the API.
    token = None

    # Wether to verify the SSL/TLS certificate of the host.
    verify = True

    # The personal user id related to the PAT.
    _pat_user_id = None

    def __init__(self):
        self.host = self.host if self.host is not None else os.environ.get("KADI_HOST")
        if self.host is None:
            raise KadiAPYConfigurationError("No host information provided.")

        self.token = (
            self.token if self.token is not None else os.environ.get("KADI_PAT")
        )
        if self.token is None:
            raise KadiAPYConfigurationError("No personal access token (PAT) provided.")

        if self.host.endswith("/"):
            self.host = self.host[:-1]

        if not self.host.endswith("/api"):
            self.host = self.host + "/api"

        if not self.verify:
            requests.packages.urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning
            )

    def _make_request(self, endpoint, method=None, headers=None, timeout=1, **kwargs):
        if not endpoint.startswith(self.host):
            endpoint = self.host + endpoint

        response = getattr(requests, method)(
            endpoint,
            headers={"Authorization": f"Bearer {self.token}"},
            verify=self.verify,
            **kwargs,
        )

        # Check if any rate limit is exceeded and just wait an increasing amount of time
        # before repeating the request.
        if (
            response.status_code == 429
            and "Rate limit exceeded" in response.json()["description"]
        ):
            time.sleep(timeout)
            return self._make_request(
                endpoint, method=method, headers=headers, timeout=timeout + 1, **kwargs
            )

        return response

    def _get(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="get", **kwargs)

    def _post(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="post", **kwargs)

    def _patch(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="patch", **kwargs)

    def _put(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="put", **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="delete", **kwargs)

    @property
    def pat_user_id(self):
        """Get the user id related to the PAT.

        :return: The user id.
        """

        if self._pat_user_id is None:
            response = self._get("/users/me")
            payload = response.json()
            if response.status_code == 200:
                self._pat_user_id = payload["id"]
            else:
                raise KadiAPYRequestError(payload)

        return self._pat_user_id
