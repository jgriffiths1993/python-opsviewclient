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


class TimePeriod(base.Resource):
    """
    {
        "alias": "",
        "friday": "00:00-24:00",
        "host_check_periods": [
            {
                "name": "10.0.2.200",
                "ref": "/rest/config/host/494"
            }
        ],
        "host_notification_periods": [
            {
                "name": "10.0.2.200",
                "ref": "/rest/config/host/494"
            },
            {
                "name": "12096_host",
                "ref": "/rest/config/host/508"
            }
        ],
        "id": "1",
        "monday": "00:00-24:00",
        "name": "24x7",
        "object_locked": "1",
        "ref": "/rest/config/timeperiod/1",
        "saturday": "00:00-24:00",
        "servicecheck_check_periods": [
            {
                "name": "/",
                "ref": "/rest/config/servicecheck/45"
            },
            {
                "name": "/backup",
                "ref": "/rest/config/servicecheck/84"
            }
        ],
        "servicecheck_notification_periods": [
            {
                "name": "kellen logdaemon passive",
                "ref": "/rest/config/servicecheck/572"
            },
            {
                "name": "logdaemon",
                "ref": "/rest/config/servicecheck/104"
            },
            {
                "name": "passive test",
                "ref": "/rest/config/servicecheck/550"
            }
        ],
        "sunday": "00:00-24:00",
        "thursday": "00:00-24:00",
        "tuesday": "00:00-24:00",
        "uncommitted": "0",
        "wednesday": "00:00-24:00"
    }
    """

    @property
    def host_check_periods(self):
        if not self._info.get('host_check_periods'):
            return

        if not self.manager:
            for h in self._info['host_check_periods']:
                yield h

        else:
            for h in self._info['host_check_periods']:
                h_id = base.id_from_ref(h)
                yield self.manager.client.config.hosts.get(h_id)

    @property
    def host_notification_periods(self):
        if not self._info.get('host_notification_periods'):
            return

        if not self.manager:
            for h in self._info['host_notification_periods']:
                yield h

        else:
            for h in self._info['host_notification_periods']:
                h_id = base.id_from_ref(h)
                yield self.manager.client.config.hosts.get(h_id)

    @property
    def service_check_check_periods(self):
        if not self._info.get('servicecheck_check_periods'):
            return

        if not self.manager:
            for sc in self._info['servicecheck_check_periods']:
                yield sc

        else:
            for sc in self._info['servicecheck_check_periods']:
                sc_id = base.id_from_ref(sc)
                yield self.manager.client.config.servicechecks.get(sc_id)

    @property
    def service_check_notification_periods(self):
        if not self._info.get('servicecheck_notification_periods'):
            return

        if not self.manager:
            for sc in self._info['servicecheck_notification_periods']:
                yield sc

        else:
            for sc in self._info['servicecheck_notification_periods']:
                sc_id = base.id_from_ref(sc)
                yield self.manager.client.config.servicechecks.get(sc_id)

    def __repr__(self):
        return '<TimePeriod: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)


class TimePeriodManager(base.Manager):

    resource_class = TimePeriod

    def get(self, time_period):
        return self._get('/config/timeperiod/%s' % base.get_id(time_period))

    def delete(self, time_period):
        return self._delete('/config/timeperiod/%s' % base.get_id(time_period))

    def create(self, name, alias, monday=None, tuesday=None, wednesday=None,
               thursday=None, friday=None, saturday=None, sunday=None,
               params=None, body_only=False):

        body = {
            'name': name,
            'alias': alias,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
        }

        body = self.resource_class._encode(body)

        if body_only:
            return body

        return self._create('/config/timeperiod', body=body, params=params)

    def update(self, timeperiod, force=False, params=None, body_only=None,
               **kwds):

        if kwds is None:
            return

        new_timeperiod = timeperiod.copy()
        new_timeperiod._info.update(kwds)
        new_timeperiod = new_timeperiod.encoded()

        if not force:
            old_timeperiod = timeperiod.encoded()
            if old_timeperiod == new_timeperiod:
                return

        body = new_timeperiod
        if body_only:
            return body

        return self._update('/config/timeperiod/%s' % base.get_id(timeperiod),
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

        return self._list('/config/timeperiod%s' % qstring)
