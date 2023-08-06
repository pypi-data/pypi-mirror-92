"""
"""

# Created on 2016.08.09
#
# Author: Giovanni Cannata
#
# Copyright 2016 - 2020 Giovanni Cannata
#
# This file is part of ldap3.
#
# ldap3 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ldap3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ldap3 in the COPYING and COPYING.LESSER files.
# If not, see <http://www.gnu.org/licenses/>.

import unittest

from ldap3 import ALL
from ldap3 import ObjectDef, Reader
from test.config import test_base, get_connection, drop_connection, random_id, add_user

testcase_id = ''


class Test(unittest.TestCase):
    def setUp(self):
        global testcase_id
        testcase_id = random_id()
        self.connection = get_connection(get_info=ALL, check_names=True)
        self.delete_at_teardown = []

    def tearDown(self):
        drop_connection(self.connection, self.delete_at_teardown)
        self.assertFalse(self.connection.bound)

    def test_create_objectdef_from_schema(self):
        o = ObjectDef(['inetorgPerson', 'person'], self.connection)
        self.assertEqual(o.cn.name, 'cn')

    def test_search_object(self):
        self.delete_at_teardown.append(add_user(self.connection, testcase_id, 'abstract-1'))
        o = ObjectDef(['inetorgPerson', 'person'], self.connection)
        r = Reader(self.connection, o, test_base, '(cn=' + testcase_id + 'abstract-1)')
        r.search(attributes='cn')  # AD returns operationError for reading some atributes
        self.assertEqual(len(r), 1)
        self.assertEqual(r.entries[0].cn, testcase_id + 'abstract-1')
