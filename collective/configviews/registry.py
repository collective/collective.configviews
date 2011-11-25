from zope import component
from zope import interface
from zope import schema

from plone.registry.interfaces import IRegistry

from collective.configviews import interfaces

class Proxy(object):
    def __init__(self, registry, schema):
        self.__registry__ = registry
        self.__schema__ = schema
    
    def __getattr__(self, name):
        if name not in self.__schema__:
            raise AttributeError(name)
        value = self.__registry__.get().get(name, None)
        if value is None:
            value = self.__schema__[name].missing_value
        return value

class Registry(object):
    """Aggregate portal_registry and contextual_registry."""

    interface.implements(interfaces.IConfigurationStorage)

    def __init__(self, context):
        self.view = context
        self.prefix = str(self.view.__name__)
        self.schema = self.view.settings_schema
        self.context = context.context
        self._settings = None
        self._registry = None
        self._site_registry = None
        self._records = None
        self._site_records = None
        self._fields = None
        self._proxy = None

    def initialize(self):
        if self._site_registry is None:
            self._site_registry = component.queryUtility(IRegistry)
        if self._registry is None:
            self._registry = component.queryAdapter(self.context,
                                                    IRegistry)
        if self._records is None:
            self._records = self._registry.forInterface(self.schema,
                                                        prefix=self.prefix,
                                                        check=False)
        if self._site_records is None:
            self._site_records = self._site_registry.forInterface(self.schema,
                                                        prefix=self.prefix,
                                                        check=False)
        if self._fields is None:
            self._fields = schema.getFields(self.schema)
        
        if self._proxy is None:
            self._proxy = Proxy(self, self.schema)


    def settings(self):
        self.initialize()
        return self._proxy
    
    def settings_dict(self):
        return self.get()

    def get(self):
        """Return settings as dict loaded in the current order: interface,
        portal_registry, context_registry"""

        if self._settings is None:
            self._settings = {}
            self.initialize()
            fields = self._fields
            #first load interface defaults
            for field in fields:
                self._settings[field] = fields[field].default
            #next override by site values
            proxy = self._site_records
            for field in fields:
                value = getattr(proxy, field)
                if value is not None:
                    self._settings[field] = value
            #finaly try to load context values
            proxy =self._records
            for field in fields:
                value = getattr(proxy, field)
                if value is not None:
                    self._settings[field] = value

        return self._settings

    def update(self, values):
        self.initialize()
        try:
            self._records = self._registry.forInterface(self.schema,
                                                        prefix=self.prefix)
        except KeyError, e:
            self._registry.registerInterface(self.schema,
                                             prefix=self.prefix)
            self._records = self._registry.forInterface(self.schema,
                                                        prefix=self.prefix)

        for field in self._fields:
            value = values.get(field,None)
            if value is None:
                continue
            setattr(self._records, field, value)

        #invalidate cache on settings:
        self._settings = None
    
        return self._fields
