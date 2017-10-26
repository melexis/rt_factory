#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Integration tests for mission control package
"""

from unittest import TestCase
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

from rt_factory.mission_control import MissionControlApi, OPERATION_TYPES
from rt_factory.support import ApiError


class TestMissionControl(TestCase):

    def setUp(self):
        self.mc = MissionControlApi()

    def tearDown(self):
        pass

    @patch('rt_factory.support.requests.get')
    def test_get_script_list(self, mock_get):

        scripts = {
            'data': [
                {'name': 'virtual-nuget.groovy', 'target': 'REPOSITORY'},
                {'name': 'qa-property-set.groovy', 'target': 'INSTANCE'},
            ]
        }

        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = scripts

        response = self.mc.get_script_list()

        self.assertEqual(response, scripts)

    @patch('rt_factory.support.requests.post')
    def test_list_user_inputs(self, mock_post):

        instance = "localhost:8091/artifactory"
        repository = "maven-local"
        user_inputs = {
            "data": [
                {
                    "success": True,
                    "instanceName": instance,
                    "repositoryKey": repository,
                    "scriptUserInputs": [
                        {
                            "multiple": False,
                            "type": "STRING",
                            "value": "object",
                            "description": "this is input #1",
                            "name": "input1",
                            "id": "1",
                        },
                        {
                            "multiple": True,
                            "type": "INTEGER",
                            "value": "42",
                            "description": "this is input #2",
                            "name": "input2",
                            "id": "2",
                        }
                    ]}
            ]
        }

        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.json.return_value = user_inputs

        response = self.mc.list_user_inputs(['script1', 'script2'], OPERATION_TYPES[0])

        self.assertEqual(response, user_inputs)

    def test_list_user_inputs_invalid_operation(self):

        with self.assertRaises(ApiError):
            self.mc.list_user_inputs([], 'NON_EXISTING_OPERATION')
