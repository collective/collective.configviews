import base
import utils


class ConfigurableViewUnitTest(base.UnitTestCase):

    def setUp(self):
        from collective.configviews import ConfigurableBaseView
        context = utils.FakeContext()
        request = {}
        self.view = ConfigurableBaseView(context, request)
        self.view._registry = utils.FakeRegistry()
        self.provider_module = ConfigurableBaseView

    def test_settings(self):
        self.view._settings = {'foo': 'bar'}
        self.assertTrue(self.view.settings['foo'] == 'bar')

    def test_javascripts(self):
        self.view._settings = {'foo': 'bar'}
        t1 = 'collectiveconfigviews = {"foo": "bar"}'
        self.assertTrue(self.view.settings_javascripts() == t1)
        self.view.jsvarname = 'othername'
        t2 = 'othername = {"foo": "bar"}'
        self.assertTrue(self.view.settings_javascripts() == t2)
