from zope import component
from zope import interface
from zope import schema
from z3c.form import form, button
from plone.autoform.form import AutoExtensibleForm
from plone.z3cform import layout

from collective.configviews import interfaces

from Products.Five import BrowserView
from collective.configviews.registry import Registry
from plone.autoform.interfaces import MODES_KEY

class IInternalConfigurationSchema(interface.Interface):
    viewname = schema.TextLine(title=u"view name")

IInternalConfigurationSchema.setTaggedValue(MODES_KEY,
                            [(interface.Interface, 'viewname','hidden')])

class ConfigurationForm(AutoExtensibleForm, form.EditForm):
    """Form to configure default view"""

    additionalSchemata = (IInternalConfigurationSchema,)

    def update(self):
        super(ConfigurationForm, self).update()
        #update viewname field
        for widgetkey in self.widgets:
            widget = self.widgets[widgetkey]
            name = widget.field.getName()
            if name == 'viewname' and not widget.value:
                viewname = self.getViewName()
                widget.value = viewname

    def getContent(self):

        registry = self.getRegistry()
        settings = registry.settings_dict()
        return settings

    @property
    def schema(self):
        """If viewname is provided in the request it will be used to get the view
        else we use the default view"""
        state = component.queryMultiAdapter((self.context, self.request),
                                            name='plone_context_state')
        url = state.view_url()
        view = self.getView()
        if view is not None:
            return view.settings_schema

        self.request.response.redirect(url)

    @button.buttonAndHandler(u'Save settings')
    def handle_settings(self, action):
        data, errors = self.extractData()

        view = self.getView()
        if view is None:
            #TODO: handle errors
            return

        registry = self.getRegistry()
        registry.update(data)
        self.status = u"Changed saved."

        state = component.queryMultiAdapter((self.context, self.request),
                                            name='plone_context_state')
        url = state.view_url()
        self.request.response.redirect(url)

    def getView(self):

        viewname = self.getViewName()
        view = component.queryMultiAdapter((self.context, self.request),
                                           name=viewname)
        if not interfaces.IConfigurableView.providedBy(view):
            return
        return view

    def getViewName(self):
        viewname = self.request.form.get('viewname',None)
        if viewname is None:
            z3viewkey = 'form.widgets.IInternalConfigurationSchema.viewname'
            viewname = self.request.form.get(z3viewkey, None)
        if viewname is None:
            viewname = self.context.getLayout()
        return viewname

    def getRegistry(self):
        view = self.getView()
        if view is not None:
            return Registry(view)

ConfigurationFormView = layout.wrap_form(ConfigurationForm)


class Utils(BrowserView):
    """Utils view"""
    
    def config_allowed(self):
        """permission is already checked by zope, here we are checking if
        current view is a configurable view"""
        viewname = self.context.getLayout()
        view = component.queryMultiAdapter((self.context, self.request),
                                           name=viewname)
        return interfaces.IConfigurableView.providedBy(view)
