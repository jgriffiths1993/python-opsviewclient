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


class Role(base.Resource):
    """
    {
        "access_hostgroups": [],
        "access_keywords": [],
        "access_servicegroups": [],
        "accesses": [
            {
                "name": "VIEWPORTACCESS",
                "ref": "/rest/config/access/10"
            }
        ],
        "all_bsm_components": "0",
        "all_bsm_edit": "0",
        "all_bsm_view": "0",
        "all_hostgroups": "0",
        "all_keywords": "0",
        "all_monitoringservers": "0",
        "all_servicegroups": "0",
        "contacts": [],
        "description": "Access available for public users",
        "hostgroups": [],
        "id": "1",
        "monitoringservers": [],
        "name": "Public",
        "ref": "/rest/config/role/1",
        "tenancy": null,
        "uncommitted": "0"
    }
    """

    _field_map_ = {
        'host_groups': 'access_hostgroups',
        'keywords': 'access_keywords',
        'service_groups': 'access_servicegroups',
        'permissions': 'accesses',
        'all_host_groups': 'all_hostgroups',
        'all_monitoring_servers': 'all_monitoringservers',
        'all_service_groups': 'all_servicegroups',
        'monitoring_servers': 'monitoringservers',
    }

    _fields_ = {
        "access_hostgroups": FT.REF_LIST,
        "access_keywords": FT.REF_LIST,
        "access_servicegroups": FT.REF_LIST,
        "accesses": FT.REF_LIST,
        "all_bsm_components": FT.BOOL_INT_STR,
        "all_bsm_edit": FT.BOOL_INT_STR,
        "all_bsm_view": FT.BOOL_INT_STR,
        "all_hostgroups": FT.BOOL_INT_STR,
        "all_keywords": FT.BOOL_INT_STR,
        "all_monitoringservers": FT.BOOL_INT_STR,
        "all_servicegroups": FT.BOOL_INT_STR,
        "contacts": FT.REF_LIST,
        "description": FT.STR,
        "hostgroups": FT.REF_LIST,
        "id": FT.INT_STR,
        "monitoringservers": FT.REF_LIST,
        "name": FT.STR,
        "ref": FT.STR,
        "tenancy": FT.REF,
        "uncommitted": FT.BOOL_INT_STR,
    }

    _field_attributes_ = {
        "access_hostgroups": FA.OMIT_NONE,
        "access_keywords": FA.OMIT_NONE,
        "access_servicegroups": FA.OMIT_NONE,
        "accesses": FA.OMIT_NONE,
        "all_bsm_components": FA.OMIT_NONE,
        "all_bsm_edit": FA.OMIT_NONE,
        "all_bsm_view": FA.OMIT_NONE,
        "all_hostgroups": FA.OMIT_NONE,
        "all_keywords": FA.OMIT_NONE,
        "all_monitoringservers": FA.OMIT_NONE,
        "all_servicegroups": FA.OMIT_NONE,
        "contacts": FA.READONLY,
        "description": FA.OMIT_NONE,
        "hostgroups": FA.OMIT_NONE,
        "id": FA.READONLY,
        "monitoringservers": FA.OMIT_NONE,
        "ref": FA.READONLY,
        "tenancy": FA.OMIT_NONE,
        "uncommitted": FA.READONLY,
    }

    @property
    def host_groups(self):
        if not self._info.get('hostgroups'):
            return

        if not self.manager:
            for hg in self._info['hostgroups']:
                yield hg

        else:
            for hg in self._info['hostgroups']:
                hg_id = base.id_from_ref(hg)
                yield self.manager.client.hostgroups.get(hg_id)

    @property
    def keywords(self):
        if not self._info.get('keywords'):
            return

        if not self.manager:
            for kw in self._info['keywords']:
                yield kw

        else:
            for kw in self._info['keywords']:
                kw_id = base.id_from_ref(kw)
                yield self.manager.client.keywords.get(kw_id)

    @property
    def service_groups(self):
        if not self._info.get('servicegroups'):
            return

        if not self.manager:
            for sg in self._info['servicegroups']:
                yield sg

        else:
            for sg in self._info['servicegroups']:
                sg_id = base.id_from_ref(sg)
                yield self.manager.client.servicegroups.get(sg_id)

    @property
    def contacts(self):
        if not self._info.get('contacts'):
            return

        if not self.manager:
            for c in self._info['contacts']:
                yield c

        else:
            for c in self._info['contacts']:
                c_id = base.id_from_ref(sc)
                yield self.manager.client.contacts.get(sc_id)

    @property
    def host_groups(self):
        if not self._info.get('servicegroups'):
            return

        if not self.manager:
            for sg in self._info['servicegroups']:
                yield sg

        else:
            for sg in self._info['servicegroups']:
                sg_id = base.id_from_ref(sg)
                yield self.manager.client.servicegroups.get(sg_id)

    @property
    def monitoring_servers(self):
        if not self._info.get('servicegroups'):
            return

        if not self.manager:
            for sg in self._info['servicegroups']:
                yield sg

        else:
            for sg in self._info['servicegroups']:
                sg_id = base.id_from_ref(sg)
                yield self.manager.client.servicegroups.get(sg_id)

    @property
    def tenancy(self):
        pass

    def __repr__(self):
        return '<Role: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class RoleManager(base.Manager):

    resource_class = Role

    def create(self, name, description=None, permissions=None,
               hostgroups=None, all_hostgroups=False,
               keywords=None, all_keywords=False,
               service_groups=None, all_servicegroups=False,
               monitoring_servers=None, all_monitoring_servers=False,
               all_bsm_components=False, all_bsm_edit=False, all_bsm_view=False,
               contacts=None, tenancy=None, params=None, body_only=False):

        body = {
            'name': name,
            'description': description,
            'all_hostgroups': all_hostgroups,
            'all_keywords': all_keywords,
            'all_servicegroups': all_servicegroups,
            'all_monitoringservers': all_monitoring_servers,
            'all_bsm_components': all_bsm_components,
            'all_bsm_edit': all_bsm_edit,
            'all_bsm_view': all_bsm_view,
            'tenancy': tenancy,
        }

        body['access_hostgroups'] = (
            [base.nameref(hg) for hg in hostgroups]
            if isinstance(hostgroups, list) else
            [base.nameref(hostgroups)]
        )

        body['access_keywords'] = (
            [base.nameref(kw) for kw in keywords]
            if isinstance(keywords, list) else
            [base.nameref(keywords)]
        )

        body['access_servicegroups'] = (
            [base.nameref(sg) for sg in service_groups]
            if isinstance(service_groups, list) else
            [base.nameref(service_groups)]
        )

        body['monitoringservers'] = (
            [base.nameref(ms) for ms in monitoring_servers]
            if isinstance(monitoring_servers, list) else
            [base.nameref(monitoring_servers)]
        )

        body['contacts'] = (
            [base.nameref(c) for c in contacts]
            if isinstance(contacts, list) else
            [base.nameref(contacts)]
        )

        body['accesses'] = (
            [base.nameref(p) for p in permissions]
            if isinstance(permissions, list) else
            [base.nameref(permissions)]
        )

        if body_only:
            return body

        return self._create('/config/role', body=body, params=params)

    def update(self, role, force=False, params=None, body_only=False, **kwds):
        if not kwds:
            return

        for (k, v) in six.iteritems(self.resource_class._field_map_):
            if k in kwds:
                kwds[v] = kwds[k]
                del kwds[k]

        if 'access_hostgroups' in kwds:
            kwds['access_hostgroups'] = (
                [base.nameref(hg) for hg in kwds['access_hostgroups']]
                if isinstance(kwds['access_hostgroups'], list) else
                [base.nameref(kwds['access_hostgroups'])]
            )

        if 'access_keywords' in kwds:
            kwds['access_keywords'] = (
                [base.nameref(kw) for kw in kwds['access_keywords']]
                if isinstance(kwds['access_keywords'], list) else
                [base.nameref(kwds['access_keywords'])]
            )

        if 'access_servicegroups' in kwds:
            kwds['access_servicegroups'] = (
                [base.nameref(sg) for sg in kwds['access_servicegroups']]
                if isinstance(kwds['access_servicegroups'], list) else
                [base.nameref(kwds['access_servicegroups'])]
            )

        if 'monitoringservers' in kwds:
            kwds['monitoringservers'] = (
                [base.nameref(ms) for ms in kwds['monitoringservers']]
                if isinstance(kwds['monitoringservers'], list) else
                [base.nameref(kwds['monitoringservers'])]
            )

        if 'contacts' in kwds:
            kwds['contacts'] = (
                [base.nameref(c) for c in kwds['contacts']]
                if isinstance(kwds['contacts'], list) else
                [base.nameref(kwds['contacts'])]
            )

        if 'accesses' in kwds:
            kwds['accesses'] = (
                [base.nameref(p) for p in kwds['accesses']]
                if isinstance(kwds['accesses'], list) else
                [base.nameref(kwds['accesses'])]
            )

        new_role = role.copy()
        new_role._info.update(kwds)
        new_role = new_role.encode()

        if not force:
            old_role = role.encode()
            if old_role == new_role:
                return

        body = new_role
        if body_only:
            return body

        return self._update('/config/role/%s' % base.get_id(role),
                            params=params, body=body)

    def get(self, role):
        return self._get('/config/role/%s' % base.get_id(role))

    def delete(self, role):
        return self._delete('/config/role/%s' % base.get_id(role))

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

        return self._list('/config/role%s' % qstring)
