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

import os
from hdc.core.catalog.crawler.netezza_crawler import NetezzaCrawler
from hdc.core.catalog.ddl_writer.snowflake_ddl_writer import SnowflakeDDLWriter
from hdc.core.catalog.mapper.netezza_to_snowflake_mapper import NetezzaToSnowflakeMapper


class PackageFactory:
    @classmethod
    def catalog(cls, source_env: str, path: str) -> tuple:
        os.environ['HDC_PROFILE_PATH'] = path
        crawler = NetezzaCrawler(connection_name=source_env)
        return crawler.run()

    @classmethod
    def map(cls, data_tuple) -> tuple:
        mapper = NetezzaToSnowflakeMapper(databases=data_tuple[0], schemas=data_tuple[1], tables=data_tuple[2])
        return mapper.map()

    @classmethod
    def write(cls, destination_env: str, path: str, sql_tuple) -> None:
        os.environ['HDC_PROFILE_PATH'] = path
        writer = SnowflakeDDLWriter(connection_name=destination_env, database_sql=sql_tuple[0], schema_sql=sql_tuple[1], table_sql=sql_tuple[2])
        writer.execute()
