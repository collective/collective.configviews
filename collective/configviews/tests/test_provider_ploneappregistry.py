import base, utils

class ProviderPloneAppRegistryUnitTest(base.UnitTestCase):

    def setUp(self):
        from collective.configviews import provider
        self.view = utils.FakeConfigurableView()
        self.schema = self.view.settings_schema

        self.provider_module = provider
        self.provider = provider.PloneRegistry(self.view)
        self.provider.fields = {'foo':utils.FakeField('bar'),
                                'boo':utils.FakeField('far')}
        self.provider.registry = utils.FakeRegistry()

    def test_get(self):
        settings = self.provider.get()
        self.failUnless(len(settings)==2)
        self.failUnless(settings['foo']=='bar')
        self.failUnless(settings['boo']=='far')
