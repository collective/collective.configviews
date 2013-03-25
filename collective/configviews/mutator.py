from persistent.dict import PersistentDict
from zope import interface

from collective.configviews import provider, interfaces
from collective.configviews.provider import InterfaceDefault

STORAGE_KEY = provider.STORAGE_KEY


class ZopeAnnotation(provider.ZopeAnnotation):
    """Mutator based on annotation"""
    interface.implements(interfaces.IConfigurationMutator)

    def set(self, configuration):
        """see ISettingsStorage. This implementation take care to save only
        non default values. If other values are found they will be deleted"""
        annotation = self.getAnnotation()
        defaults = self.get_defaults()

        #faster than parsing and cleanup:
        if STORAGE_KEY in annotation:
            #be sure ZODB remove this
            del annotation[STORAGE_KEY]

        annotation[STORAGE_KEY] = PersistentDict()

        for key in configuration:
            if key not in defaults:
                continue
            if configuration[key] == defaults[key]:
                continue
            annotation[STORAGE_KEY][key] = configuration[key]

    def get_defaults(self):
        """This method return defaults values for the current view"""
        return InterfaceDefault.get(self)
