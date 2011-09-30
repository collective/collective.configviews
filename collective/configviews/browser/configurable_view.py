import json

from zope import interface

from Products.Five import BrowserView

from collective.configviews import interfaces
from collective.configviews.registry import Registry
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ConfigurableBaseView(BrowserView):
    """Base browserview make it configurable view"""

    interface.implements(interfaces.IConfigurableView)

    jsvarname = "collectiveconfigviews"
    settings_schema = interface.Interface
    settings_prefix = 'base'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._settings = None
        self._registry = None

    def initialize(self):
        if self._registry is None:
            self._registry = Registry(self)

    @property
    def settings(self):
        """See interface IConfigurableView"""
        if not self._settings:
            self.initialize()
            self._settings = self._registry.get()

        return self._settings

    def settings_javascripts(self):
        return "%s = %s"%(self.jsvarname, json.dumps(self.settings))

from zope import schema

class ExampleSchema(interface.Interface):
    foo = schema.Bool(title=u"foo", default=True)
    bar = schema.ASCIILine(title=u"bar",default="")
    
class Example(ConfigurableBaseView):
    settings_schema = ExampleSchema

    __call__ = ViewPageTemplateFile('example.pt')