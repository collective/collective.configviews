from persistent.dict import PersistentDict
from zope import interface
from zope import schema

from collective.configviews import provider, interfaces

STORAGE_KEY = provider.STORAGE_KEY

class ZopeAnnotation(provider.ZopeAnnotation):
    """Mutator based on annotation"""
    interface.implements(interfaces.IConfigurationMutator)

    def __init__(self, view):
        super(ZopeAnnotation,self).__init__(view)
        self._provider = None

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
        provider = self.get_provider()
        #we are storing in annotation, so we want value outside of this provider
        if 'context.zope.annotation' in provider.pnames:
            pnames = list(provider.pnames)
            pnames.remove('context.zope.annotation')
            provider.pnames = pnames

        return provider.get()

    def get_provider(self):
        if self._provider is None:
            self._provider = interfaces.IConfigurationProvider(self.view)
        return self._provider
