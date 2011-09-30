import base, utils

class RegistryUnitTest(base.UnitTestCase):

    def setUp(self):
        from collective.configviews import registry
        self.view = utils.FakeConfigurableView()
        self.provider_module = registry
        self.registry = registry.Registry(self.view)
        self.registry._fields = {}
        self.registry._fields['foo'] = utils.FakeField('foo', 'bar')
        self.registry._fields['boo'] = utils.FakeField('foo', 'bar')
        self.registry._site_registry = utils.FakeRegistry()
        self.registry._registry = utils.FakeRegistry()

    def test_get(self):
        mysettings = self.registry.get()
        self.failUnless(len(mysettings.keys()) == 2, 'settings keys = %s'%len(mysettings.keys()))
        self.failUnless(mysettings['foo'] == 'bar')
        self.failUnless(mysettings['boo'] == 'far')

    def test_update(self):
        pass

