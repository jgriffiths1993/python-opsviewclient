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


class HostTemplate(base.Resource):
    """
    {
        "id": "125",
        "name": "a",
        "ref": "/rest/config/hosttemplate/125",
        "description": "a",
        "has_icon": "1402931397",
        "hosts": [
            {
                "name": "kellen-test",
                "ref": "/rest/config/host/255"
            },
            {
                "name": "kellentest2",
                "ref": "/rest/config/host/256"
            }
        ],
        "managementurls": [
            {
                "name": "Webadmin",
                "url": "http://ov-uat.opsview.com/"
            },
            {
                "name": "Webadmin1",
                "url": "http://ov-uat.opsview.com/"
            }
        ],
        "servicechecks": [
            {
                "event_handler": null,
                "exception": "--username=opsera --location=uk",
                "name": "check_em_rackspace",
                "ref": "/rest/config/servicecheck/404",
                "timed_exception": null
            },
            {
                "event_handler": null,
                "exception": null,
                "name": "ODW keyword SLA availability",
                "ref": "/rest/config/servicecheck/577",
                "timed_exception": null
            }
        ],
        "uncommitted": "0"
    }
    """

    _field_map_ = {
        'management_urls': 'managementurls',
        'service_checks': 'servicechecks',
    }

    _fields_ = {
        "id": FT.INT_STR,
        "name": FT.STR,
        "ref": FT.STR,
        "description": FT.STR,
        "has_icon": FT.INT_STR,
        "hosts": FT.REF_LIST,
        "managementurls": FT.NONE,
        "servicechecks": FT.REF_LIST,
        "uncommitted": FT.BOOL_INT_STR,
    }

    _field_attributes_ = {
        "id": FA.READONLY,
        "ref": FA.READONLY,
        "description": FA.OMIT_NONE,
        "has_icon": FA.READONLY,
        "hosts": FA.OMIT_NONE,
        "managementurls": FA.OMIT_NONE,
        "servicechecks": FA.OMIT_NONE,
        "uncommitted": FA.READONLY,
    }

    def __repr__(self):
        return '<HostTemplate: %s>' % self.name

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

    def delete(self):
        return self.manager.delete(self)


class HostTemplateManager(base.Manager):

    resource_class = HostTemplate

    def get(self, template):
        return self._get('/config/hosttemplate/%s' % base.get_id(template))

    def create(self, name, description=None, hosts=None, management_urls=None,
               service_checks=None, params=None, body_only=False):

        body = {
            'name': name,
            'description': description,
        }

        if hosts:
            if not isinstance(hosts, list):
                hosts = [hosts]

            body['hosts'] = [base.nameref(h) for h in hosts]

        if management_urls:
            if not isinstance(management_urls, list):
                management_urls = [management_urls]

            body['managementurls'] = []
            for url in management_urls:
                if not isinstance(url, dict) or not ('url' in url and
                                                     'name' in url):

                    raise ValueError('management_urls should be a dictionary '
                                     'or a list of dictionaries with keys: '
                                     '`url` and `name`')

                body['managementurls'].append(url)

        if service_checks:
            if not isinstance(service_checks, list):
                service_checks = [service_checks]

            body['servicechecks'] = []
            for sc in service_checks:
                if isinstance(sc, str):
                    body['servicechecks'].append(base.nameref(sc))
                else:
                    body['servicechecks'].append(sc)

        body = self.resource_class._encode(body)

        if body_only:
            return body

        return self._create('/config/hosttemplate', body=body, params=params)

    def update(self, host_template, force=False, params=None, body_only=False,
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

        if 'servicechecks' in kwds:
            scs = kwds['servicechecks']
            if not isinstance(scs, list):
                scs = [scs]

            kwds['servicechecks'] = []
            for sc in scs:
                if isinstance(sc, str):
                    kwds['servicechecks'].append(base.nameref(sc))
                else:
                    kwds['servicechecks'].append(sc)

        if 'managementurls' in kwds:
            urls = kwds['managementurls']

            if not isinstance(urls, list):
                urls = [urls]

            kwds['managementurls'] = []
            for url in urls:
                if not isinstance(url, dict) or not ('url' in url and
                                                     'name' in url):

                    raise ValueError('management_urls should be a dictionary '
                                     'or a list of dictionaries with keys: '
                                     '`url` and `name`')

                kwds['managementurls'].append(url)

        new_template = host_template.copy()
        new_template._info.update(kwds)
        new_template = new_template.encode()

        if not force:
            old_template = host_template.encode()

            if old_template == new_template:
                return

        body = new_template
        if body_only:
            return body

        return self._update('/config/hosttemplate/%s' %
                            base.get_id(host_template),
                            params=params, body=body)

    def delete(self, template):
        return self._delete('/config/hosttemplate/%s' % base.get_id(template))

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

        return self._list('/config/hosttemplate%s' % qstring)
