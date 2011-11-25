import json

from zope import interface

from Products.Five import BrowserView

from collective.configviews import interfaces
from collective.configviews.registry import Registry

class ConfigurableBaseView(BrowserView):
    """Base browserview make it configurable view"""

    interface.implements(interfaces.IConfigurableView)

    jsvarname = "collectiveconfigviews"
    settings_schema = interface.Interface
#    settings_prefix = 'base'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._settings = None
        self._registry = None

    def initialize(self):
        if self._registry is None:
            self._registry = Registry(self)
        if self._settings is None:
            self._settings = self._registry.settings_dict()

    @property
    def settings(self):
        """See interface IConfigurableView"""
        self.initialize()

        return self._settings

    def settings_javascripts(self):
        return "%s = %s"%(self.jsvarname, json.dumps(self.settings))
