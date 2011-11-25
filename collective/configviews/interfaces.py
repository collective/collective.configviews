from zope import schema
from zope import interface

# -*- Additional Imports Here -*-


class IConfigViewsLayer(interface.Interface):
    """ A layer specific to this product. 
        Is registered using browserlayer.xml
    """

class IConfigurableView(interface.Interface):
    """Make your view implements this, so you will have all the benefit of this
    add-on"""

    settings = schema.Object(title=u"Settings object",
                             schema=schema.interfaces.IObject)

    settings_dict = schema.Object(title=u"Settings dict",
                             schema=schema.interfaces.IDict)

    jsvarname = schema.ASCIILine(title=u"JavaScript var name")

    settings_schema = schema.Object(title=u"Schema",
                                    schema=interface.interfaces.IInterface)

    def settings_javascripts():
        """Return a string with JavaScript content to declare the
        variable with the settings in json inside.
        
        myjsvarname = {'setting_attribute_1':'setting_value_1', ...}
        """

class IConfigurationStorage(interface.Interface):
    """Storage for configuration aka registry."""

    def settings():
        """return an object that implement the schema"""

    def settings_dict():
        """return settings value as a dict wehere keys are attributes."""

    def update(values):
        """values must be a dict like object to update values of the
        configuration."""


class IConfigViewsUtils(interface.Interface):
    """utils"""

    def config_allowed():
        """Check if the current default view is configurable"""
