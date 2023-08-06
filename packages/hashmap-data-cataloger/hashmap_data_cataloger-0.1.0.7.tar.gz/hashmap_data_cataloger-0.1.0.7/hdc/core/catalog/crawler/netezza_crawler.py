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
from hdc.core.dao.netezza_jdbc import NetezzaJDBC
from hdc.core.dao.netezza_odbc import NetezzaODBC


class NetezzaCrawler:
    @classmethod
    def _get_logger(cls):
        return logging.getLogger(cls.__name__)

    def __init__(self, **kwargs):
        self._logger = self._get_logger()
        self.__connection_choice = kwargs.get('connection_name')

    def run(self) -> tuple:
        try:
            with NetezzaJDBC(connection=self.__connection_choice).connection as conn:
                databases = self._get_database_names(conn)
                schemas = []
                tables = {}
                for db in databases:
                    schemas.extend(self._get_schema_names_by_db(db, conn))
                    tables.update(self._get_tables_by_db(db, conn))
                return databases, schemas, tables
        except Exception:
            try:
                with NetezzaODBC(connection=self.__connection_choice).connection as conn:
                    databases = self._get_database_names(conn)
                    schemas = []
                    tables = {}
                    for db in databases:
                        schemas.extend(self._get_schema_names_by_db(db, conn))
                        tables.update(self._get_tables_by_db(db, conn))
                    return databases, schemas, tables
            except Exception:
                raise ValueError("Unable to connect to Netezza source. Please check if source is up. Check the configuration: %s" % self.__connection_choice)

    @classmethod
    def _get_database_names(cls, conn) -> list:
        query_string = "SELECT DATABASE FROM _V_DATABASE WHERE DATABASE <> 'SYSTEM'"
        databases = []
        cursor = conn.cursor()
        cursor.execute(query_string)
        result = cursor.fetchall()
        for row in result:
            databases.append(row[0])

        return databases

    @classmethod
    def _get_schema_names_by_db(cls, database, conn) -> list:
        query_string = f"SELECT DISTINCT SCHEMA FROM {database}.._V_SCHEMA"  # WHERE OBJTYPE = 'TABLE'"
        schemas = []

        cursor = conn.cursor()
        cursor.execute(query_string)
        result = cursor.fetchall()

        for row in result:
            schemas.append(row[0])
        return schemas

    @classmethod
    def _get_tables_by_db(cls, database, conn) -> dict:
        query_string = f"SELECT DATABASE, SCHEMA, NAME, ATTNAME, FORMAT_TYPE, ATTLEN, ATTNOTNULL, COLDEFAULT " \
                       f"FROM {database}.._V_RELATION_COLUMN " \
                       f"WHERE DATABASE <> 'SYSTEM' AND TYPE = 'TABLE' ORDER BY SCHEMA, NAME, ATTNUM ASC"
        tables = {}

        cursor = conn.cursor()
        cursor.execute(query_string)
        result = cursor.fetchall()

        for row in result:
            table_name = f"{row[0]}.{row[1]}.{row[2]}"  # ignoring name collisions across multiple db's for now
            if table_name not in tables:
                tables[table_name] = []

            column = {
                'database': row[0],
                'schema': row[1],
                'name': row[2],
                'columnName': row[3],
                'columnType': row[4],
                'columnSize': row[5],
                'notNull': row[6],
                'default': row[7]
            }
            tables[table_name].append(column)
        return tables
