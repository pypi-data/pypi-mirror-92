# -*- coding:utf-8 -*-

import gdpy
import mock

from gdpy.utils import is_object_name_valid, is_object_version_valid, to_unixtime
from unittests.common import *


class TestUtils(GDTestCase):
    def test_object_name(self):
        name = "123"
        self.assertTrue(is_object_name_valid(name))

        name = "a1"
        self.assertFalse(is_object_name_valid(name))

        name = "a" * 129
        self.assertFalse(is_object_name_valid(name))

        name = "ab_#$%"
        self.assertFalse(is_object_name_valid(name))

        # normal case:
        name = "abc"
        self.assertTrue(is_object_name_valid(name))

        name = "a" * 128
        self.assertTrue(is_object_name_valid(name))

        name = "ab_cd123ABC"
        self.assertTrue(is_object_name_valid(name))

    def test_object_version(self):
        version = -1
        self.assertFalse(is_object_version_valid(version))

        version = 0
        self.assertFalse(is_object_version_valid(version))

        version = 1
        self.assertTrue(is_object_version_valid(version))

        version = 'hasdklf'
        self.assertFalse(is_object_version_valid(version))

    def test_to_unixtime(self):
        _GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        _ISO8601_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'
        iso8601_format_time = '2013-10-10T23:40:0.000Z'
        gmt_format_time = 'Thu, 10 Oct 2013 23:40:00 GMT'
        self.assertEquals(to_unixtime(iso8601_format_time, _ISO8601_FORMAT), 1381448400)
        self.assertEquals(to_unixtime(gmt_format_time, _GMT_FORMAT), 1381448400)


if __name__ == 'main':
    unittest.main()
