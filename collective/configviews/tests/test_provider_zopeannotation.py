import base, utils

class ProviderZopeAnnotationUnitTest(base.UnitTestCase):

    def setUp(self):
        from collective.configviews import provider
        self.view = utils.FakeConfigurableView()
        self.schema = self.view.settings_schema

        self.provider_module = provider
        self.provider = provider.ZopeAnnotation(self.view)
        test_settings = {'foo':'bar', 'boo':'far'}
        self.provider.annotation = {provider.STORAGE_KEY:test_settings}

    def test_get(self):
        settings = self.provider.get()
        self.failUnless(len(settings)==2)
        self.failUnless(settings['foo']=='bar')
        self.failUnless(settings['boo']=='far')
