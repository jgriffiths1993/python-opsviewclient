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


class Collector(base.Resource):

    # Map our API names to the Opsview API names
    _field_map_ = {
        "monitoring_cluster": "monitoringcluster",
    }

    # Map the types we use to the API types used by Opsview to prevent using
    # stringy booleans and integers
    _fields_ = {
        "id": FT.INT_STR,
        "name": FT.STR,
        "host": FT.REF,
        "collector_ref": FT.STR,
        "last_heartbeat": FT.INT_STR,
        "hostname": FT.STR,
        "ip": FT.STR,
        "os": FT.STR,
        "version": FT.STR,
        "status": FT.STR,
        "monitoringcluster": FT.REF,
        "has_single_node_cluster": FT.BOOL_INT_STR,
    }

    # Specify which fields should be ommitted and cannot be updated/created
    _field_attributes_ = {
        "id": FA.READONLY,
        "host": FA.READONLY,
        "collector_ref": FA.READONLY,
        "last_heartbeat": FA.READONLY,
        "hostname": FA.READONLY,
        "ip": FA.READONLY,
        "os": FA.READONLY,
        "version": FA.READONLY,
        "status": FA.READONLY,
        "monitoringcluster": FA.READONLY,
        "has_single_node_cluster": FA.READONLY,
    }

    @property
    def monitoring_cluster(self):
        if not self._info.get('monitoringcluster'):
            return

        if not self.manager:
            return self._info['monitoringcluster']

        mc_id = base.id_from_ref(self._info['monitoringcluster'])
        return self.manager.client.config.monitoringclusters.get(mc_id)

    @property
    def host(self):
        if not self._info.get('host'):
            return

        if not self.manager:
            return self._info['host']

        h_id = base.id_from_ref(self._info['host'])
        return self.manager.client.config.hosts.get(h_id)

    def __repr__(self):
        return '<Collector: %s>' % self.name


class CollectorManager(base.Manager):

    resource_class = Collector

    def get(self, collector):
        return self._get('/config/collector/%s' % base.get_id(collector))

    def update(self, collector, force=False, params=None, body_only=None,
               **kwds):

        if kwds is None:
            return

        # Replace the kwds with the appropriate names used by the Opsview API.
        for (k, v) in six.iteritems(self.resource_class._field_map_):
            if k in kwds:
                kwds[v] = kwds[k]
                del kwds[k]

        new_coll = collector.copy()
        new_coll._info.update(kwds)
        new_coll = new_coll.encoded()

        if not force:
            old_coll = collector.encoded()

            if old_coll == new_coll:
                return

        body = new_coll

        if body_only:
            return body

        return self._update('/config/collector/%s' % base.get_id(collector),
                            body=body, params=params)

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

        return self._list('/config/collector%s' % qstring)
