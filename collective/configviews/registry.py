from zope import component
from zope import schema
from plone.registry.interfaces import IRegistry

class Registry(object):
    
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

    def get(self):
        """Return settings as dict loaded in the current order: interface,
        portal_registry, context_registry"""

        if not self._settings:
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

        fields = schema.getFields(self.schema)
        for field in fields:
            value = values.get(field)
            if value is None:
                continue
            setattr(self._records, field, value)
    
        return self._fields
