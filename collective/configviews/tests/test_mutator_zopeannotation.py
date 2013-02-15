from collective.configviews.tests import base
from collective.configviews.tests import fake


class MutatorZopeAnnotationUnitTest(base.UnitTestCase):

    def setUp(self):
        from collective.configviews import mutator
        self.view = fake.FakeConfigurableView()
        self.schema = self.view.settings_schema
        self.key = mutator.STORAGE_KEY

        self.mutator_module = mutator
        self.mutator = mutator.ZopeAnnotation(self.view)
        self.mutator.annotation = {self.key: {}}
        self.mutator.fields = {'foo': fake.FakeField('bar'),
                               'boo': fake.FakeField('far')}

    def test_set(self):
        settings = self.mutator.get()
        settings['foo'] = 'great'
        settings['boo'] = 'far'  # default should not be written
        settings['new'] = 'one'
        self.mutator.set(settings)
        self.assertTrue(len(settings) == 3)
        self.assertTrue(settings['foo'] == 'great')
        self.assertTrue(settings['boo'] == 'far')
        self.assertTrue(settings['new'] == 'one')
        annotation = self.mutator.annotation
        #default should not be written
        self.assertTrue('boo' not in annotation[self.key].keys())

    def test_get_defaults(self):
        settings = self.mutator.get_defaults()
        self.assertTrue(settings['foo'] == 'bar')
        self.assertTrue(settings['boo'] == 'far')
