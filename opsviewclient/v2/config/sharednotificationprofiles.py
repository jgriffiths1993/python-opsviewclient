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


class SharedNotificationProfile(base.Resource):
    """
    {
        "all_business_components": "0",
        "all_business_services": "0",
        "all_hostgroups": "0",
        "all_keywords": "0",
        "all_servicegroups": "0",
        "business_component_availability_below": "99.999",
        "business_component_options": "f,i,r",
        "business_component_renotification_interval": "30",
        "business_components": [],
        "business_service_availability_below": "99.999",
        "business_service_options": "o,i",
        "business_service_renotification_interval": "30",
        "business_services": [],
        "host_notification_options": "u,d,r,f",
        "hostgroups": [],
        "id": "12",
        "include_component_notes": "0",
        "include_service_notes": "0",
        "keywords": [],
        "name": "1123",
        "notification_level": "1",
        "notification_level_stop": "0",
        "notification_period": {
            "name": "24x7",
            "ref": "/rest/config/timeperiod/1"
        },
        "notificationmethods": [],
        "ref": "/rest/config/sharednotificationprofile/12",
        "role": {
            "name": "Administrator",
            "ref": "/rest/config/role/22"
        },
        "service_notification_options": "w,c,r,u,f",
        "servicegroups": [],
        "uncommitted": "0"
    }
    """

    def __repr__(self):
        return '<SharedNotificationProfile: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class SharedNotificationProfileManager(base.Manager):

    resource_class = SharedNotificationProfile

    def get(self, profile):
        return self._get('/config/sharednotificationprofile/%s' %
                         base.get_id(profile))

    def delete(self, profile):
        return self._delete('/config/sharednotificationprofile/%s' %
                            base.get_id(profile))

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

        return self._list('/config/sharednotificationprofile%s' % qstring)
