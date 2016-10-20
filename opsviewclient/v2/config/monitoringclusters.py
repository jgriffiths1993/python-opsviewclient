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


class MonitoringCluster(base.Resource):
    _field_map_ = {}

    _fields_ = {
        'id': FT.INT_STR,
        'name': FT.STR,
        'active_host_checks_enabled': FT.BOOL_INT_STR,
        'active_service_checks_enabled': FT.BOOL_INT_STR,
        'collectors': FT.REF_LIST,
        'event_handlers_enabled': FT.BOOL_INT_STR,
        'monitors': FT.REF_LIST,
        'passive': FT.BOOL_INT_STR,
        'ref': FT.STR,
        'roles': FT.REF_LIST,
        'uncommitted': FT.BOOL_INT_STR,
    }

    _field_attributes_ = {
        'id': FA.READONLY,
        'active_host_checks_enabled': FA.OMIT_NONE,
        'active_service_checks_enabled': FA.OMIT_NONE,
        'collectors': FA.OMIT_NONE,
        'event_handlers_enabled': FA.OMIT_NONE,
        'monitors': FA.READONLY,
        'passive': FA.OMIT_NONE,
        'ref': FA.READONLY,
        'roles': FA.READONLY,
        'uncommitted': FA.READONLY,
    }

    def __repr__(self):
        return '<MonitoringCluster: %s>' % self.name

    @property
    def collectors(self):
        if not self._info.get('collectors'):
            return

        if not self.manager:
            for c in self._info['collectors']:
                yield c
        else:
            for c in self._info['collectors']:
                c_id = base.id_from_ref(hg)
                yield self.manager.client.config.collectors.get(hg_id)

    @property
    def monitors(self):
        if not self._info.get('monitors'):
            return

        if not self.manager:
            for m in self._info['monitors']:
                yield m

        else:
            for m in self._info['monitors']:
                m_id = base.id_from_ref(m)
                yield self.manager.client.config.hosts.get(m_id)

    @property
    def roles(self):
        if not self._info.get('roles'):
            return

        if not self.manager:
            for r in self._info['roles']:
                yield r

        else:
            for r in self._info['roles']:
                r_id = base.id_from_ref(r)
                yield self.manager.client.config.roles.get(r_id)

    def delete(self):
        return self.manager.delete(self)


class MonitoringClusterManager(base.Manager):

    resource_class = MonitoringCluster

    def get(self, cluster):
        return self._get('/config/monitoringcluster/%s' % base.get_id(cluster))

    def create(self, name, collectors, active_host_checks_enabled=None,
               active_service_checks_enabled=None, event_handlers_enabled=None,
               passive=None, params=None, body_only=False):

        body = {
            'name': name,
            'collectors': (
                [base.nameref(c) for c in collectors]
                if isinstance(collectors, list) else
                [base.nameref(collectors)]
            ),
            'active_host_checks_enabled': active_host_checks_enabled,
            'active_service_checks_enabled': active_service_checks_enabled,
            'event_handlers_enabled': event_handlers_enabled,
            'passive': passive
        }

        body = self.resource_class._encode(body)

        if body_only:
            return body

        return self._create('/config/monitoringcluster',
                            body=body, params=params)

    def update(self, cluster, force=False, params=None, body_only=None,
               **kwds):

        if kwds is None:
            return

        for (k, v) in six.iteritems(self.resource_class._field_map_):
            if k in kwds:
                kwds[v] = kwds[k]
                del kwds[k]

        if 'collectors' in kwds:
            kwds['collectors'] = (
                [base.nameref(c) for c in kwds['collectors']]
                if isinstance(kwds['collectors'], list) else
                [base.nameref(kwds['collectors'])]
            )

        new_mc = cluster.copy()
        new_mc._info.update(kwds)
        new_mc = new_mc.encoded()

        if not force:
            old_mc = cluster.encoded()

            if old_mc == new_mc:
                return

        body = new_mc
        if body_only:
            return body

        return self._update('/config/monitoringcluster/%s' %
                            base.get_id(cluster), body=body, params=params)

    def delete(self, cluster):
        return self._delete('/config/monitoringcluster/%s' %
                            base.get_id(cluster))

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

        return self._list('/config/monitoringcluster%s' % qstring)
