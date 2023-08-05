# -*- coding:utf-8 -*-

import gdpy
import mock
from gdpy.http import requests
from unittests.common import *


def makeResponse202():
    status = 202
    headers = {},
    response = requests.Response
    response.text = '"{success}"'
    return MockResponse_base(status, headers, response)


def makeResponse200_4_list():
    status = 200
    headers = {},
    response = requests.Response
    response.text = '{"items":{}}'
    response.content = '{"items":{}}'
    return MockResponse_base(status, headers, response)


def makeResponse200_4_getparam():
    status = 200
    headers = {},
    response = requests.Response
    response.text = '{"parameter":{}}'
    response.content = '{"parameter":{}}'
    return MockResponse_base(status, headers, response)


@mock.patch('gdpy.Session.do_request')
class TestData(GDTestCase):
    # invalid data path
    def test_archive_data_failed(self, do_request):
        req_info = mock_response(do_request, makeResponse202())
        with self.assertRaises(ValueError) as cm:
            result = data().archive_data(None)
        self.assertEquals(str(cm.exception), 'Expect a date path')

    def test_archive_data_success(self, do_request):
        req_info = mock_response(do_request, makeResponse202())
        result = data().archive_data('test.txt')
        self.assertEquals(result.status, 202)
        self.assertEquals(result.response.text, '"{success}"')

    # invalid data path
    def test_restore_data_failed(self, do_request):
        req_info = mock_response(do_request, makeResponse202())
        with self.assertRaises(ValueError) as cm:
            result = data().restore_data(None)
        self.assertEquals(str(cm.exception), 'Expect a date path')

    def test_restore_data_success(self, do_request):
        req_info = mock_response(do_request, makeResponse202())
        result = data().restore_data('test.txt')
        self.assertEquals(result.status, 202)
        self.assertEquals(result.response.text, '"{success}"')



if __name__ == '__main__':
        unittest.main()
