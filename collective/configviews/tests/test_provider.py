import base, utils

class ProviderUnitTest(base.UnitTestCase):

    def setUp(self):
        from collective.configviews import provider
        self.view = utils.FakeConfigurableView()
        self.provider_module = provider
        self.provider = provider.Provider(self.view)
        #monkey patch init providers
        self.provider.providers = [utils.FakeConfigurationProvider()]

    def test_get(self):
        mysettings = self.provider.get()
        self.failUnless(len(mysettings.keys()) == 1)
        self.failUnless(mysettings['foo'] == 'bar')

        #test aggregation of providers
        self.provider.providers.append(utils.FakeConfigurationProvider())
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
        #zope interface is the default provider
        self.failUnless(len(self.provider.pnames)==2)
        self.failUnless(self.provider.pnames[0]=='default.zope.interface')
        self.failUnless(self.provider.pnames[1]==self.view.settings_providers[0])
