#!/usr/bin/env python
# coding: utf-8

import six
from six.moves.urllib import parse

try:
    import simplejson as json
except ImportError:
    import json

from passlib.hash import apr_md5_crypt

from opsviewclient import base
from opsviewclient.fields import (
    FieldTypes as FT,
    FieldAttributes as FA
)

# TODO(jg): sort out notification profiles


class Contact(base.Resource):
    """
    {
        "id": "999",
        "name": "jgriffiths",
        "description": "Joshua Griffiths",
        "encrypted_password": null,
        "fullname": "Joshua Griffiths",
        "language": "",
        "notificationprofiles": [
            {
                "all_business_components": "0",
                "all_business_services": "0",
                "all_hostgroups": "1",
                "all_keywords": "0",
                "all_servicegroups": "1",
                "business_component_availability_below": "99.999",
                "business_component_options": "f,i",
                "business_component_renotification_interval": "1800",
                "business_components": [],
                "business_service_availability_below": "99.999",
                "business_service_options": "o,i",
                "business_service_renotification_interval": "1800",
                "business_services": [],
                "host_notification_options": "d,u,r,f",
                "hostgroups": [],
                "include_component_notes": "0",
                "include_service_notes": "0",
                "keywords": [],
                "name": "Test Notification",
                "notification_level": "1",
                "notification_level_stop": "0",
                "notification_period": {
                    "name": "24x7",
                    "ref": "/rest/config/timeperiod/1"
                },
                "notificationmethods": [
                    {
                        "name": "Email",
                        "ref": "/rest/config/notificationmethod/3"
                    },
                    {
                        "name": "Opsview Demo Notification",
                        "ref": "/rest/config/notificationmethod/14"
                    }
                ],
                "ref": "/rest/config/notificationprofile/4",
                "service_notification_options": "w,r,u,c,f",
                "servicegroups": [],
                "uncommitted": "0"
            }
        ]
        "realm": "ldap",
        "ref": "/rest/config/contact/66",
        "role": {
            "name": "Admin",
            "ref": "/rest/config/role/16"
        },
        "sharednotificationprofiles": [
            {
                "name": "shared np 1",
                "ref": "/rest/config/sharednotificationprofile/6"
            }
        ],
        "uncommitted": "0",
        "variables": [
            {
                "name": "EMAIL",
                "value": ""
            },
            {
                "name": "IOSPUSH_PASSWORD",
                "value": ""
            }
        ],
        "mylinks": [],
        "enable_tips": '1',
    }
    """

    _field_map_ = {
        'full_name': 'fullname',
        'notification_profiles': 'notificationprofiles',
        'shared_notification_profiles': 'sharednotificationprofiles',
        'my_links': 'mylinks',
    }

    _fields_ = {
        'id': FT.INT_STR,
        'name': FT.STR,
        'description': FT.STR,
        'encrypted_password': FT.STR,
        'fullname': FT.STR,
        'language': FT.STR,
        'notificationprofiles': FT.NONE,
        'realm': FT.STR,
        'ref': FT.STR,
        'role': FT.REF,
        'sharednotificationprofiles': FT.REF_LIST,
        'uncommitted': FT.BOOL_INT_STR,
        'variables': FT.NONE,
    }

    _field_attributes_ = {
        'id': FA.READONLY,
        'description': FA.OMIT_NONE,
        'encrypted_password': FA.OMIT_EMPTY,
        'fullname': FA.OMIT_NONE,
        'language': FA.OMIT_NONE,
        'notificationprofiles': FA.OMIT_EMPTY,
        'realm': FA.OMIT_NONE,
        'ref': FA.READONLY,
        'role': FA.OMIT_EMPTY,
        'sharednotificationprofiles': FA.OMIT_EMPTY,
        'uncommitted': FA.READONLY,
        'variables': FA.OMIT_EMPTY,
    }

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

    @property
    def role(self):
        if not self._info.get('role'):
            return

        # Return the proper role object via an API request
        if not self.manager:
            return self._info['role']

        role_id = base.id_from_ref(self._info['role'])
        return self.manager.client.config.roles.get(role_id)

    def __repr__(self):
        return '<Contact: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class ContactManager(base.Manager):

    resource_class = Contact

    def create(self, name, description=None, password=None,
               encrypted_password=None, full_name=None, language=None,
               notification_profiles=None, realm=None, role=None,
               shared_notification_profiles=None, variables=None,
               params=None, body_only=False):

        body = {
            'name': name,
            'description': description,
            'fullname': full_name,
            'language': language,
            'realm': realm,
        }

        if password:
            if encrypted_password:
                raise ValueError('Cannot specify password and '
                                 'encrypted_password together')

            # Must hash password in apache `apr1` (MD5) format
            encrypted_password = apr_md5_crypt.encrypt(password)

        body['encrypted_password'] = encrypted_password

        if notification_profiles:
            if not isinstance(notification_profiles, list):
                notification_profiles = [notification_profiles]

            body['notificationprofiles'] = [
                base.nameref(np) for np in notification_profiles
            ]

        if shared_notification_profiles:
            if not isinstance(shared_notification_profiles, list):
                shared_notification_profiles = [shared_notification_profiles]

            body['sharednotificationprofiles'] = [
                base.nameref(snp) for snp in shared_notification_profiles
            ]

        if role:
            body['role'] = base.nameref(role)

        if variables:
            if not isinstance(variables, list):
                variables = [variables]

            body['variables'] = variables

        body = self.resource_class._encode(body)

        if body_only:
            return body

        return self._create('/config/contact', body=body, params=params)

    def update(self, contact, force=False, params=None, body_only=None,
               **kwds):

        if kwds is None:
            # Nothing to update
            return

        # Replace keyword arguments with different API names
        for (k, v) in six.iteritems(self.resource_class._field_map_):
            if k in kwds:
                kwds[v] = kwds[k]
                del kwds[k]

        if 'role' in kwds:
            kwds['role'] = base.nameref(kwds['role'])

        if 'sharednotificationprofiles' in kwds:
            kwds['role'] = (
                [base.nameref(x) for x in kwds['sharednotificationprofiles']]
                if isinstance(kwds['sharednotificationprofiles'], list) else
                (base.nameref(kwds['sharednotificationprofiles']))
            )

        if 'variables' in kwds:
            if not isinstance(kwds['variables'], list):
                kwds['variables'] = [kwds['variables']]

        new_contact = contact.copy()
        new_contact._info.update(kwds)
        new_contact = new_contact.encoded()

        if not force:
            # Check if we need to update or if the contacts will be the same
            old_contact = contact.encoded()

            if old_contact == new_contact:
                # No changes
                return

        body = new_contact

        if body_only:
            return body

        return self._update('/config/contact/%s' % base.get_id(contact),
                            body=body, params=params)

    def get(self, contact):
        return self._get('/config/contact/%s' % base.get_id(contact))

    def delete(self, contact):
        return self._delete('/config/contact/%s' % base.get_id(contact))

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

        return self._list('/config/contact%s' % qstring)
