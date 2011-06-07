from zope import interface
from zope import schema
from plone.app.layout.globals.interfaces import IViewView

class IConfigurableView(interface.Interface):
    """Make your view implements this, so you will have all the benefit of this
    add-on"""

    settings = schema.Object(schema.interfaces.IDict)
    jsvarname = schema.ASCIILine(title=u"JavaScript var name")
    settings_schema = schema = schema.Object(interface.interfaces.IInterface)

    def settings_javascripts():
        """Return a string with JavaScript content to declare the
        variable with the settings in json inside"""
