from persistent.dict import PersistentDict
from zope import interface
from zope import schema

from collective.configviews import provider, interfaces

STORAGE_KEY = provider.STORAGE_KEY

class ZopeAnnotation(provider.ZopeAnnotation):
    """Mutator based on annotation"""
    interface.implements(interfaces.IConfigurationMutator)

    def set(self, configuration):
        """see ISettingsStorage. This implementation take care to save only
        non default values. If other values are found they will be deleted"""

        defaults = self.get_defaults()

        #faster than parsing and cleanup:
        if STORAGE_KEY in self.storage:
            #be sure ZODB remove this
            del self.storage[STORAGE_KEY]

        self.storage[STORAGE_KEY] = PersistentDict()

        for key in configuration:
            if key not in defaults:
                continue
            if configuration[key] == defaults[key]:
                continue
            self.storage[STORAGE_KEY][key] = configuration[key]

    def get_defaults(self):
        """This method return defaults values for the current view"""
        fields = schema.getFields(self.schema)
        defaults = {}
        for field_name in fields:
            defaults[field_name] = fields[field_name].default
        return defaults
