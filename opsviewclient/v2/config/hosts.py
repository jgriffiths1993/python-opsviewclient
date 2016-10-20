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


class Host(base.Resource):
    """
    {
        "id": "494",
        "name": "10.0.2.200",
        "ip": "10.0.2.200",
        "alias": "",
        "other_addresses": "",
        "business_components": [],
        "check_attempts": "2",
        "check_command": {
            "name": "ping",
            "ref": "/rest/config/hostcheckcommand/16"
        },
        "check_interval": "5",
        "check_period": {
            "name": "24x7",
            "ref": "/rest/config/timeperiod/1"
        },
        "enable_snmp": "1",
        "event_handler": "",
        "flap_detection_enabled": "0",
        "hostattributes": [],
        "hostgroup": {
            "name": "anotherplaceholder",
            "ref": "/rest/config/hostgroup/172"
        },
        "hosttemplates": [
            {
                "name": "hhh",
                "ref": "/rest/config/hosttemplate/137"
            }
        ],
        "icon": {
            "name": "LOGO - 3com",
            "path": "/images/logos/3com_small.png"
        },
        "keywords": [],
        "last_updated": "1461272645",
        "monitored_by": {
            "name": "Master Monitoring Server",
            "ref": "/rest/config/monitoringserver/1"
        },
        "nmis_node_type": "router",
        "notification_interval": "60",
        "notification_options": "",
        "notification_period": {
            "name": "24x7",
            "ref": "/rest/config/timeperiod/1"
        },
        "parents": [
            {
                "name": "easedale.opsera.com",
                "ref": "/rest/config/host/325"
            }
        ],
        "rancid_connection_type": "ssh",
        "rancid_username": "",
        "rancid_vendor": {
            "name": "Agm",
            "ref": "/rest/config/rancidvendor/1"
        },
        "ref": "/rest/config/host/494",
        "retry_check_interval": "1",
        "servicechecks": [],
        "snmp_extended_throughput_data": "0",
        "snmp_max_msg_size": "0",
        "snmp_port": "161",
        "snmp_version": "2c",
        "snmpv3_authprotocol": null,
        "snmpv3_privprotocol": null,
        "snmpv3_username": "",
        "tidy_ifdescr_level": "0",
        "uncommitted": "0",
        "use_mrtg": "0",
        "use_nmis": "0",
        "use_rancid": "0"
    }
    """

    _field_map_ = {
        'host_attributes': 'hostattributes',
        'host_group': 'hostgroup',
        'host_templates': 'hosttemplates',
        'service_checks': 'servicechecks',
    }

    # TODO add password stuff
    _fields_ = {
        'id': FT.INT_STR,
        'name': FT.STR,
        'ip': FT.STR,
        'alias': FT.STR,
        'other_addresses': FT.STR,
        'business_components': FT.REF_LIST,
        'check_attempts': FT.INT_STR,
        'check_command': FT.REF,
        'check_interval': FT.INT_STR,
        'check_period': FT.REF,
        'enable_snmp': FT.BOOL_INT_STR,
        'encrypted_rancid_password': FT.STR,
        'encrypted_snmp_community': FT.STR,
        'encrypted_snmpv3_autopassword': FT.STR,
        'encrypted_snmpv3_privpassword': FT.STR,
        'event_handler': FT.STR,
        'flap_detection_enabled': FT.BOOL_INT_STR,
        'hostattributes': FT.NONE,
        'hostgroup': FT.REF,
        'hosttemplates': FT.REF_LIST,
        'icon': FT.NONE,
        'is_master': FT.BOOL_INT_STR,
        'keywords': FT.REF_LIST,
        'last_updated': FT.INT_STR,
        'monitored_by': FT.REF,
        'nmis_node_type': FT.STR,
        'notification_interval': FT.INT_STR,
        'notification_options': FT.STR,
        'notification_period': FT.REF,
        'parents': FT.REF_LIST,
        'rancid_connection_type': FT.STR,
        'rancid_username': FT.STR,
        'rancid_password': FT.STR,
        'rancid_vendor': FT.REF,
        'ref': FT.STR,
        'retry_check_interval': FT.INT_STR,
        'servicechecks': FT.REF_LIST,
        'snmp_community': FT.STR,
        'snmp_extended_throughput_data': FT.BOOL_INT_STR,
        'snmp_max_msg_size': FT.STR,
        'snmp_port': FT.INT_STR,
        'snmp_version': FT.STR,
        'snmpv3_autopassword': FT.STR,
        'snmpv3_authprotocol': FT.STR,
        'snmpv3_privpassword': FT.STR,
        'snmpv3_privprotocol': FT.STR,
        'snmpv3_username': FT.STR,
        'tidy_ifdescr_level': FT.INT_STR,
        'uncommitted': FT.BOOL_INT_STR,
        'use_mrtg': FT.BOOL_INT_STR,
        'use_nmis': FT.BOOL_INT_STR,
        'use_rancid': FT.BOOL_INT_STR,
    }

    _field_attributes_ = {
        'id': FA.READONLY,
        'alias': FA.OMIT_NONE,
        'other_addresses': FA.OMIT_NONE,
        'check_attempts': FA.OMIT_NONE,
        'check_command': FA.OMIT_NONE,
        'check_interval': FA.OMIT_NONE,
        'check_period': FA.OMIT_NONE,
        'enable_snmp': FA.OMIT_NONE,
        'encrypted_rancid_password': FA.OMIT_NONE,
        'encrypted_snmp_community': FA.OMIT_NONE,
        'encrypted_snmpv3_autopassword': FA.OMIT_NONE,
        'encrypted_snmpv3_privpassword': FA.OMIT_NONE,
        'event_handler': FA.OMIT_NONE,
        'flap_detection_enabled': FA.OMIT_NONE,
        'hostattributes': FA.OMIT_NONE,
        'hostgroup': FA.OMIT_NONE,
        'hosttemplates': FA.OMIT_NONE,
        'is_master': FA.READONLY,
        'icon': FA.OMIT_NONE,
        'keywords': FA.OMIT_NONE,
        'last_updated': FA.READONLY,
        'monitored_by': FA.OMIT_NONE,
        'nmis_node_type': FA.OMIT_NONE,
        'notification_interval': FA.OMIT_NONE,
        'notification_options': FA.OMIT_NONE,
        'notification_period': FA.OMIT_NONE,
        'parents': FA.OMIT_NONE,
        'rancid_connection_type': FA.OMIT_NONE,
        'rancid_username': FA.OMIT_NONE,
        'rancid_password': FA.OMIT_NONE,
        'snmp_community': FA.OMIT_NONE,
        'rancid_vendor': FA.OMIT_NONE,
        'ref': FA.READONLY,
        'retry_check_interval': FA.READONLY,
        'servicechecks': FA.OMIT_NONE,
        'snmp_extended_throughput_data': FA.OMIT_NONE,
        'snmp_max_msg_size': FA.OMIT_NONE,
        'snmp_port': FA.OMIT_NONE,
        'snmp_version': FA.OMIT_NONE,
        'snmpv3_autopassword': FA.OMIT_NONE,
        'snmpv3_authprotocol': FA.OMIT_NONE,
        'snmpv3_privpassword': FA.OMIT_NONE,
        'snmpv3_privprotocol': FA.OMIT_NONE,
        'snmpv3_username': FA.OMIT_NONE,
        'tidy_ifdescr_level': FA.OMIT_NONE,
        'uncommitted': FA.READONLY,
        'use_mrtg': FA.OMIT_NONE,
        'use_nmis': FA.OMIT_NONE,
        'use_rancid': FA.OMIT_NONE,
    }

    def __repr__(self):
        return '<Host: %s>' % self.name

    # TODO(jg): Property for business components

    @property
    def keywords(self):
        if not self._info.get('keywords'):
            return

        if not self.manager:
            for k in self._info['keywords']:
                yield k
        else:
            for k in self._info['keywords']:
                k_id = base.id_from_ref(k)
                yield self.manager.client.config.keywords.get(k_id)

    @property
    def check_command(self):
        if not self._info.get('check_command'):
            return

        if not self.manager:
            return self._info['check_command']

        check_id = base.id_from_ref(self._info['check_command'])
        return self.manager.client.config.hostcheckcommands.get(check_id)

    @property
    def check_period(self):
        if not self._info.get('check_period'):
            return

        if not self.manager:
            return self._info['check_period']

        period_id = base.id_from_ref(self._info['check_period'])
        return self.manager.client.config.timeperiods.get(period_id)

    @property
    def host_group(self):
        if not self._info.get('hostgroup'):
            return

        if not self.manager:
            return self._info['hostgroup']

        hg_id = base.id_from_ref(self._info['hostgroup'])
        return self.manager.client.config.hostgroups.get(hg_id)

    @property
    def host_templates(self):
        if not self._info.get('hosttemplates'):
            return

        if not self.manager:
            for ht in self._info['hosttemplates']:
                yield ht
        else:
            for ht in self._info['hosttemplates']:
                ht_id = base.id_from_ref(ht)
                yield self.manager.client.config.hosttemplates.get(ht_id)

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

    @property
    def parents(self):
        if not self._info.get('parents'):
            return

        if not self.manager:
            for h in self._info['parents']:
                yield h
        else:
            for h in self._info['parents']:
                h_id = base.id_from_ref(h)
                yield self.manager.client.config.hosts.get(h_id)

    @property
    def notification_period(self):
        if not self._info.get('notification_period'):
            return

        if not self.manager:
            return self._info['notification_period']

        period_id = base.id_from_ref(self._info['notification_period'])
        return self.manager.client.config.timeperiods.get(period_id)

    @property
    def monitored_by(self):
        if not self._info.get('monitored_by'):
            return

        if not self.manager:
            return self._info['monitored_by']

        mon_id = base.id_from_ref(self._info['monitored_by'])
        return self.manager.client.config.monitoringservers.get(mon_id)

    def delete(self):
        return self.manager.delete(self)


