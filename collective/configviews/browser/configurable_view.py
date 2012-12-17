import json

from zope import interface
from Products.Five.browser import BrowserView

from collective.configviews import interfaces


class ConfigurableBaseView(BrowserView):
    """Base browserview make it configurable view"""

    interface.implements(interfaces.IConfigurableView)

    jsvarname = "collectiveconfigviews"
    settings_schema = interface.Interface
    settings_providers = ('site.plone.app.registry', 'context.zope.annotation')
    settings_mutator = 'context.zope.annotation'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._settings = None

    @property
    def settings(self):
        """See interface IConfigurableView"""
        if not self._settings:
            provider = interfaces.IConfigurationProvider(self)
            self._settings = provider.get()

        return self._settings

    def settings_javascripts(self):
        return "%s = %s" % (self.jsvarname, json.dumps(self.settings))
