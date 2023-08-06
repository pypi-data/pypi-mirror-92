# -*- coding: utf-8 -*-
from collective.clamav.interfaces import IAVScanner
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2
from zope.component import getGlobalSiteManager
from zope.configuration import xmlconfig
from zope.interface import implementer

import base64
import collective.clamav


class CollectiveClamavLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.clamav)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.clamav:default')


COLLECTIVE_CLAMAV_FIXTURE = CollectiveClamavLayer()


COLLECTIVE_CLAMAV_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CLAMAV_FIXTURE,),
    name='CollectiveClamavLayer:IntegrationTesting',
)


COLLECTIVE_CLAMAV_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CLAMAV_FIXTURE,),
    name='CollectiveClamavLayer:FunctionalTesting',
)


COLLECTIVE_CLAMAV_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_CLAMAV_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveClamavLayer:AcceptanceTesting',
)

s = """
    WDVPIVAlQEFQWzRcUFpYNTQoUF4pN0NDKTd9JEVJQ0FSLVNUQU5E
    QVJELUFOVElWSVJVUy1URVNU\nLUZJTEUhJEgrSCo=\n"""

EICAR = base64.b64decode(s)


@implementer(IAVScanner)
class MockAVScanner(object):
    """Mock objects to run tests withoud clamav present.
    """

    def ping(self, type, **kwargs):
        """
        """
        return True

    def scanBuffer(self, buffer, type, **kwargs):
        """
        """
        if EICAR in buffer:
            return 'Eicar-Test-Signature FOUND'
        return None


class AVFixture(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import collective.clamav
        xmlconfig.file('configure.zcml', collective.clamav,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.clamav:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Folder', 'virus-folder')  # noqa: P001
        setRoles(portal, TEST_USER_ID, ['Member'])


AV_FIXTURE = AVFixture()


class AVMockFixture(PloneSandboxLayer):

    defaultBases = (AV_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        gsm = getGlobalSiteManager()
        gsm.registerUtility(MockAVScanner())


AVMOCK_FIXTURE = AVMockFixture()

AV_INTEGRATION_TESTING = IntegrationTesting(
    bases=(AV_FIXTURE, ), name='AVFixture:Integration')
AV_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(AV_FIXTURE, ), name='AVFixture:Functional')
AVMOCK_INTEGRATION_TESTING = IntegrationTesting(
    bases=(AVMOCK_FIXTURE, ), name='AVMockFixture:Integration')
AVMOCK_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(AVMOCK_FIXTURE, ), name='AVMockFixture:Functional')
