from collective.configviews.tests import base
from collective.configviews.tests import fake


class ProviderPloneAppRegistryUnitTest(base.UnitTestCase):

    def setUp(self):
        from collective.configviews import provider
        self.view = fake.FakeConfigurableView()
        self.schema = self.view.settings_schema

        self.provider_module = provider
        self.provider = provider.PloneRegistry(self.view)
        self.provider.fields = {'foo': fake.FakeField('bar'),
                                'boo': fake.FakeField('far')}
        self.provider.registry = fake.FakeRegistry()

    def test_get(self):
        settings = self.provider.get()
        self.failUnless(len(settings) == 2)
        self.failUnless(settings['foo'] == 'bar')
        self.failUnless(settings['boo'] == 'far')
