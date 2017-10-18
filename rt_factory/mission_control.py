# -*- coding: utf-8 -*-
from rt_factory.support import AbstractApi, ApiError
import os

MISSION_CONTROL_URL = os.getenv("MISSION_CONTROL_URL", "http://localhost:8080/missioncontrol/api/v2")
MISSION_CONTROL_USER = os.getenv("MISSION_CONTROL_USER", "admin")
MISSION_CONTROL_PASS = os.getenv("MISSION_CONTROL_PASS", "password1")

OPERATION_TYPES = ["CREATE_REPOSITORY", "UPDATE_REPOSITORY", "UPDATE_INSTANCE"]

class MissionControlApi(AbstractApi):

    def __init__(self, url=MISSION_CONTROL_URL, user=MISSION_CONTROL_USER, pwd=MISSION_CONTROL_PASS):
        super().__init__(url=url, user=user, pwd=pwd)

    # script resources


    def get_script_list(self):
        return self._get("scripts")

    def list_user_inputs(self, script_mappings=[], op_type="*invalid*" ):
        if op_type not in OPERATION_TYPES:
            raise ApiError("Invalid operation type passed to list_user_input : {}".format(op_type))

        data = {"scriptMappings": script_mappings, "operationType": op_type}
        return self._post("scripts/user_inputs", data).json()


    # instance resources

    def get_instances(self):
        return self._get("instances")
