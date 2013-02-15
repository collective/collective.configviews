from collective.configviews.tests import base
from collective.configviews.tests import fake


class ProviderZopeAnnotationUnitTest(base.UnitTestCase):

    def setUp(self):
        from collective.configviews import provider
        self.view = fake.FakeConfigurableView()
        self.schema = self.view.settings_schema

        self.provider_module = provider
        self.provider = provider.ZopeAnnotation(self.view)
        test_settings = {'foo': 'new'}
        self.provider.annotation = {provider.STORAGE_KEY: test_settings}
        self.provider.fields = {'foo': fake.FakeField('bar'),
                                'boo': fake.FakeField('far')}

    def test_get(self):
        settings = self.provider.get()
        self.failUnless(len(settings) == 1)
        self.failUnless(settings['foo'] == 'new')
