import base, utils


class ProviderInterfaceDefaultUnitTest(base.UnitTestCase):

    def setUp(self):
        from collective.configviews import provider
        self.view = utils.FakeConfigurableView()
        self.schema = self.view.settings_schema
        
        self.provider_module = provider
        self.provider = provider.InterfaceDefault(self.view)
        self.provider.fields = {'foo':utils.FakeField('bar'),
                                'boo':utils.FakeField('far')}

    def test_get(self):
        settings = self.provider.get()
        self.failUnless(len(settings)==2)
        self.failUnless(settings['foo']=='bar')
        self.failUnless(settings['boo']=='far')
