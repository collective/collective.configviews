from zope import schema
from zope import interface


class IConfigViewsLayer(interface.Interface):
    """ A layer specific to this product.
        Is registered using browserlayer.xml
    """


class IConfigurableView(interface.Interface):
    """Make your view implements this, so you will have all the benefit of this
    add-on"""

    settings = schema.Object(schema.interfaces.IDict)
    jsvarname = schema.ASCIILine(title=u"JavaScript var name")
    settings_schema = schema.Object(interface.interfaces.IInterface)
    settings_providers = schema.List(
        title=u"Settings providers",
        value_type=schema.ASCIILine(title=u"Provider")
    )
    settings_mutator = schema.ASCIILine(title=u"Mutator name")

    def settings_javascripts():
        """Return a string with JavaScript content to declare the
        variable with the settings in json inside"""


class IConfigurationProvider(interface.Interface):
    """Configuration provider"""

    def get():
        """-> dict with configuration like if it was extracted from the form
        """


class IConfigurationMutator(IConfigurationProvider):
    """Configuration storage manager"""

    def set(configuration):
        """Create or update configuration stored in instance."""


class IConfigViewsUtils(interface.Interface):
    """utils"""
    def config_allowed():
        """Check if the current default view is configurable"""
