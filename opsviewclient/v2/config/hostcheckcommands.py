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


class HostCheckCommand(base.Resource):
    """
    {
        "args": "-H $HOSTADDRESS$ -t 15 -p 22",
        "hosts": [],
        "id": "18",
        "name": "tcp port 22 (SSH)",
        "plugin": {
            "name": "check_ssh",
            "ref": "/rest/config/plugin/check_ssh"
        },
        "priority": "1",
        "ref": "/rest/config/hostcheckcommand/18",
        "uncommitted": "0"
    }
    """

    _field_map_ = {}

    _fields_ = {
        'id': FT.INT_STR,
        'name': FT.STR,
        'args': FT.STR,
        'plugin': FT.REF,
        'priority': FT.INT_STR,
        'ref': FT.STR,
        'uncommitted': FT.BOOL_INT_STR,
        'hosts': FT.REF_LIST,
    }

    _field_attributes_ = {
        'id': FA.READONLY,
        'args': FA.OMIT_NONE,
        'priority': FA.OMIT_NONE,
        'ref': FA.READONLY,
        'uncommitted': FA.READONLY,
        'hosts': FA.READONLY,
    }

    def __repr__(self):
        return '<HostCheckCommand: %s>' % self.name

    @property
    def hosts(self):
        if not self._info.get('hosts'):
            return

        if not self.manager:
            for host in self._info['hosts']:
                yield host
        else:
            for host in self._info['hosts']:
                host_id = base.id_from_ref(host)
                yield self.manager.client.config.hosts.get(host_id)

    def delete(self):
        return self.manager.delete(self)


class HostCheckCommandManager(base.Manager):

    resource_class = HostCheckCommand

    def get(self, command):
        return self._get('/config/hostcheckcommand/%s' % base.get_id(command))

    def create(self, name, plugin, args=None, priority=None,
               params=None, body_only=None):

        body = {
            'name': name,
            'plugin': base.nameref(plugin),
            'args': args,
            'priority': priority,
        }

        body = self.resource_class._encode(body)
        if body_only:
            return body

        return self._create('/config/hostcheckcommand',
                            body=body, params=params)

    def update(self, host_check_command, force=False, params=None,
               body_only=False, **kwds):

        if kwds is None:
            # Nothing to update
            return

        for (k, v) in six.iteritems(self.resource_class._field_map_):
            if k in kwds:
                kwds[v] = kwds[k]
                del kwds[k]

        try:
            plugin = kwds.pop('plugin')
        except KeyError:
            pass
        else:
            kwds['plugin'] = base.nameref(plugin)

        new_command = host_check_command.copy()
        new_command._info.update(kwds)
        new_command = new_command.encoded()

        if not force:
            # Check if we need to update or not
            old_command = host_check_command.encoded()

            if old_command == new_command:
                return

        body = new_command
        if body_only:
            return body

        return self._update('/config/hostcheckcommand/%s' %
                            base.get_id(host_check_command),
                            body=body, params=params)

    def delete(self, command):
        return self._delete('/config/hostcheckcommand/%s' %
                            base.get_id(command))

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

        return self._list('/config/hostcheckcommand%s' % qstring)
