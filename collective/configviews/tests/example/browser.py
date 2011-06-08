from collective.configviews import browser
from zope import schema
from zope import interface

class Schema(interface.Interface):
    """A test schema"""
    
    text = schema.TextLine(title=u"Text",
                           default=u"default text value")
    boolean = schema.Bool(title=u"Boolean",
                               default=False)
    int = schema.Int(title=u"Int",
                     default=10)

class Browser(browser.ConfigurableBaseView):
    """A test Browser view"""

    settings_schema = Schema
