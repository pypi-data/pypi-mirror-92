# -*- coding: utf-8 -*-

from __future__ import absolute_import
import unittest

from requests import Request
import time
import mock

from gdpy import auth, compat


class TestGeneDockAuth(unittest.TestCase):

    def setUp(self):
        self._auth = auth.GeneDockAuth(access_key_id='access_key_id', access_key_secret='access_key_secret')

        self.patcher = mock.patch('gdpy.auth.time.gmtime')
        mock_time = self.patcher.start()
        mock_time.return_value = time.struct_time([2018, 12, 19, 9, 39, 55, 2, 353, 0])

    def tearDown(self):
        self.patcher.stop()

    def test_auth_by_get(self):
        req = Request(
            method='get',
            url='https://cn-beijing-api.genedock.com',
            params={'unittest': True},
            auth=self._auth
        )

        p = req.prepare()
        date = p.headers['date']
        self.assertIsInstance(date, compat.builtin_str)
        self.assertEquals(date, 'Wed, 19 Dec 2018 09:39:55 GMT')

        authorization = p.headers['authorization']
        self.assertIsInstance(authorization, compat.builtin_str)
        self.assertEquals(authorization, 'GeneDock access_key_id:6Wcuf3PXsHiUt2+fTOVXR0IwQf4=')

    def test_auth_by_post(self):
        req = Request(
            method='post',
            url='https://cn-beijing-api.genedock.com',
            data={'unittest': True},
            auth=self._auth
        )

        p = req.prepare()

        date = p.headers['date']
        self.assertIsInstance(date, compat.builtin_str)
        self.assertEquals(date, 'Wed, 19 Dec 2018 09:39:55 GMT')

        authorization = p.headers['authorization']
        self.assertIsInstance(authorization, compat.builtin_str)
        self.assertEquals(authorization, 'GeneDock access_key_id:aQCUVdlWrOG/gahjp47rTjgCtG8=')


if __name__ == '__main__':
    unittest.main()
