from zope import component
from zope import schema
from plone.registry.interfaces import IRegistry

class Registry(object):
    
    def __init__(self, context):
        self.view = context
        self.schema = self.view.settings_schema
        self.context = context.context
        self._settings = None
        self._registry = None
        self._site_registry = None
        self._records = None
        self._site_records = None

    def initialize(self):
        if self._site_registry is None:
            self._site_registry = component.queryUtility(IRegistry)
        if self._registry is None:
            self._registry = component.queryAdapter(self.context,
                                                    IRegistry)
        if self._records is None:
            self._records = self._registry.forInterface(self.schema,
                                                        check=False)
        if self._site_records is None:
            self._site_records = self._site_registry.forInterface(self.schema,
                                                        check=False)

    def get(self):
        """Return settings as dict loaded in the current order: interface,
        portal_registry, context_registry"""

        if not self._settings:
            import pdb;pdb.set_trace()
            self._settings = {}
            self.initialize()
            fields = schema.getFields(self.schema)
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
        fields = schema.getFields(self.schema)
        for field in fields:
            self._records[field] = values[field]
