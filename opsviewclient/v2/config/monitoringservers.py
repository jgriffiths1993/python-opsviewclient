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


class MonitoringServer(base.Resource):

    _field_map_ = {}

    _fields_ = {
        'activated': FT.BOOL_INT_STR,
        'id': FT.INT_STR,
        'monitors': FT.REF_LIST,
        'name': FT.STR,
        'nodes': FT.NONE,
        'passive': FT.BOOL_INT_STR,
        'ref': FT.STR,
        'roles': FT.REF_LIST,
        'ssh_forward': FT.BOOL_INT_STR,
        'uncommitted': FT.BOOL_INT_STR,
    }

    _field_attributes_ = {
        'activated': FA.OMIT_NONE,
        'id': FA.READONLY,
        'monitors': FA.OMIT_NONE,
        'passive': FA.OMIT_NONE,
        'ref': FA.READONLY,
        'roles': FA.READONLY,
        'ssh_forward': FA.OMIT_NONE,
        'uncommitted': FA.READONLY,
    }

    @property
    def monitors(self):
        pass

    @property
    def nodes(self):
        pass

    def __repr__(self):
        return '<MonitoringServer: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)

    def update(self, **kwds):
        return self.manager.update(self, **kwds)


class MonitoringServerManager(base.Manager):

    resource_class = MonitoringServer

    def get(self, server):
        return self._get('/config/monitoringserver/%s' % base.get_id(server))

    def delete(self, server):
        return self._delete('/config/monitoringserver/%s' % base.get_id(server))

    def create(self, name, nodes, activated=None, passive=None,
               ssh_forward=None, params=None, body_only=False):

        body = {
            'name': name,
            'activated': activated,
            'nodes': ([base.nameref(n) for n in nodes]
                      if isinstance(nodes, list) else
                      [base.nameref(nodes)]),
            'passive': passive,
            'ssh_forward': ssh_forward
        }

        body = self.resource_class._encode(body)
        if body_only:
            return body

        return self._create('/config/monitoringserver',
                            params=params, body=body)

    def update(self, server, force=False, params=None, body_only=None, **kwds):
        if kwds is None:
            return

        for (k, v) in six.iteritems(self.resource_class._field_map_):
            if k in kwds:
                kwds[v] = kwds[k]
                del kwds[k]

        new_server = server.copy()
        new_server._info.update(kwds)

        nodes = new_server._info.get('nodes')
        if nodes and any([n for n in nodes if 'host' in n]):
            tmp_nodes = [n for n in nodes if 'host' not in n]
            tmp_nodes += [n['host'] for n in nodes if 'host' in n]
            new_server._info['nodes'] = tmp_nodes

        new_server = new_server.encoded()

        if not force:
            old_server = server.copy()
            nodes = old_server._info.get('nodes')

            if nodes and any([n for n in nodes if 'host' in n]):
                old_server._info['nodes'] = [n['host'] for n in nodes]

            old_server = old_server.encoded()

            if old_server == new_server:
                return

        body = new_server

        if body_only:
            return body

        return self._update('/config/monitoringserver/%s' % base.get_id(server),
                            params=params, body=body)

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

        return self._list('/config/monitoringserver%s' % qstring)
