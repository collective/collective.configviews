import logging
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('collective.configviews')

def upgrade_to_2000(context):
    """We need to migrate all configviews anotation to the new system.
    It will be done by trying to register the schema in the local registry
    and then apply field by field value"""
    from zope import component
    from zope import schema
    from zope.annotation.interfaces import IAnnotations
    from plone.registry.interfaces import IRegistry

    STORAGE_KEY = "collective.configviews"
    
    catalog = getToolByName(context, 'portal_catalog')
    typestool = getToolByName(context, 'portal_types')
    for type_ in typestool.listContentTypes():
        brains = catalog(portal_type=type_)
        for brain in brains:
            ob = brain.getObject()
            annotation = IAnnotations(ob)
            
            if STORAGE_KEY not in annotation.keys():
                continue
            else:
                settings_value = annotation[STORAGE_KEY]
                lregistry = IRegistry(ob)
                lregistry.initialize_registry()
                layout = ob.getLayout()
                view = component.queryMultiAdapter((ob, ob.REQUEST),
                                                   name=layout)
                if view is None:
                    logger.info('we have found settings, but not on default view. -> delete')
                    del annotation[STORAGE_KEY]
                    continue
                if not hasattr(view, 'settings_schema'):
                    logger.info('we have found settings, but not on default view. -> delete')
                    del annotation[STORAGE_KEY]
                    continue

                settings_schema = view.settings_schema

                try:
                    proxy = lregistry.forInterface(settings_schema)
                except KeyError,e:
                    lregistry.registerInterface(settings_schema)
                    proxy = lregistry.forInterface(settings_schema)
                
                for key in settings_value:
                    #key == field name
                    setattr(proxy, key, settings_value[key])
                
                logger.info('configviews of %s migrated'%ob.absolute_url())
                del annotation[STORAGE_KEY]
