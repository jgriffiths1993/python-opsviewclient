#!/usr/bin/env python
# coding: utf-8

from opsviewclient.v2.config import attributes
from opsviewclient.v2.config import collectors
from opsviewclient.v2.config import contacts
from opsviewclient.v2.config import hostcheckcommands
from opsviewclient.v2.config import hostgroups
from opsviewclient.v2.config import hosttemplates
from opsviewclient.v2.config import hosts
from opsviewclient.v2.config import keywords
from opsviewclient.v2.config import monitoringclusters
from opsviewclient.v2.config import monitoringservers
from opsviewclient.v2.config import netflowcollectors
from opsviewclient.v2.config import netflowsources
from opsviewclient.v2.config import notificationmethods
from opsviewclient.v2.config import roles
from opsviewclient.v2.config import servicechecks
from opsviewclient.v2.config import servicegroups
from opsviewclient.v2.config import sharednotificationprofiles
from opsviewclient.v2.config import tenancies
from opsviewclient.v2.config import timeperiods


class Client(object):

    def __init__(self, api):
        self._api = api
        self.attributes = attributes.AttributeManager(api)
        self.collectors = collectors.CollectorManager(api)
        self.contacts = contacts.ContactManager(api)
        self.hostcheckcommands = hostcheckcommands.HostCheckCommandManager(api)
        self.hostgroups = hostgroups.HostGroupManager(api)
        self.hosttemplates = hosttemplates.HostTemplateManager(api)
        self.hosts = hosts.HostManager(api)
        self.keywords = keywords.KeywordManager(api)
        self.monitoringservers = monitoringservers.MonitoringServerManager(api)
        self.monitoringclusters = \
            monitoringclusters.MonitoringClusterManager(api)

        self.netflowcollectors = netflowcollectors.NetflowCollectorManager(api)
        self.netflowsources = netflowsources.NetflowSourceManager(api)
        self.notificationmethods = \
            notificationmethods.NotificationMethodManager(api)

        self.roles = roles.RoleManager(api)
        self.servicechecks = servicechecks.ServiceCheckManager(api)
        self.servicegroups = servicegroups.ServiceGroupManager(api)
        self.sharednotificationprofiles = \
            sharednotificationprofiles.SharedNotificationProfileManager(api)

        self.tenancies = tenancies.TenancyManager(api)
        self.timeperiods = timeperiods.TimePeriodManager(api)
