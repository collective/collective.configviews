from zope import component
from z3c.form import form, button
from plone.autoform.form import AutoExtensibleForm
from plone.z3cform import layout

from collective.configviews import interfaces

class ConfigurationForm(AutoExtensibleForm, form.Form):
    """Form to configure default view"""
    ignoreContext = True
    
    @property
    def schema(self):
        """If viewname is provided in the request it will be used to get the view
        else we use the default view"""
        state = component.queryMultiAdapter((self.context, self.request),
                                            name='plone_context_state')
        url = state.view_url()
        viewname = self.request.get('configviewname', None)
        if viewname is None:
            viewname = self.context.getLayout()
            url = state.canonical_object_url()+'/' +viewname
        view = component.queryMultiAdapter((self.context, self.request),
                                           name=viewname)

        if interfaces.IConfigurableView.providedBy(view):
            return view.settings_schema

        self.request.response.redirect(url)

    @button.buttonAndHandler(u'Save settings')
    def handle_settings(self, action):
        data, errors = self.extractData()
        #TODO: really handle it
        self.status = u"Changed saved."

ConfigurationFormView = layout.wrap_form(ConfigurationForm)
