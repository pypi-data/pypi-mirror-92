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
import platform
import os


class ProjectConfig:
    @classmethod
    def hdc_env(cls):
        env = os.getenv('HDC_ENV')
        if not env:
            env = 'dev'
            os.environ['HDC_ENV'] = env
        return env

    @classmethod
    def profile_path(cls):
        return os.getenv('HDC_PROFILE_PATH')

    @classmethod
    def connection_max_attempts(cls):
        return 3

    @classmethod
    def connection_timeout(cls):
        return 3

