from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting

from plone.testing import z2

class Layer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.app.registry
        import collective.configviews
        import collective.configviews.tests.example
        self.loadZCML(package=plone.app.registry)
        self.loadZCML(package=collective.configviews)
        self.loadZCML(package=collective.configviews.tests.example)

        z2.installProduct(app, 'plone.app.registry')
        z2.installProduct(app, 'collective.configviews')


    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.configviews:default')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'collective.configviews')
        z2.uninstallProduct(app, 'plone.app.registry')


FIXTURE = Layer()
INTEGRATION = IntegrationTesting(bases=(FIXTURE,),
                                name="collective.configviews:Integration")
FUNCTIONAL =  FunctionalTesting(bases=(FIXTURE,), 
                                name="collective.configviews:Functional")
