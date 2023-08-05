# -*- coding:utf-8 -*-

import gdpy
import mock
from gdpy.http import requests
from unittests.common import *


def makeResponse200():
    status = 200
    headers = {},
    response = requests.Response
    response.text = '"{success}"'
    return MockResponse_base(status, headers, response)


def makeResponse200_4_listworkflows():
    status = 200
    headers = {}
    response = requests.Response
    response.text = '{"items": {}}'
    response.content = '{"items": {}}'
    return MockResponse_base(status, headers, response)


def makeResponse200_4_excworkflows():
    status = 200
    headers = {}
    response = requests.Response
    response.text = '{"parameter": {"Condition": {}}}'
    response.content = '{"parameter": {"Condition": {}}}'
    return MockResponse_base(status, headers, response)


@mock.patch('gdpy.Session.do_request')
class TestWorkflow(GDTestCase):
    # invalid workflow version
    def test_get_workflow_failed(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        with self.assertRaises(ValueError) as cm:
            result = workflow().get_workflow('TestWorkflow', 'version')
        self.assertEquals(str(cm.exception), 'Invalid workflow version! Expect interger greater than 0, but got version')

        with self.assertRaises(ValueError) as cm:
            result = workflow().get_workflow('TestWorkflow', -1)
        self.assertEquals(str(cm.exception), 'Invalid workflow version! Expect interger greater than 0, but got -1')

    # invalid workflow name
        with self.assertRaises(ValueError) as cm:
            result = workflow().get_workflow(1, 1)
        self.assertEquals(str(cm.exception), 'Invalid workflow name! Expect a string started with alphabet and under 128 characters, but got 1!')

    # get workflow without version
    def test_get_workflow_success(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        result = workflow().get_workflow('TestWorkflow')
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

        result = workflow().get_workflow('TestWorkflow', None)
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    # get workflow with version
        result = workflow().get_workflow('TestWorkflow', 1)
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    # get executable workflow failed
    # lack version
    def test_get_exe_workflow_failed(self, do_request):
        req_info = mock_response(do_request, makeResponse200_4_excworkflows())
        with self.assertRaises(TypeError) as cm:
            result = workflow().get_exc_workflow('TestWorkflow')

    # invalid version
        with self.assertRaises(ValueError) as cm:
            result = workflow().get_exc_workflow('TestWorkflow', 'asdkjfl')
        self.assertEquals(str(cm.exception), 'Invalid workflow version! Expect interger greater than 0, but got asdkjfl')

    # invalid name
        with self.assertRaises(ValueError) as cm:
            result = workflow().get_exc_workflow(1, 1)
        self.assertEquals(str(cm.exception), 'Invalid workflow name! Expect a string started with alphabet and under 128 characters, but got 1!')

    # get executable workflow success
    def test_get_exe_workflow_success(self, do_request):
        req_info = mock_response(do_request, makeResponse200_4_excworkflows())
        result = workflow().get_exc_workflow('TestWorkflow', 1)
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '{"parameter": {"Condition": {}}}')

    # test list workflows
    def test_list_workflow(self, do_request):
        req_info = mock_response(do_request, makeResponse200_4_listworkflows())
        result = workflow().list_workflows()
        self.assertEquals(result.status, 200)

    # test list executable workflows
    def test_list_exe_workflow_failed(self, do_request):
        req_info = mock_response(do_request, makeResponse200_4_listworkflows())
        result = workflow().list_exc_workflows()
        self.assertEquals(result.status, 200)

    # test delete workflow
    def test_delete_workflow(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        result = workflow().get_workflow('TestWorkflow', 1)
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    # test create workflow:
    def test_create_workflow(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        result = workflow().create_workflow('TestWorkflow', 1)
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    # invalid name
    def test_create_workflow_failed(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        with self.assertRaises(ValueError) as cm:
            result = workflow().create_workflow(1, 1)
        self.assertEquals(str(cm.exception), 'Invalid workflow name! Expect a string started with alphabet and under 128 characters, but got 1!')

        with self.assertRaises(ValueError) as cm:
            result = workflow().create_workflow(None, 1)
        self.assertEquals(str(cm.exception), 'Invalid workflow name! Expect a string started with alphabet and under 128 characters, but got None!')

    # invalid version
        with self.assertRaises(ValueError) as cm:
            result = workflow().create_workflow('TestWorkflow', 'klasjflkj')
        self.assertEquals(str(cm.exception), 'Invalid workflow version! Expect interger greater than 0, but got klasjflkj')

        with self.assertRaises(ValueError) as cm:
            result = workflow().create_workflow('TestWorkflow', 1.1)

    # test put workflow(self, param_file)
    def test_put_workflow(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        result = workflow().put_workflow('unittests/resources/hello-workflow.yml')
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    # test set workflow param success
    def test_set_workflow_param_success(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        result = workflow().set_workflow_param('unittests/resources/cutfasta_v1_parameters.yml', 'cutfasta', 1)
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    # test set workflow param failed
    def test_set_workflow_param_failed(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        # invalid version
        with self.assertRaises(ValueError) as cm:
            result = workflow().set_workflow_param('unittests/resources/cutfasta_v1_parameters.yml', 'cutfasta', 'asdkjfl')
        self.assertEquals(str(cm.exception), 'Invalid workflow version! Expect interger greater than 0, but got asdkjfl')

        with self.assertRaises(TypeError) as cm:
            result = workflow().set_workflow_param('unittests/resources/cutfasta_v1_parameters.yml', 'TestWorkflow')

        # invalid name
        with self.assertRaises(ValueError) as cm:
            result = workflow().set_workflow_param('unittests/resources/cutfasta_v1_parameters.yml', 1, 1)
        self.assertEquals(str(cm.exception), 'Invalid workflow name! Expect a string started with alphabet and under 128 characters, but got 1!')

        with self.assertRaises(TypeError) as cm:
            result = workflow().set_workflow_param('unittests/resources/cutfasta_v1_parameters.yml', 1)


if __name__ == '__main__':
    unittest.main()
