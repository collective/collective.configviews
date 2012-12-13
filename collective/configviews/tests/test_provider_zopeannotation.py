import base, utils

class ProviderZopeAnnotationUnitTest(base.UnitTestCase):

    def setUp(self):
        from collective.configviews import provider
        self.view = utils.FakeConfigurableView()
        self.schema = self.view.settings_schema

        self.provider_module = provider
        self.provider = provider.ZopeAnnotation(self.view)
        test_settings = {'foo':'new'}
        self.provider.annotation = {provider.STORAGE_KEY:test_settings}
        self.provider.fields = {'foo':utils.FakeField('bar'),
                                'boo':utils.FakeField('far')}

    def test_get(self):
        settings = self.provider.get()
        self.failUnless(len(settings)==1)
        self.failUnless(settings['foo']=='new')
