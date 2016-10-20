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


class Tenancy(base.Resource):
    """
    {
        "description": "Customer: Google.com users",
        "id": "1",
        "name": "Google.com",
        "primary_role": {
            "name": "Google",
            "ref": "/rest/config/role/53"
        },
        "priority": "0",
        "ref": "/rest/config/tenancy/1"
    }
    """

    @property
    def primary_role(self):
        if not self._info.get('primary_role'):
            return

        if not self.manager:
            return self._info['primary_role']

        pr_id = base.id_from_ref(self._info['primary_role'])
        return self.manager.client.config.roles.get(pr_id)

    def __repr__(self):
        return '<Tenancy: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class TenancyManager(base.Manager):

    resource_class = Tenancy

    def get(self, tenancy):
        return self._get('/config/tenancy/%s' % base.get_id(tenancy))

    def delete(self, tenancy):
        return self._delete('/config/tenancy/%s' % base.get_id(tenancy))

    # def create(self, name, description=None, )

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

        return self._list('/config/tenancy%s' % qstring)
