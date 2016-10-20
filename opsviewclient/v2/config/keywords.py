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


class Keyword(base.Resource):
    """
    {
        "all_hosts": "1",
        "all_servicechecks": "0",
        "description": "Ton",
        "enabled": "1",
        "exclude_handled": "0",
        "hosts": [
            {
                "name": "bob",
                "ref": "/rest/config/host/63"
            }
        ],
        "id": "92",
        "name": "Alex",
        "public": "1",
        "ref": "/rest/config/keyword/92",
        "roles": [],
        "servicechecks": [
            {
                "name": "Check Loadavg",
                "ref": "/rest/config/servicecheck/44"
            }
        ],
        "show_contextual_menus": "0",
        "style": "group_by_host",
        "uncommitted": "0"
    }
    """

    _field_map_ = {
        'service_checks': 'servicechecks'
    }

    _fields_ = {
        'all_hosts': FT.BOOL_INT_STR,
        'all_servicechecks': FT.BOOL_INT_STR,
        'description': FT.STR,
        'enabled': FT.BOOL_INT_STR,
        'exclude_handled': FT.BOOL_INT_STR,
        'hosts': FT.REF_LIST,
        'id': FT.INT_STR,
        'name': FT.STR,
        'public': FT.BOOL_INT_STR,
        'ref': FT.STR,
        'roles': FT.REF_LIST,
        'servicechecks': FT.REF_LIST,
        'show_contextual_menus': FT.BOOL_INT_STR,
        'style': FT.STR,
        'uncommitted': FT.BOOL_INT_STR,
    }

    _field_attributes_ = {
        'all_hosts': FA.OMIT_NONE,
        'all_servicechecks': FA.OMIT_NONE,
        'description': FA.OMIT_NONE,
        'enabled': FA.OMIT_NONE,
        'exclude_handled': FA.OMIT_NONE,
        'hosts': FA.OMIT_NONE,
        'id': FA.READONLY,
        'public': FA.OMIT_NONE,
        'ref': FA.READONLY,
        'roles': FA.OMIT_NONE,
        'servicechecks': FA.OMIT_NONE,
        'show_contextual_menus': FA.OMIT_NONE,
        'style': FA.OMIT_NONE,
        'uncommitted': FA.READONLY,
    }

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
    def service_checks(self):
        if not self._info.get('servicechecks'):
            return

        if not self.manager:
            for sc in self._info['servicechecks']:
                yield sc
        else:
            for sc in self._info['servicechecks']:
                sc_id = base.id_from_ref(sc)
                yield self.manager.client.config.servicechecks.get(sc_id)

    def __repr__(self):
        return '<Keyword: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class KeywordManager(base.Manager):

    resource_class = Keyword

    def get(self, keyword):
        return self._get('/config/keyword/%s' % base.get_id(keyword))

    def create(self, name, all_hosts=None, all_servicechecks=None,
               description=None, enabled=True, exclude_handled=None,
               hosts=None, public=None, roles=None, service_checks=None,
               show_contextual_menus=None, style=None,
               params=None, body_only=False):

        body = {
            'name': name,
            'all_hosts': all_hosts,
            'all_servicechecks': all_servicechecks,
            'description': description,
            'enabled': enabled,
            'exclude_handled': exclude_handled,
            'hosts': ([base.nameref(h) for h in hosts]
                      if isinstance(hosts, list)
                      else [base.nameref(hosts)]),
            'public': public,
            'roles': ([base.nameref(r) for r in roles]
                      if isinstance(roles, list)
                      else [base.nameref(roles)]),
            'servicechecks': ([base.nameref(s) for s in service_checks]
                              if isinstance(service_checks, list)
                              else [base.nameref(service_checks)]),
            'show_contextual_menus': show_contextual_menus,
            'style': style,
        }

        body = self.resource_class._encode(body)
        if body_only:
            return body

        return self._create('/config/keyword', body=body, params=params)

    def update(self, keyword, force=False, params=None, body_only=False,
               **kwds):

        if not kwds:
            return

        for (k, v) in six.iteritems(self.resource_class._field_map_):
            if k in kwds:
                kwds[v] = kwds[k]
                del kwds[k]

        if 'hosts' in kwds:
            kwds['hosts'] = (
                [base.nameref(h) for h in kwds['hosts']]
                if isinstance(kwds['hosts'], list)
                else [base.nameref(kwds['hosts'])]
            )

        if 'roles' in kwds:
            kwds['roles'] = (
                [base.nameref(h) for h in kwds['roles']]
                if isinstance(kwds['roles'], list)
                else [base.nameref(kwds['roles'])]
            )

        if 'servicechecks' in kwds:
            kwds['servicechecks'] = (
                [base.nameref(h) for h in kwds['servicechecks']]
                if isinstance(kwds['servicechecks'], list)
                else [base.nameref(kwds['servicechecks'])]
            )

        new_kw = keyword.copy()
        new_kw._info.update(kwds)
        new_kw = new_kw.encode()

        if not force:
            old_kw = keyword.encode()
            if old_kw == new_kw:
                return

        body = new_kw
        if body_only:
            return body

        return self._update('/config/keyword/%s' % base.get_id(keyword),
                            params=params, body=body)

    def delete(self, keyword):
        return self._delete('/config/keyword/%s' % base.get_id(keyword))

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

        return self._list('/config/keyword%s' % qstring)
