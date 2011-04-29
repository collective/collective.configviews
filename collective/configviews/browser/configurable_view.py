import json
from zope import interface
from zope import schema

from Products.Five import BrowserView
from Products.Five import metaclass

from collective.configviews import interfaces

class ConfigurableBaseView(BrowserView):
    """Base browserview make it configurable view"""

    interface.implements(interfaces.IConfigurableView)

    jsvarname = "collectiveconfigviews"
    settings_schema = interface.Interface

    def __init__(self, context, request):
        """See interface"""
        self.context = context
        self.request = request
        self._settings_storage = None
        self._settings = None
        self._settings_form = None

    def get_settings(self):
        """Accessor to harlequin_config."""
        if not self._settings_storage:
            self._settings_storage = interfaces.IConfigurationStorage(self)
        if not self._settings:
            self._settings = self._settings_storage.get()
        
        return self._settings

    def set_settings(self, configuration):
        """Mutator"""
        if not self._settings_storage:
            self._settings_storage = interfaces.IConfigurationStorage(self)
        return self._settings_storage.set(configuration)

    settings = property(get_settings, set_settings)

    def get_settings_form(self):
        """Accessor to harlequin_form."""

        if not self._settings_form:
            self._settings_form = self.__create_form_page()

        return self._harlequin_form

    def set_settings_form(self, formpage):
       """Mutator to harlequin_form."""
       self._settings_form = formpage

    settings_form   = property(get_settings_form, set_settings_form)


    def __create_form_page(self):
        """Create a form page based on the schema"""
        return "my html form"
#        form = metaclass.makeClass('HarlequinMetaForm',(forms.Form,), {})
#        form.fields = forms.field.Fields(self.harlequin_schema)
#        form.label = _("Harlequin dynamic configuration form")
#        return layout.wrap_form(form)

    def settings_javascripts(self):
        return "%s = %s"%(self.jsvarname, json.dumps(self.settings))
