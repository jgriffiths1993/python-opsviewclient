#!/usr/bin/env python
# coding: utf-8

import requests

try:
    import simplejson as json
except ImportError:
    import json

from opsviewclient import exceptions as exc
from opsviewclient.v2.config import Client as ConfigClient


class Client(object):

    _default_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    def __init__(self, endpoint, username=None, password=None, token=None):
        if endpoint[-1] == '/':
            self.base_url = endpoint
        else:
            self.base_url = endpoint + '/'

        if not (username and (token or password)):
            raise exc.OpsviewClientException('Must specify username and either '
                                             'token or password')

        self.token = token
        self._username = username
        self._password = password

        self._session = requests.Session()
        self._session.headers = Client._default_headers

        self.config = ConfigClient(self)

        self._authenticate()

    def _authenticate(self):
        # Clear the authenticated headers
        self._session.headers.pop('X-Opsview-Username', None)
        self._session.headers.pop('X-Opsview-Token', None)

        if self._username and self._password:
            payload = {
                'username': self._username,
                'password': self._password,
            }
            response = self._request('POST', 'login', data=payload)

            try:
                token = response['token']
            except Exception as e:
                raise e

            self.token = token

        self._session.headers['X-Opsview-Username'] = self._username
        self._session.headers['X-Opsview-Token'] = self.token

    def _url(self, path):
        if path[0] == '/':
            path = path[1:]

        return self.base_url + path

    def _request(self, method, path, data=None, params=None, expected=[200]):

        if data is not None:
            data = json.dumps(data)

        response = self._session.request(method=method, url=self._url(path),
                                         data=data, params=params)

        if response.status_code not in expected:
            raise exc.OpsviewClientException('Unexpected response: ',
                                             response.text)

        return response.json()

    def get(self, url, **kwds):
        return self._request('GET', url, **kwds)

    def post(self, url, **kwds):
        return self._request('POST', url, **kwds)

    def put(self, url, **kwds):
        return self._request('PUT', url, **kwds)

    def delete(self, url, **kwds):
        return self._request('DELETE', url, **kwds)

    def reload(self, asynchronous=False):
        params = {}
        if asynchronous:
            params['asynchronous'] = 1

        return self.post('/reload', params=params)

    def reload_status(self):
        return self.get('/reload')

    def info(self):
        return self.get('/info')
