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

from unittest import TestCase
from unittest.mock import Mock
from hdc.core.catalog.crawler.netezza_crawler import NetezzaCrawler


class TestNetezzaCrawler(TestCase):
    def setUp(self) -> None:
        self._mock = Mock()

    def test_get_database_names(self):
        mock_db_result = [('TEST',)]
        expected_response = ['TEST']

        execute = self._mock.cursor.return_value
        execute.fetchall.return_value = mock_db_result

        self.assertEqual(NetezzaCrawler._get_database_names(self._mock), expected_response)

    def test_get_schema_names_by_db(self):
        mock_db_result = [('ADMIN',), ('DEFINITION_SCHEMA',), ('INFORMATION_SCHEMA',)]
        expected_response = ['ADMIN', 'DEFINITION_SCHEMA', 'INFORMATION_SCHEMA']

        execute = self._mock.cursor.return_value
        execute.fetchall.return_value = mock_db_result

        self.assertEqual(NetezzaCrawler._get_schema_names_by_db('TEST', self._mock), expected_response)

    def test_get_tables_by_db(self):
        mock_db_result = [('TEST', 'ADMIN', 'ABC', 'T1', 'INTEGER', 4, False, None), ('TEST', 'ADMIN', 'ABC', 'T5', 'CHARACTER VARYING(400)', -1, False, None),
                          ('TEST', 'ADMIN', 'ABC', 'C_SUM', 'CHARACTER VARYING(64000)', -1, False, None), ('TEST', 'ADMIN', 'TEST1', 'T1', 'INTEGER', 4, False, None),
                          ('TEST', 'ADMIN', 'TEST1', 'T5', 'CHARACTER VARYING(400)', -1, False, None), ('TEST', 'ADMIN', 'TEST2', 'U1', 'INTEGER', 4, False, None),
                          ('TEST', 'ADMIN', 'TEST2', 'U5', 'CHARACTER VARYING(400)', -1, False, None)]

        expected_response = {'TEST.ADMIN.ABC': [{'database': 'TEST', 'schema': 'ADMIN', 'name': 'ABC', 'columnName': 'T1', 'columnType': 'INTEGER', 'columnSize': 4,
                                                 'notNull': False, 'default': None}, {'database': 'TEST', 'schema': 'ADMIN', 'name': 'ABC', 'columnName': 'T5',
                                                                                      'columnType': 'CHARACTER VARYING(400)', 'columnSize': -1, 'notNull': False, 'default': None},
                                                {'database': 'TEST', 'schema': 'ADMIN', 'name': 'ABC', 'columnName': 'C_SUM',
                                                 'columnType': 'CHARACTER VARYING(64000)', 'columnSize': -1, 'notNull': False, 'default': None}],
                             'TEST.ADMIN.TEST1': [{'database': 'TEST', 'schema': 'ADMIN', 'name': 'TEST1', 'columnName': 'T1', 'columnType': 'INTEGER',
                                                   'columnSize': 4, 'notNull': False, 'default': None}, {'database': 'TEST', 'schema': 'ADMIN', 'name': 'TEST1',
                                                                                                         'columnName': 'T5', 'columnType': 'CHARACTER VARYING(400)',
                                                                                                         'columnSize': -1, 'notNull': False, 'default': None}],
                             'TEST.ADMIN.TEST2': [{'database': 'TEST', 'schema': 'ADMIN', 'name': 'TEST2', 'columnName': 'U1', 'columnType': 'INTEGER',
                                                   'columnSize': 4, 'notNull': False, 'default': None}, {'database': 'TEST', 'schema': 'ADMIN', 'name': 'TEST2',
                                                                                                         'columnName': 'U5', 'columnType': 'CHARACTER VARYING(400)',
                                                                                                         'columnSize': -1, 'notNull': False, 'default': None}]}

        execute = self._mock.cursor.return_value
        execute.fetchall.return_value = mock_db_result

        self.assertEqual(NetezzaCrawler._get_tables_by_db('TEST', self._mock), expected_response)
