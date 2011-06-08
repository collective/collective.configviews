from zope import component
from zope import interface
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable

from plone.registry.interfaces import IRegistry

from collective.configviews import interfaces

STORAGE_KEY = "collective.configviews"

class InterfaceDefault(object):
    """Implements IConfigurationProvider with Interface fields default"""

    interface.implements(interfaces.IConfigurationProvider)
    component.adapts(interfaces.IConfigurableView)

    def __init__(self, view):
        context = view.context.aq_inner
        self.context = context
        self.view = view
        self.schema = view.settings_schema

    def get(self):
        fields = schema.getFields(self.schema)
        configuration = {}
        for field_name in fields:
            configuration[field_name] = fields[field_name].default
        return configuration

class PloneRegistry(object):
    """Configuration provider based on plone.app.registry"""
    interface.implements(interfaces.IConfigurationProvider)
    component.adapts(interfaces.IConfigurableView)

    def __init__(self, view):
        context = view.context.aq_inner
        self.context = context
        self.view = view
        self.schema = view.settings_schema

    def get(self):
        fields = schema.getFields(self.schema)
        registry = component.queryUtility(IRegistry)
        settings = {}
        if registry:
            proxy = registry.forInterface(self.schema, check=False)
            for field in fields:
                settings[field] = getattr(proxy, field)
        return settings

class ZopeAnnotation(object):
    """Implements ConfigProvider with Annotation"""

    interface.implements(interfaces.IConfigurationProvider)
    component.adapts(interfaces.IConfigurableView)

    def __init__(self, view):
        context = view.context.aq_inner
        self.context = context
        self.view = view
        self.schema = view.settings_schema
        self.storage = self._annotations()

    def get(self):
        """see IHarlequinStorage. This implementation return all default 
        values of the schema is nothing has already been saved"""

        if STORAGE_KEY not in self.storage.keys():
            return {}

        return self.storage[STORAGE_KEY]

    def _annotations(self):
        """Return the persistent dict that will embed the configuration"""
        return IAnnotations(self.context)

class Provider(object):
    """Aggregator of named providers"""
    interface.implements(interfaces.IConfigurationProvider)
    component.adapts(interfaces.IConfigurableView)

    def __init__(self, view):
        context = view.context.aq_inner
        self.context = context
        self.view = view
        self.schema = view.settings_schema
        self.pnames = ['default.zope.interface']
        self.pnames.extend(view.settings_providers)
        self.providers = []
        self.configuration = {}

    def get(self):
        if self.configuration:
            return self.configuration

        self.init_providers()

        for provider in self.providers:
            configuration = provider.get()
            for key in configuration:
                self.configuration[key] = configuration[key]

        return self.configuration

    def init_providers(self):
        if len(self.providers)>1:return

        for pname in self.pnames:
            adapter = component.queryAdapter(self.view,
                                             interfaces.IConfigurationProvider,
                                             pname)
            if adapter is not None:
                self.providers.append(adapter)
