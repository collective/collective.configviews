"""Store you configuration"""
from zope import component
from zope import interface
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from collective.configviews import interfaces
from persistent.dict import PersistentDict
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

STORAGE_KEY = "collective.configviews"

class AnnotationStorage(object):
    """Implements ConfigStorage with Annotation"""

    interface.implements(interfaces.IConfigurationStorage)
    component.adapts(interfaces.IConfigurableView)

    def __init__(self, view):
        context = view.context.aq_inner
        self.context = context
        self.view = view
        self.schema = view.settings_schema
        self.storage = self._annotations()

    def set(self, configuration):
        """see ISettingsStorage. This implementation take care to save only
        non default values. If other values are found they will be deleted"""

        defaults = self._get_defaults()

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

    def get(self):
        """see IHarlequinStorage. This implementation return all default 
        values of the schema is nothing has already been saved"""

        defaults = self._get_defaults()

        if STORAGE_KEY not in self.storage.keys():
            return defaults

        configuration = defaults
        #is there a faster way to cast persistent dict to dict ?
        for k in configuration.keys():
            if k in self.storage[STORAGE_KEY]:
                configuration[k] = self.storage[STORAGE_KEY][k]

        return configuration

    def _get_defaults(self):
        """Fields are taken from the schema. 
        
        Return a dict with field name as key and field default
        value as value
        """
        
        defaults = self._get_defaults_schema()
        defaults_portal = self._get_defaults_portal()

        #update defaults with portal data:
        for field_name in defaults:
            if field_name in defaults_portal:
                defaults[field_name] = defaults_portal[field_name]

        return defaults

    def _get_defaults_schema(self):
        """Fields are taken from the schema. 
        
        Return a dict with field name as key and field default
        value as value
        """
        fields = schema.getFields(self.schema)
        defaults = {}
        for field_name in fields:
            defaults[field_name] = fields[field_name].default
        return defaults

    def _get_defaults_portal(self):

        registry = component.queryUtility(IRegistry)
        settings = {}
        if registry:
            settings = registry.forInterface(self.schema, check=False)
        return settings

    def _annotations(self):
        """Return the persistent dict that will embed the configuration"""
        return IAnnotations(self.context)

