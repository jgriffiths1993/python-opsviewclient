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


class NotificationMethod(base.Resource):
    """
    {
        "id": "5",
        "name": "Email",
        "active": "0",
        "command": "notify_by_email",
        "contact_variables": "EMAIL",
        "master": "1",
        "namespace": "com.opsview.notificationmethods.email",
        "notificationprofiles": [
            {
                "name": "test",
                "ref": "/rest/config/notificationprofile/56"
            },
            {
                "name": "oracle",
                "ref": "/rest/config/notificationprofile/93"
            }
        ],
        "ref": "/rest/config/notificationmethod/5",
        "sharednotificationprofiles": [
            {
                "name": "shared-admins",
                "ref": "/rest/config/sharednotificationprofile/8"
            }
        ],
        "uncommitted": "0",
        "variables": []
    }
    """

    _field_map_ = {
        'notification_profiles': 'notificationprofiles',
        'shared_notification_profiles': 'sharednotificationprofiles',
    }

    _fields_ = {
        'id': FT.INT_STR,
        'name': FT.STR,
        'active': FT.BOOL_INT_STR,
        'command': FT.STR,
        'contact_variables': FT.STR,
        'master': FT.BOOL_INT_STR,
        'namespace': FT.STR,
        'notificationprofiles': FT.REF_LIST,
        'ref': FT.STR,
        'sharednotificationprofiles': FT.REF_LIST,
        'uncommitted': FT.BOOL_INT_STR,
        'variables': FT.NONE,
    }

    _field_attributes_ = {
        'id': FA.READONLY,
        'active': FA.OMIT_NONE,
        'contact_variables': FA.OMIT_NONE,
        'master': FA.OMIT_NONE,
        'namespace': FA.OMIT_NONE,
        'notificationprofiles': FA.READONLY,
        'ref': FA.READONLY,
        'sharednotificationprofiles': FA.READONLY,
        'uncommitted': FA.READONLY,
        'variables': FA.OMIT_NONE,
    }

    @property
    def notification_profiles(self):
        # I don't know why we include these URIs; there is no way of actually
        # accessing the objects from the information given without listing
        # notification_profiles and trying to match the erroneous references
        raise NotImplemented('No request found for uri: '
                             '/rest/config/notificationprofile')

    @property
    def shared_notification_profiles(self):
        if not self._info.get('sharednotificationprofiles'):
            return

        if not self.manager:
            for profile in self._info['sharednotificationprofiles']:
                yield profile

        else:
            for profile in self._info['sharednotificationprofiles']:
                profile_id = base.id_from_ref(profile)
                yield self.manager.client.config.sharednotificationprofiles.get(
                    profile_id
                )

    def __repr__(self):
        return '<NotificationMethod: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class NotificationMethodManager(base.Manager):

    resource_class = NotificationMethod

    def get(self, method):
        return self._get('/config/notificationmethod/%s' % base.get_id(method))

    def create(self, name, command, active=None, contact_variables=None,
               master=None, namespace=None, variables=None,
               params=None, body_only=False):

        body = {
            'name': name,
            'command': command,
            'active': active,
            'contact_variables': contact_variables,
            'master': master,
            'namespace': namespace,
        }

        if variables:
            if not isinstance(variables, list):
                variables = [variables]

            body['variables'] = []
            for v in variables:
                if not isinstance(v, dict) or not ('name' in v and
                                                   'value' in v):
                    raise ValueError(
                        'variables must be a dictionary or list of dictionaries'
                        ' containing the keys "name" and "value"'
                    )

                body['variables'].append(v)

        body = self.resource_class._encode(body)

        if body_only:
            return body

        return self._create('/config/notificationmethod',
                            body=body, params=params)

    def update(self, notification_method, force=False, params=None,
               body_only=False, **kwds):

        if kwds is None:
            return

        # Replace keyword arguments with opsview api names
        for (k, v) in six.iteritems(self.resource_class._field_map_):
            if k in kwds:
                kwds[v] = kwds[k]
                del kwds[k]

        if 'variables' in kwds:
            variables = kwds.pop('variables')

            if not isinstance(variables, list):
                variables = [variables]

            kwds['variables'] = []
            for v in variables:
                if not isinstance(v, dict) or not ('name' in v and
                                                   'value' in v):
                    raise ValueError(
                        'variables must be a dictionary or list of dictionaries'
                        ' containing the keys "name" and "value"'
                    )

                kwds['variables'].append(v)

        new_notif = notification_method.copy()
        new_notif._info.update(kwds)
        new_notif = new_notif.encode()

        if not force:
            old_notif = notification_method.encode()
            if old_notif == new_notif:
                return

        body = new_notif
        if body_only:
            return body

        return self._update('/config/notificationmethod/%s' %
                            base.get_id(notification_method),
                            params=params, body=body)

    def delete(self, method):
        return self._delete('/config/notificationmethod/%s' %
                            base.get_id(method))

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

        return self._list('/config/notificationmethod%s' % qstring)
