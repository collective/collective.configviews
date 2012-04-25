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
        self.registry.initialize()

    def test_settings_dict(self):
        mysettings = self.registry.settings_dict()
        self.assertTrue(len(mysettings.keys()) == 2,
                        'settings keys = %s'%len(mysettings.keys()))
        self.assertTrue(mysettings['foo'] == 'bar')
        self.assertTrue(mysettings['boo'] == 'far')

    def test_settings(self):
        settings = self.registry.settings()
        settings.foo
        self.assertTrue(settings.foo == 'bar')
        self.assertTrue(settings.boo == 'far')

    def test_update(self):
        values = {'foo':'foo'}
        self.assertTrue(self.registry.get()['foo']=='bar')
        self.registry.update(values)
        self.assertTrue(getattr(self.registry._records,'foo',None)=='foo')
        #check other has not changed
        self.assertTrue(getattr(self.registry._records,'boo',None)=='far')
        #check cache has been invalidated
        self.assertTrue(self.registry.get()['foo']=='foo')

        values = {'notexisting':'shouldnotberegistred'}
        self.registry.update(values)
        self.assertTrue(self.registry.get().get('notexisting',None) is None)

