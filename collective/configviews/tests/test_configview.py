import base, utils

class ConfigurableViewUnitTest(base.UnitTestCase):

    def setUp(self):
        from collective.configviews import ConfigurableBaseView
        context = utils.FakeContext()
        request = {}
        self.view = ConfigurableBaseView(context, request)
        self.view._registry = utils.FakeRegistry()
        self.provider_module = ConfigurableBaseView

    def test_settings(self):
        self.view._settings = {'foo':'bar'}
        self.failUnless(self.view.settings['foo'] == 'bar')
    
    def test_javascripts(self):
        self.view._settings = {'foo':'bar'}
        self.failUnless(self.view.settings_javascripts()=='collectiveconfigviews = {"foo": "bar"}')
        self.view.jsvarname = 'othername'
        self.failUnless(self.view.settings_javascripts()=='othername = {"foo": "bar"}')

