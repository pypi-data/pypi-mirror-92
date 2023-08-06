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
import argparse
import os
import logging.config
import warnings
from hdc.catalog_driver import CatalogDriver
from hdc.core.utils.parse_config import ParseConfig
warnings.filterwarnings("ignore")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--path", type=str, help="path for profile yml file that has connection information")
    parser.add_argument("-s", "--source", type=str, help="source connection name in profile yml file")
    parser.add_argument("-d", "--destination", type=str, help="destination connection name in profile yml file")
    parser.add_argument("-l", "--log_settings", type=str, default="log_settings.yml", help="log settings path")
    parser.add_argument("-e", "--env", type=str, default="prod", help="environment to take connection information "
                                                                      "from in hdc_profiles.yml")
    args = parser.parse_args()

    os.environ['HDC_ENV'] = args.env
    os.environ['HDC_PROFILE_PATH'] = args.path
    os.environ['HDC_SOURCE'] = args.source
    os.environ['HDC_DESTINATION'] = args.destination

    log_settings = ParseConfig.parse(config_path=args.log_settings)
    logging.config.dictConfig(log_settings)

    director = CatalogDriver()
    director.run()
