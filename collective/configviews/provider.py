from zope import component
from zope import interface
from zope import schema
from zope.annotation.interfaces import IAnnotations

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
        self.fields = []

    def get(self):
        fields = self.getFields()
        configuration = {}
        for field_name in fields:
            configuration[field_name] = fields[field_name].default
        return configuration

    def getFields(self):
        if not self.fields:
            self.fields = schema.getFields(self.schema)
        return self.fields


class PloneRegistry(InterfaceDefault):
    """Configuration provider based on plone.app.registry"""
    interface.implements(interfaces.IConfigurationProvider)
    component.adapts(interfaces.IConfigurableView)

    def __init__(self, view):
        super(PloneRegistry, self).__init__(view)
        self.registry = None

    def get(self):
        fields = self.getFields()
        registry = self.getRegistry()
        settings = {}

        if registry:
            proxy = registry.forInterface(self.schema, check=False)
            for field in fields:
                value = getattr(proxy, field)
                if value is not None:
                    settings[field] = value

        return settings

    def getRegistry(self):
        if not self.registry:
            self.registry = component.queryUtility(IRegistry)
        return self.registry


class ZopeAnnotation(InterfaceDefault):
    """Implements ConfigProvider with Annotation"""

    interface.implements(interfaces.IConfigurationProvider)
    component.adapts(interfaces.IConfigurableView)

    def __init__(self, view):
        super(ZopeAnnotation, self).__init__(view)
        self.annotation = None

    def get(self):
        """see IHarlequinStorage. This implementation return all default
        values of the schema is nothing has already been saved"""
        annotation = self.getAnnotation()
        if STORAGE_KEY not in annotation.keys():
            return {}

        return annotation[STORAGE_KEY]

    def getAnnotation(self):
        """Return the persistent dict that will embed the configuration"""
        if self.annotation is None:
            self.annotation = IAnnotations(self.context)
        return self.annotation


class Provider(InterfaceDefault):
    """Aggregator of named providers"""

    def __init__(self, view):
        super(Provider, self).__init__(view)
        self.pnames = view.settings_providers
        self.providers = []
        self.configuration = {}

    def get(self):
        if self.configuration:
            return self.configuration

        self.init_providers()
        self.configuration = super(Provider, self).get()  # load defaults

        for provider in self.providers:
            configuration = provider.get()
            for key in configuration:
                self.configuration[key] = configuration[key]

        return self.configuration

    def init_providers(self):
        if len(self.providers) > 1:
            return

        for pname in self.pnames:
            adapter = component.queryAdapter(self.view,
                                             interfaces.IConfigurationProvider,
                                             pname)
            if adapter is not None:
                self.providers.append(adapter)
