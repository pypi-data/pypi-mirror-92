# -*- coding:utf-8 -*-

import unittest
import functools
import re
import gdpy


def task():
    return gdpy.Tasks(gdpy.GeneDockAuth('fake-access-key-id', 'fake-access-key-secret'),
                      'https://cn-beijing-api.genedock.com', 'res_account_name', 'project_name')


def workflow():
    return gdpy.Workflows(gdpy.GeneDockAuth('fake-access-key-id', 'fake-access-key-secret'),
                          'https://cn-beijing-api.genedock.com', 'res_account_name', 'project_name')


def tool():
    return gdpy.Tools(gdpy.GeneDockAuth('fake-access-key-id', 'fake-access-key-secret'),
                      'https://cn-beijing-api.genedock.com', 'res_account_name', 'project_name')


def data():
    return gdpy.Data(gdpy.GeneDockAuth('fake-access-key-id', 'fake-access-key-secret'),
                      'https://cn-beijing-api.genedock.com', 'res_account_name', 'project_name')


class GDTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GDTestCase, self).__init__(*args, **kwargs)
        self.default_connect_timeout = gdpy.defaults.connect_timeout
        self.default_request_retries = gdpy.defaults.request_retries

    def setUp(self):
        self.default_connect_timeout = gdpy.defaults.connect_timeout
        self.default_request_retries = gdpy.defaults.request_retries


class RequestInfo(object):
    def __init__(self):
        self.req = None
        self.data = None
        self.resp = None
        self.size = None


def do4response(req, timeout, req_info=None, payload=None):
    if req_info:
        req_info.req = req

        if req.data is None:
            req_info.data = b''
            req_info.size = 0
        else:
            req_info.data = gdpy.to_bytes(req.data)
            req_info.size = len(req.data)

    return MockResponse_base(payload.status, payload.headers, payload.response)


def mock_response(do_request, payload):
    req_info = RequestInfo()

    do_request.auto_spec = True
    do_request.side_effect = functools.partial(do4response, req_info=req_info, payload=payload)
    return req_info


class MockResponse_base(object):
    def __init__(self, status, headers, response):
        self.status = status
        self.headers = headers
        self.response = response

    def read(self, amt=None):
        return self.__io.read(fmt)
