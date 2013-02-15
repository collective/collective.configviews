from collective.configviews.tests import base
from collective.configviews.tests import fake


class ProviderUnitTest(base.UnitTestCase):

    def setUp(self):
        from collective.configviews import provider
        self.view = fake.FakeConfigurableView()
        self.provider_module = provider
        self.provider = provider.Provider(self.view)
        self.provider.providers = [fake.FakeConfigurationProvider()]

    def test_get(self):
        mysettings = self.provider.get()
        self.failUnless(len(mysettings.keys()) == 1)
        self.failUnless(mysettings['foo'] == 'bar')

        #test aggregation of providers
        self.provider.providers.append(fake.FakeConfigurationProvider())
        self.provider.providers[1].configuration['foo'] = 'beer'
        self.provider.providers[1].configuration['other'] = 'great'
        mysettings = self.provider.get()
        #settings are cached
        self.failUnless(mysettings['foo'] == 'bar')
        #force reload
        self.provider.configuration = {}
        mysettings = self.provider.get()
        self.failUnless(mysettings['foo'] == 'beer')
        self.failUnless(mysettings['other'] == 'great')

    def test_pnames(self):
        #the one set by the view
        self.assertEqual(len(self.provider.pnames), 1)
        self.assertEqual(self.provider.pnames[0],
                         self.view.settings_providers[0])
