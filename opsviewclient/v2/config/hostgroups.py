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


class HostGroup(base.Resource):
    """
    {
        "id": "172",
        "children": [],
        "hosts": [
            {
                "name": "10.0.2.200",
                "ref": "/rest/config/host/494"
            },
            {
                "name": "ba",
                "ref": "/rest/config/host/503"
            }
        ],
        "is_leaf": "1",
        "matpath": "Opsview,brian,anotherplaceholder,",
        "name": "anotherplaceholder",
        "parent": {
            "matpath": "Opsview,brian,",
            "name": "brian",
            "ref": "/rest/config/hostgroup/170"
        },
        "ref": "/rest/config/hostgroup/172",
        "uncommitted": "0"
    }
    """

    _field_map_ = {}

    _fields_ = {
        'id': FT.INT_STR,
        'children': FT.REF_LIST,
        'hosts': FT.REF_LIST,
        'is_leaf': FT.BOOL_INT_STR,
        'matpath': FT.STR,
        'parent': FT.REF,
        'ref': FT.STR,
        'uncommitted': FT.BOOL_INT_STR,
    }

    _field_attributes_ = {
        'id': FA.READONLY,
        'children': FA.READONLY,
        'hosts': FA.OMIT_NONE,
        'is_leaf': FA.READONLY,
        'matpath': FA.READONLY,
        'parent': FA.OMIT_NONE,
        'ref': FA.READONLY,
        'uncommitted': FA.READONLY,
    }

    def __repr__(self):
        return '<HostGroup: %s>' % self.name

    @property
    def children(self):
        if not self._info.get('children'):
            return

        if not self.manager:
            for hg in self._info['children']:
                yield hg
        else:
            for hg in self._info['children']:
                hg_id = base.id_from_ref(hg)
                yield self.manager.client.config.hostgroups.get(hg_id)

    @property
    def hosts(self):
        if not self._info.get('hosts'):
            return

        if not self.manager:
            for h in self._info['hosts']:
                yield h
        else:
            for h in self._info['hosts']:
                h_id = base.id_from_ref(h)
                yield self.manager.client.config.hosts.get(h_id)

    @property
    def parent(self):
        if not self._info.get('parent'):
            return

        if not self.manager:
            return self._info['parent']

        hg_id = base.id_from_ref(self._info['parent'])
        return self.manager.client.config.hostgroups.get(hg_id)

    def delete(self):
        return self.manager.delete(self)


class HostGroupManager(base.Manager):

    resource_class = HostGroup

    def get(self, group):
        return self._get('/config/hostgroup/%s' % base.get_id(group))

    def create(self, name, parent=None, hosts=None,
               params=None, body_only=False):

        body = {
            'name': name,
            'parent': base.nameref(parent),
        }

        if hosts:
            if not isinstance(hosts, list):
                hosts = [hosts]

            body['hosts'] = [base.nameref(h) for h in hosts]

        body = self.resource_class._encode(body)

        if body_only:
            return body

        return self._create('/config/hostgroup', body=body, params=params)

    def update(self, host_group, force=False, params=None, body_only=None,
               **kwds):

        if kwds is None:
            # Nothing to update
            return

        # Replace keyword arguments with opsview api names
        for (k, v) in six.iteritems(self.resource_class._field_map_):
            if k in kwds:
                kwds[v] = kwds[k]
                del kwds[k]

        if 'parent' in kwds:
            kwds['parent'] = base.nameref('parent')

        if 'hosts' in kwds:
            kwds['hosts'] = (
                [base.nameref(h) for h in kwds['hosts']]
                if isinstance(kwds['hosts'], list)
                else [base.nameref(kwds['hosts'])]
            )

        new_hg = host_group.copy()
        new_hg._info.update(kwds)
        new_hg = new_hg.encoded()

        if not force:
            old_hg = hg.encoded()

            if old_hg == new_hg:
                return

        body = new_hg
        if body_only:
            return body

        return self._update('/config/hostgroup/%s' % base.get_id(host_group),
                            body=body, params=params)

    def delete(self, group):
        return self._delete('/config/hostgroup/%s' % base.get_id(group))

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

        return self._list('/config/hostgroup%s' % qstring)
