# -*- coding: utf-8 -*-
from .support import AbstractApi, ApiError
import os

MISSION_CONTROL_URL = os.getenv("MISSION_CONTROL_URL", "http://localhost:8080/missioncontrol/api/v2")
MISSION_CONTROL_USER = os.getenv("MISSION_CONTROL_USER", "admin")
MISSION_CONTROL_PASS = os.getenv("MISSION_CONTROL_PASS", "password")

OPERATION_TYPES = ["CREATE_REPOSITORY", "UPDATE_REPOSITORY", "UPDATE_INSTANCE"]


class MissionControlApi(AbstractApi):

    def __init__(self, url=MISSION_CONTROL_URL, user=MISSION_CONTROL_USER, pwd=MISSION_CONTROL_PASS):
        super().__init__(url=url, user=user, pwd=pwd)

    #
    #  script resources
    #

    def get_script_list(self):
        return self._get("scripts")

    def list_user_inputs(self, script_mappings=[], op_type="*invalid*" ):
        if op_type not in OPERATION_TYPES:
            raise ApiError("Invalid operation type passed to list_user_input : {}".format(op_type))

        data = {"scriptMappings": script_mappings, "operationType": op_type}
        return self._post("scripts/user_inputs", data).json()

    #
    #  instance resources
    #

    def get_instances(self):
        return self._get("instances")

    def add_instance(self, name="", description="", url="", username="", password="",location=""):
        data = {
            "name": name,
            "description": description,
            "url": url,
            "username": username,
            "password": password,
            "location": location,
        }
        return self._post("instances", data)

    def update_instance(self, name="", description="", url="", username="", password="",location=""):
        data = {
            "description": description,
            "url": url,
            "username": username,
            "password": password,
            "location": location,
        }
        return self.put("instances/{}".format(name), data)

    def delete_instance(self, name=""):
        return self._delete("instances/{}".format(name))

    def execute_scripts(self, instance_name="", script_names=[]):
        data = {
            "scriptMappings": [{
                "instanceName": instance_name,
                "scriptNames": script_names,
            }]
        }
        return self._put("execute_scripts/instances", data)

    def get_all_instances_status(self):
        return self._get("instances/monitoring/status")

    def get_instance_status(self, instance_name=""):
        return self._get("instances/{}/monitoring/status".format(instance_name))

    #
    # repositories resource
    #
    def get_repositories(self, instance_name=""):
        return self._get("instances/{}/repositories".format(instance_name))

    def create_repository(self, instance_name="", script_names=[], script_user_inputs = {}):
        data = {
            "scriptMappings": [{
                "instanceName": instance_name,
                "scriptNames": script_names,
                "scriptUserInputs": script_user_inputs,
            }],
        }
        return self._post("execute_scripts/repositories", data)

    def update_repository(self, instance_name="", repository_key=""
                          , script_names=[], script_user_inputs={}):
        data = {
            "scriptMappings": [{
                "instanceName": instance_name,
                "repositoryKey": repository_key,
                "scriptNames": script_names,
                "scriptUserInputs": script_user_inputs,
            }],
        }
        return self._put("execute_scripts/repositories", data)

    #
    # security resource
    #

    def create_user(self, instance_names=[], name="", email="", password=""
                    , is_admin=False
                    , is_profile_updatable=False
                    , is_internal_password_disabled=False):
        data = {
            "instanceNames": instance_names,
            "user": {
                "name": name,
                "email": email,
                "password": password,
                "admin": is_admin,
                "profileUpdatable": is_profile_updatable,
                "internalPasswordDisabled": is_internal_password_disabled,
            }
        }
        return self._post("security/users", data)

    def update_user(self, instance_names=[], name="", email="", password=""
                    , is_admin=False
                    , is_profile_updatable=False
                    , is_internal_password_disabled=False):
        data = {
            "instanceNames": instance_names,
            "user": {
                "email": email,
                "password": password,
                "admin": is_admin,
                "profileUpdatable": is_profile_updatable,
                "internalPasswordDisabled": is_internal_password_disabled,
            }
        }
        return self._post("security/users/{}".format(name), data)


    def create_user_group(self, instance_names=[],
                          name="", description="", auto_join=False,
                          users=[]):
        data = {
            "instanceNames": instance_names,
            "userGroup": {
                "name": name,
                "description": description,
                "autoJoin": auto_join,
                "users": users,
            }
        }
        return self._post("security/user_groups", data)

    def update_user_group(self, instance_names=[],
                          name="", description="", auto_join=False,
                          users=[]):
        data = {
            "instanceNames": instance_names,
            "userGroup": {
                "description": description,
                "autoJoin": auto_join,
                "users": users,
            }
        }
        return self._post("security/user_groups/{}".format(name), data)

    def create_permission_target(self, instance_names=[],
                                 name="", repositories=[],
                                 any_remote=False, any_local=False,
                                 excludes_pattern="", includes_pattern="",
                                 users={}, groups={}):
        data = {
            "instanceNames" : instance_names,
            "permissionTarget" : {
                "name" : name,
                "repositories" : repositories,
                "anyRemote" : any_remote,
                "anyLocal" : any_local,
                "excludesPattern": excludes_pattern,
                "includesPattern" : includes_pattern,
                "principals": {
                    "users" : users,
                    "groups" : groups,
                }
            }
        }
        return self._post("security/permission_targets")

    def update_permission_target(self, instance_names=[],
                                 name="", repositories=[],
                                 any_remote=False, any_local=False,
                                 excludes_pattern="", includes_pattern="",
                                 users={}, groups={}):
        data = {
            "instanceNames" : instance_names,
            "permissionTarget" : {
                "repositories" : repositories,
                "anyRemote" : any_remote,
                "anyLocal" : any_local,
                "excludesPattern": excludes_pattern,
                "includesPattern" : includes_pattern,
                "principals": {
                    "users" : users,
                    "groups" : groups,
                }
            }
        }
        return self._put("security/permission_targets/{}".format(name))

    #
    # license bucket resource
    #

    def get_bucket_status(self, bucket_name=""):
        return self._get("buckets/{}/report".format(bucket_name))

    def attach_license(self, bucket_name="", instance_name="", deploy=True, number_of_licenses=1):
        data = {
            "instanceName" : instance_name,
            "deploy" : deploy,
            "numberOfLicenses" : number_of_licenses,
        }
        return self._post("attach_lic/buckets/{}".format(bucket_name), data)

    def detach_license(self, bucket_name="", instance_name=""):
        data = {
            "instanceName": instance_name
        }
        return self._delete("attach_/lic/buckets/{}".format(bucket_name), data)

    #
    # disaster recovery resource
    #
    def create_dr_pair(self, master="", target=""):
        data = {
            "source": master,
            "target": target,
        }
        return self._post("dr-configs",data)
