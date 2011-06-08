import base, utils

class MutatorZopeAnnotationUnitTest(base.UnitTestCase):

    def setUp(self):
        from collective.configviews import mutator
        self.view = utils.FakeConfigurableView()
        self.schema = self.view.settings_schema
        self.key = mutator.STORAGE_KEY

        self.mutator_module = mutator
        self.mutator = mutator.ZopeAnnotation(self.view)
        self.mutator.annotation = {self.key:{}}
        self.mutator.fields = {'foo':utils.FakeField('bar'),
                                'boo':utils.FakeField('far')}

    def test_set(self):
        settings = self.mutator.get()
        settings['foo'] = 'great'
        settings['boo'] = 'far' #default should not be written
        settings['new'] = 'one'
        self.mutator.set(settings)
        self.failUnless(len(settings)==3)
        self.failUnless(settings['foo']=='great')
        self.failUnless(settings['boo']=='far')
        self.failUnless(settings['new']=='one')
        annotation = self.mutator.annotation
        #default should not be written
        self.failUnless('boo' not in annotation[self.key].keys())

    def test_get_defaults(self):
        settings = self.mutator.get_defaults()
        self.failUnless(settings['foo']=='bar')
        self.failUnless(settings['boo']=='far')

