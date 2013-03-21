import json
from zope import interface
from plone.app.layout.viewlets.common import ViewletBase
from collective.configviews import interfaces


class ConfigViewlet(ViewletBase):
    """A viewlet which support configuration"""
    interface.implements(interfaces.IConfigurableView)

    jsvarname = "collectiveconfigviewlet"
    settings_schema = interface.Interface
    settings_providers = ('site.plone.app.registry', 'context.zope.annotation')
    settings_mutator = 'context.zope.annotation'

    def update(self):
        super(ConfigViewlet, self).update()
        provider = interfaces.IConfigurationProvider(self)
        self.settings = provider.get()

    def settings_javascripts(self):
        return "%s = %s" % (self.jsvarname, json.dumps(self.settings))
