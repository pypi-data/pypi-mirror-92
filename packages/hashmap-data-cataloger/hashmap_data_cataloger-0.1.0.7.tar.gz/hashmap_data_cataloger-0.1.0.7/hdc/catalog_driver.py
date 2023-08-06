# Copyright © 2020 Hashmap, Inc
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
import logging
import os
from providah.factories.package_factory import PackageFactory as pf
from hdc.core.orchestrator.orchestrator import Orchestrator
from hdc.core.utils.parse_config import ParseConfig


class CatalogDriver:
    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        # Set up orchestration engine
        self._initiate_orchestrator()

    def _initiate_orchestrator(self):
        if "netezza" in os.getenv('HDC_SOURCE') and "snowflake" in os.getenv('HDC_DESTINATION'):
            self._orchestrator: Orchestrator = pf.create(key='NetezzaSnowflakeOrchestrator',
                                                         configuration={'config_path': os.getenv('HDC_PROFILE_PATH'),
                                                                        'source_env': os.getenv('HDC_SOURCE'),
                                                                        'destination_env': os.getenv('HDC_DESTINATION')})

    def run(self):
        self._orchestrator.run_cataloging()
