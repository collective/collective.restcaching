# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.restcaching


class CollectiveRestcachingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        # import plone.restapi
        # self.loadZCML(package=plone.restapi)
        import plone.app.caching
        import plone.rest
        self.loadZCML(name="configure.zcml", package=plone.app.caching)
        self.loadZCML(name="configure.zcml", package=plone.rest)
        self.loadZCML(name="testing.zcml", package=plone.rest)
        self.loadZCML(package=collective.restcaching)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.restcaching:default')
        applyProfile(portal, 'plone.app.caching:default')
        applyProfile(portal, 'plone.app.caching:without-caching-proxy')


COLLECTIVE_RESTCACHING_FIXTURE = CollectiveRestcachingLayer()


COLLECTIVE_RESTCACHING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_RESTCACHING_FIXTURE,),
    name='CollectiveRestcachingLayer:IntegrationTesting',
)


COLLECTIVE_RESTCACHING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_RESTCACHING_FIXTURE, z2.ZSERVER_FIXTURE),
    name='CollectiveRestcachingLayer:FunctionalTesting',
)


COLLECTIVE_RESTCACHING_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_RESTCACHING_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveRestcachingLayer:AcceptanceTesting',
)
