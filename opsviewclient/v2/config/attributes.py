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


class Attribute(base.Resource):
    """
    {
        "id": "72",
        "name": "A2",
        "arg1": "C:",
        "arg2": "5",
        "arg3": "10",
        "arg4": "",
        "label1": "",
        "label2": "",
        "label3": "",
        "label4": "",
        "ref": "/rest/config/attribute/72",
        "secured1": "0",
        "secured2": "0",
        "secured3": "0",
        "secured4": "0",
        "servicechecks": [],
        "uncommitted": "0",
        "value": "Testing"
    }
    """

    # Map our API names to the Opsview API names
    _field_map_ = {
        'default_value': 'value',
        'arg1_default_value': 'arg1',
        'arg2_default_value': 'arg2',
        'arg3_default_value': 'arg3',
        'arg4_default_value': 'arg4',
        'arg1_label': 'label1',
        'arg2_label': 'label2',
        'arg3_label': 'label3',
        'arg4_label': 'label4',
        'arg1_encrypted': 'secured1',
        'arg2_encrypted': 'secured2',
        'arg3_encrypted': 'secured3',
        'arg4_encrypted': 'secured4',
    }

    # Map the types we use to the API types used by Opsview to prevent using
    # stringy booleans and integers
    _fields_ = {
        "id": FT.INT_STR,
        "name": FT.STR,
        "value": FT.STR,
        "arg1": FT.STR,
        "arg2": FT.STR,
        "arg3": FT.STR,
        "arg4": FT.STR,
        "label1": FT.STR,
        "label2": FT.STR,
        "label3": FT.STR,
        "label4": FT.STR,
        "secured1": FT.BOOL_INT_STR,
        "secured2": FT.BOOL_INT_STR,
        "secured3": FT.BOOL_INT_STR,
        "secured4": FT.BOOL_INT_STR,
        "servicechecks": FT.REF_LIST,
        "uncommitted": FT.BOOL_INT_STR,
    }

    # Specify which fields should be ommitted and cannot be updated/created
    _field_attributes_ = {
        'id': FA.READONLY,
        'ref': FA.READONLY,
        'servicechecks': FA.READONLY,
        'uncommitted': FA.READONLY,
        "arg1": FA.OMIT_NONE,
        "arg2": FA.OMIT_NONE,
        "arg3": FA.OMIT_NONE,
        "arg4": FA.OMIT_NONE,
        "label1": FA.OMIT_NONE,
        "label2": FA.OMIT_NONE,
        "label3": FA.OMIT_NONE,
        "label4": FA.OMIT_NONE,
        "value": FA.OMIT_NONE
    }

    @property
    def service_checks(self):
        if not self._info.get('servicechecks'):
            return

        if not self.manager:
            for check in self._info['servicechecks']:
                yield check

        else:
            for check in self._info['servicechecks']:
                check_id = base.id_from_ref(check)
                yield self.manager.client.config.servicechecks.get(check_id)

    def __repr__(self):
        return '<Attribute: %s>' % self.name


class AttributeManager(base.Manager):

    resource_class = Attribute

    def get(self, attribute):
        return self._get('/config/attribute/%s' % base.get_id(attribute))

    def create(self, name, default_value=None,
               arg1_default_value=None, arg1_label=None, arg1_encrypted=False,
               arg2_default_value=None, arg2_label=None, arg2_encrypted=False,
               arg3_default_value=None, arg3_label=None, arg3_encrypted=False,
               arg4_default_value=None, arg4_label=None, arg4_encrypted=False,
               params=None, body_only=None):

        body = {
            'name': name,
        }

        body['value'] = default_value

        body['arg1'] = arg1_default_value
        body['label1'] = arg1_label
        body['secured1'] = True if arg1_encrypted else False

        body['arg2'] = arg2_default_value
        body['label2'] = arg2_label
        body['secured2'] = True if arg2_encrypted else False

        body['arg3'] = arg3_default_value
        body['label3'] = arg3_label
        body['secured3'] = True if arg3_encrypted else False

        body['arg4'] = arg4_default_value
        body['label4'] = arg4_label
        body['secured4'] = True if arg4_encrypted else False

        body = self.resource_class._encode(body)

        if body_only:
            return body

        return self._create('/config/attribute', body=body, params=params)

    def delete(self, attribute):
        return self._delete('/config/attribute/%s' % base.get_id(attribute))

    def update(self, attribute, force=False, params=None, body_only=None,
               **kwds):

        if kwds is None:
            # kwds should contain all of the attributes to be updated. If this
            # is empty then we have no updates to make
            return

        # Replace the kwds with the appropriate names used by the Opsview API.
        for (k, v) in six.iteritems(self.resource_class._field_map_):
            if k in kwds:
                kwds[v] = kwds[k]
                del kwds[k]

        new_attr = attribute.copy()
        new_attr._info.update(kwds)
        new_attr = new_attr.encoded()
        if not force:
            # Check if the existing attribute is the same as what we'll have if
            # we update it. If not, don't bother updating it.

            # Strip the fields which can't be updated anyway.
            old_attr = attribute.encoded()

            if old_attr == new_attr:
                # No changes
                return

        body = new_attr

        if body_only:
            return body

        return self._update('/config/attribute/%s' % base.get_id(attribute),
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

        return self._list('/config/attribute%s' % qstring)
