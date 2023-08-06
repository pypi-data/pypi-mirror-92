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
from kadi_apy.cli.commons import raise_request_error
from kadi_apy.cli.decorators import apy_command
from kadi_apy.cli.decorators import id_identifier_options
from kadi_apy.cli.decorators import user_id_options
from kadi_apy.cli.lib.collections import CLICollection
from kadi_apy.cli.lib.groups import CLIGroup
from kadi_apy.cli.lib.records import CLIRecord
from kadi_apy.cli.lib.templates import CLITemplate
from kadi_apy.cli.lib.users import CLIUser
from kadi_apy.cli.search import CLISearchResource
from kadi_apy.cli.search import CLISearchUser
from kadi_apy.lib.core import KadiAPI
from kadi_apy.lib.miscellaneous import Miscellaneous
from kadi_apy.lib.resources.collections import Collection
from kadi_apy.lib.resources.groups import Group
from kadi_apy.lib.resources.records import Record
from kadi_apy.lib.resources.templates import Template
from kadi_apy.lib.resources.users import User
from kadi_apy.lib.search import SearchResource
from kadi_apy.lib.search import SearchUser