class HostManager(base.Manager):

    resource_class = Host

    def get(self, host, params=None):
        return self._get('/config/host/%s' % base.get_id(host),
                         params=params)

    def delete(self, host):
        return self._delete('/config/host/%s' % base.get_id(host))

    def create(self, name, ip, alias=None, other_addresses=None,
               business_components=None, check_attempts=None,
               check_command=None, check_interval=None, check_period=None,
               enable_snmp=None, event_handler=None,
               flap_detection_enabled=None, host_attributes=None,
               host_group=None, host_templates=None, icon=None,
               keywords=None, monitored_by=None, nmis_node_type=None,
               notification_interval=None, notification_options=None,
               notification_period=None, parents=None,
               rancid_connection_type=None, rancid_username=None,
               retry_check_interval=None, service_checks=None,
               snmp_extended_throughput_data=None, snmp_max_msg_size=None,
               snmp_port=None, snmp_version=None, snmpv3_authprotocol=None,
               snmpv3_privprotocol=None, snmpv3_username=None,
               tidy_ifdescr_level=None, use_mrtg=None, use_nmis=None,
               use_rancid=None,
               encrypted_rancid_password=None, rancid_password=None,
               encrypted_snmp_community=None, snmp_community=None,
               encrypted_snmpv3_authpassword=None, snmpv3_authpassword=None,
               encrypted_snmpv3_privpassword=None, snmpv3_privpassword=None,
               params=None, body_only=None):

        body = {
            'name': name,
            'ip': ip,
            'alias': alias,
            'other_addresses': (','.join(other_addresses)
                                if isinstance(other_addresses, list)
                                else other_addresses),
            'check_attempts': check_attempts,
            'check_command': base.nameref(check_command),
            'check_interval': check_interval,
            'check_period': base.nameref(check_period),
            'enable_snmp': enable_snmp,
            'event_handler': event_handler,
            'flap_detection_enabled': flap_detection_enabled,
            'hostgroup': base.nameref(host_group),
            'monitored_by': base.nameref(monitored_by),
            'nmis_node_type': nmis_node_type,
            'notification_interval': notification_interval,
            'notification_options': notification_options,
            'notification_period': base.nameref(notification_period),
            'rancid_connection_type': rancid_connection_type,
            'rancid_username': rancid_username,
            'retry_check_interval': retry_check_interval,
            'snmp_extended_throughput_data': snmp_extended_throughput_data,
            'snmp_max_msg_size': snmp_max_msg_size,
            'snmp_port': snmp_port,
            'snmp_version': snmp_version,
            'snmpv3_authprotocol': snmpv3_authprotocol,
            'snmpv3_privprotocol': snmpv3_privprotocol,
            'snmpv3_username': snmpv3_username,
            'tidy_ifdescr_level': tidy_ifdescr_level,
            'use_mrtg': use_mrtg,
            'use_nmis': use_nmis,
            'use_rancid': use_rancid,
        }

        if encrypted_rancid_password:
            if rancid_password:
                raise ValueError('Cannot supply both encrypted and unencrypted '
                                 'passwords for rancid_password')

            body['encrypted_rancid_password'] = encrypted_rancid_password
        elif rancid_password:
            body['rancid_password'] = rancid_password

        if encrypted_snmp_community:
            if snmp_community:
                raise ValueError('Cannot supply both encrypted and unencrypted '
                                 'passwords for snmp_community')

            body['encrypted_snmp_community'] = encrypted_snmp_community
        elif snmp_community:
            body['snmp_community'] = snmp_community

        if encrypted_snmpv3_authpassword:
            if snmpv3_authpassword:
                raise ValueError('Cannot supply both encrypted and unencrypted '
                                 'passwords for snmpv3_authpassword')

            body['encrypted_snmpv3_authpassword'] = \
                encrypted_snmpv3_authpassword

        elif snmpv3_authpassword:
            body['snmpv3_authpassword'] = snmpv3_authpassword

        if encrypted_snmpv3_privpassword:
            if snmpv3_privpassword:
                raise ValueError('Cannot supply both encrypted and unencrypted '
                                 'passwords for snmpv3_privpassword')

            body['encrypted_snmpv3_privpassword'] = \
                encrypted_snmpv3_privpassword

        elif snmpv3_privpassword:
            body['snmpv3_privpassword'] = snmpv3_privpassword

        if icon:
            if isinstance(icon, str):
                key = 'path' if icon[0] == '/' else 'name'

                body['icon'] = {key: icon}
            else:
                body['icon'] = icon

        if service_checks:
            if not isinstance(service_checks, list):
                service_checks = [service_checks]

            body['servicechecks'] = []
            for sc in service_checks:
                if isinstance(sc, six.string_types):
                    body['servicechecks'].append(base.nameref(sc))
                else:
                    body['servicechecks'].append(sc)

        if host_templates:
            if not isinstance(host_templates, list):
                host_templates = [host_templates]

            body['hosttemplates'] = [base.nameref(ht) for ht in host_templates]

        if parents:
            if not isinstance(parents, list):
                parents = [parents]

            body['parents'] = [base.nameref(p) for p in parents]

        if keywords:
            if not isinstance(keyword, list):
                keywords = [keywords]

            body['keywords'] = [base.nameref(k) for k in keywords]

        if host_attributes:
            if not isinstance(host_attributes, list):
                host_attributes = [host_attributes]

            body['hostattributes'] = host_attributes

        if business_components:
            if not isinstance(business_components, list):
                business_components = [business_components]

            body['business_components'] = [base.nameref(bc) for bc
                                           in business_components]

        body = self.resource_class._encode(body)

        if body_only:
            return body

        return self._create('/config/host', body=body, params=params)

    def update(self, host, force=False, params=None, body_only=False,
               always_update_passwords=True, **kwds):

        if not kwds:
            # Nothing to update
            return

        for (k, v) in six.iteritems(self.resource_class._field_map_):
            if k in kwds:
                kwds[v] = kwds[k]
                del kwds[k]

        if 'check_command' in kwds:
            kwds['check_command'] = base.nameref(kwds['check_command'])

        if 'check_period' in kwds:
            kwds['check_period'] = base.nameref(kwds['check_period'])

        if 'hostgroup' in kwds:
            kwds['hostgroup'] = base.nameref(kwds['hostgroup'])

        if 'hosttemplates' in kwds:
            kwds['hosttemplates'] = (
                [base.nameref(p) for p in kwds['hosttemplates']]
                if isinstance(kwds['hosttemplates'], list)
                else [base.nameref(kwds['hosttemplates'])]
            )

        if 'icon' in kwds:
            if isinstance(kwds['icon'], str):
                key = 'path' if kwds['icon'][0] == '/' else 'name'
                kwds['icon'] = {key: icon}

        if 'keywords' in kwds:
            kwds['keywords'] = base.nameref(kwds['keywords'])

        if 'notification_period' in kwds:
            kwds['notification_period'] = \
                base.nameref(kwds['notification_period'])

        if 'parents' in kwds:
            kwds['parents'] = (
                [base.nameref(p) for p in kwds['parents']]
                if isinstance(kwds['parents'], list)
                else [base.nameref(kwds['parents'])]
            )

        if 'rancid_vendor' in kwds:
            kwds['rancid_vendor'] = base.nameref(kwds['rancid_vendor'])

        if 'service_checks' in kwds:
            scs = kwds['servicechecks']
            if not isinstance(scs, list):
                scs = [scs]

            kwds['servicechecks'] = []
            for sc in scs:
                if isinstance(sc, six.string_types):
                    kwds['servicechecks'].append(base.nameref(sc))
                else:
                    kwds['servicechecks'].append(sc)

        new_host = host.copy()
        new_host._info.update(kwds)
        new_host = new_host.encoded()

        if not force:
            old_host = host.encoded()

            for pw_key in ['snmp_community', 'rancid_password',
                           'snmpv3_authpassword', 'snmpv3_privpassword']:

                # If we aren't updating passwords, make sure that they're
                # removed from the new host before comparing them
                if pw_key in new_host and not always_update_passwords:
                    del new_host[pw_key]

                # Delete encrypted password fields from the old host unless
                # they exist in both or the comparison won't work
                e_pw_key = 'encrypted_' + pw_key
                if e_pw_key in old_host and e_pw_key not in new_host:
                    del old_host[e_pw_key]

                # If the new host has encrypted_X passwords in and the old host
                # does not then we need to re-get the old host with these fields
                if e_pw_key in new_host and e_pw_key not in old_host:
                    old_host = self.get(
                        host, params={'include_encrypted': 1}
                    ).encoded()

            if old_host == new_host:
                return

        body = new_host
        if body_only:
            return body

        return self._update('/config/host/%s' % base.get_id(host),
                            body=body, params=params)

    def list(self, rows='all', page=None, cols=None, order=None,
             search=None, in_use=None, is_parent=None, include_ms=None,
             include_encrypted=None, monitored_by_id=None, template_id=None,
             template_name=None, bsm_component_id=None, with_snmpifs=False,
             kwds=None):

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
        if is_parent is not None:
            qparams['is_parent'] = 1 if is_parent else 0
        if include_ms is not None:
            qparams['include_ms'] = 1 if include_ms else 0
        if include_encrypted is not None:
            qparams['include_encrypted'] = 1 if include_encrypted else 0
        if monitored_by_id:
            qparams['s.monitored_by.id'] = int(monitored_by_id)
        if template_id:
            qparams['s.hosttemplates.id'] = int(template_id)
        if template_name:
            qparams['s.hosttemplates.name'] = str(template_name)
        if bsm_component_id:
            qparams['s.business_components.id'] = int(bsm_component_id)
        if with_snmpifs:
            if 'cols' in qparams:
                qparams['cols'] += ',+snmpinterfaces'
            else:
                qparams['cols'] = '+snmpinterfaces'

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/host%s' % qstring)

    def create_many(self, _list, params=None):
        if isinstance(_list, list):
            _list = {'list': _list}

        return self._create('/config/host', body=_list, params=params,
                            return_raw=True)
