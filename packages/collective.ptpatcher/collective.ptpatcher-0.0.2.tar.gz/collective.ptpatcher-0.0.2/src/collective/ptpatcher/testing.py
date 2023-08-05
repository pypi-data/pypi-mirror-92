# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import collective.ptpatcher.tests
import z3c.jbot


class CollectivePtpatcherLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=z3c.jbot)
        self.loadZCML(package=collective.ptpatcher.tests)


COLLECTIVE_PTPATCHER_FIXTURE = CollectivePtpatcherLayer()


COLLECTIVE_PTPATCHER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_PTPATCHER_FIXTURE,),
    name='CollectivePtpatcherLayer:IntegrationTesting'
)


COLLECTIVE_PTPATCHER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_PTPATCHER_FIXTURE,),
    name='CollectivePtpatcherLayer:FunctionalTesting'
)
