import json
from zope import interface
from zope import schema

from Products.Five import BrowserView
from Products.Five import metaclass

from collective.configviews import interfaces

class ConfigurableBaseView(BrowserView):
    """Base browserview make it configurable view"""

    interface.implements(interfaces.IConfigurableView)

    jsvarname = "collectiveconfigviews"
    settings_schema = interface.Interface

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._settings_storage = None
        self._settings = None
        self._settings_form = None

    @property
    def settings(self):
        """See interface IConfigurableView"""
        if not self._settings_storage:
            self._settings_storage = interfaces.IConfigurationStorage(self)
        if not self._settings:
            self._settings = self._settings_storage.get()

        return self._settings

    def settings_javascripts(self):
        return "%s = %s"%(self.jsvarname, json.dumps(self.settings))
