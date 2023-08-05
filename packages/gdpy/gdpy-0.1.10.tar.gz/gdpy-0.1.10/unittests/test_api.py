from gdpy.api import Tasks
from gdpy import auth
import unittest
import mock
import requests
import json
from gdpy.http import Response
import platform


class TestAPI(unittest.TestCase):

    def setUp(self):
        pass

    @mock.patch("gdpy.api.Tasks._do")
    def test_create_task(self, mock_do):
        response = requests.Response()
        response.status_code = 200

        python_version = platform.python_version_tuple()
        if python_version[0] == "2":
            response._content = json.dumps({"task_id": "task_id", "task_name": "task_name"})
        else:
            response._content = bytes(json.dumps({"task_id": "task_id", "task_name": "task_name"}), encoding='utf-8')
        mock_do.return_value = Response(response)

        res_account_name = "res_account_name"
        endpoint = "http://endpoint/"
        project = "defalut"
        task_type = "wdl"
        task = Tasks(
            auth=auth.GeneDockAuth(access_key_id='access_key_id', access_key_secret='access_key_secret'),
            res_account_name=res_account_name,
            endpoint=endpoint,
            project_name=project,
            task_type=task_type
        )

        workflow_id = "workflow_id"
        workflow_version = "wf_version"
        inputs = {}
        remote_output_dir = "remote_output_dir"
        task_name = None
        keep_output_structure = False
        result = task.create_task(
            workflow_id, workflow_version,
            parameters={
                "inputs": inputs,
                "output_dir": remote_output_dir,
                "name": task_name,
                "keep_output_structure": keep_output_structure
            }
        )
        self.assertEqual(mock_do.call_args[1]["data"]["keep_output_structure"], keep_output_structure)
        self.assertEqual(result.status, 200)
        self.assertEqual(result.task_id, "task_id")
        self.assertEqual(result.task_name, "task_name")

        # test default keep_output_structure param
        result = task.create_task(
            workflow_id, workflow_version,
            parameters={
                "inputs": inputs,
                "output_dir": remote_output_dir,
                "name": task_name,
            }
        )

        self.assertEqual(mock_do.call_args[1]["data"]["keep_output_structure"], True)
        self.assertEqual(result.status, 200)
        self.assertEqual(result.task_id, "task_id")
        self.assertEqual(result.task_name, "task_name")


if __name__ == '__main__':
    unittest.main()
