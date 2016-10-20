#!/usr/bin/env python
# coding: utf-8

import six
from six.moves.urllib import parse

try:
    import simplejson as json
except ImportError:
    import json

from opsviewclient import base
from opsviewclient.fields import (
    FieldTypes as FT,
    FieldAttributes as FA
)


class ServiceGroup(base.Resource):
    """
    {
        "id": "137",
        "name": "AAA-Polling",
        "ref": "/rest/config/servicegroup/137",
        "servicechecks": [
            {
                "name": "58582852",
                "ref": "/rest/config/servicecheck/1028"
            },
            {
                "name": "Apache Server Status",
                "ref": "/rest/config/servicecheck/895"
            },
            {
                "name": "check_basic_load",
                "ref": "/rest/config/servicecheck/1018"
            },
            {
                "name": "check_period_test",
                "ref": "/rest/config/servicecheck/923"
            },
            {
                "name": "check_period_test testbomb",
                "ref": "/rest/config/servicecheck/1025"
            },
            {
                "name": "check_period_test testbomb2",
                "ref": "/rest/config/servicecheck/1026"
            },
            {
                "name": "check_vmware_api_test",
                "ref": "/rest/config/servicecheck/1011"
            },
            {
                "name": "duncs test",
                "ref": "/rest/config/servicecheck/1035"
            },
            {
                "name": "fortesting",
                "ref": "/rest/config/servicecheck/919"
            },
            {
                "name": "ov203-polling",
                "ref": "/rest/config/servicecheck/806"
            },
            {
                "name": "SNMP_COMMTEST",
                "ref": "/rest/config/servicecheck/887"
            },
            {
                "name": "SNMP_Polling_test_hp",
                "ref": "/rest/config/servicecheck/846"
            },
            {
                "name": "tester",
                "ref": "/rest/config/servicecheck/888"
            },
            {
                "name": "Testertrap",
                "ref": "/rest/config/servicecheck/914"
            },
            {
                "name": "traptest",
                "ref": "/rest/config/servicecheck/889"
            }
        ],
        "uncommitted": "0"
    }
    """

    def __repr__(self):
        return '<ServiceGroup: %s>' % self.name

    def update(self, **kwds):
        return self.manager.update(self, **kwds)

    def delete(self):
        return self.manager.delete(self)


class ServiceGroupManager(base.Manager):

    resource_class = ServiceGroup

    def get(self, group):
        return self._get('/config/servicegroup/%s' % base.get_id(group))

    def update(self, group, **kwds):
        body = group._info
        body.update(kwds)
        return self._update('/config/servicegroup/%s' % base.get_id(group),
                            body=body)

    def create(self, name, servicechecks=None):
        body = {'name': name}

        if servicechecks is not None:
            if not isinstance(servicechecks, list):
                servicechecks = [servicechecks]

            body['servicechecks'] = [base.nameref(s) for s in servicechecks]

        return self._create('/config/servicegroup', body=body)

    def delete(self, group):
        return self._delete('/config/servicegroup/%s' % base.get_id(group))

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/servicegroup%s' % qstring)
