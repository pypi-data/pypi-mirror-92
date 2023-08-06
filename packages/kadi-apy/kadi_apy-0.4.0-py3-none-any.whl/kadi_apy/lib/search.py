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
from kadi_apy.lib.core import KadiAPI


class SearchResource(KadiAPI):
    """Search class for resources"""

    def search_items(self, item, **params):
        """Search for items"""

        return self._get(endpoint=item.base_path, params=params)

    def search_items_user(self, item, user, **params):
        """Search for items of users"""

        endpoint = f"/users/{user}{item.base_path}"
        return self._get(endpoint=endpoint, params=params)


class SearchUser(KadiAPI):
    """Search class for users"""

    def search_users(self, **params):
        """Search for users"""

        return self._get(endpoint="/users", params=params)
