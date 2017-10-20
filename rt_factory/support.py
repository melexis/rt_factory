# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth


class ApiError(Exception):
    pass


class AbstractApi(object):
    def __init__(self, url="", user=None, pwd=None):
        self.url = url
        self.api_key_header = None
        self.auth=HTTPBasicAuth(user, pwd)

    def _get_from_url(self, full_url):
        resp = requests.get(full_url, headers=self.api_key_header, auth=self.auth)
        if not resp.ok:
            # This means something went wrong.
            raise ApiError('GET {} {}'.format(full_url, resp.status_code))
        return resp.json()

    def _get(self, path):
        return self._get_from_url(self.url + path)

    def _post(self, path, payload):
        resp = requests.post(self.url + path, json=payload, headers=self.api_key_header, auth=self.auth)
        if not resp.ok:
            # This means something went wrong.
            raise ApiError('POST {} {} {}'.format(path, resp.status_code, resp.content))
        return resp

    def _put(self, path, payload=None):
        resp = requests.put(self.url + path, json=payload, headers=self.api_key_header, auth=self.auth)
        if not resp.ok:
            # This means something went wrong.
            raise ApiError('PUT {} {} {}'.format(path, resp.status_code, resp.content))
        return resp

    def _put_file(self, path, filename, **kwargs):
        with open(filename, "rb") as file:
            resp = requests.put(self.url + path, data=file, auth=self.auth, **kwargs)
            if not resp.ok:
                # This means something went wrong.
                raise ApiError('PUT {} {} {}'.format(path, resp.status_code, resp.content))
        return resp

    def _delete(self, path, payload):
        resp = requests.delete(self.url + path, json=payload, headers=self.api_key_header, auth=self.auth)
        if not resp.ok:
            # This means something went wrong.
            raise ApiError('DELETE {} {} {}'.format(path, resp.status_code, resp.content))
        return resp
