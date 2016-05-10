# -*- coding: utf-8 -*-

from zope import component
from z3c.form import form, button
from plone.autoform.form import AutoExtensibleForm
from plone.z3cform import layout
from collective.configviews import interfaces
from Products.Five import BrowserView
from .. import _


class ConfigurationForm(AutoExtensibleForm, form.EditForm):
    """Form to configure default view"""

    def getContent(self):
        provider = self.getProvider()
        return provider.get()

    @property
    def schema(self):
        """If viewname is provided in the request it will be used
        to get the view else we use the default view"""
        state = component.queryMultiAdapter((self.context, self.request),
                                            name='plone_context_state')
        url = state.view_url()
        view = self.getView()
        if view is not None:
            return view.settings_schema

        self.request.response.redirect(url)

    @button.buttonAndHandler(_(u'Save settings'))
    def handle_settings(self, action):
        data, errors = self.extractData()
        view = self.getView()
        if view is None:
            #TODO: handle errors
            return

        mutator = self.getMutator()
        mutator.set(data)
        self.status = u"Changed saved."

        state = component.queryMultiAdapter((self.context, self.request),
                                            name='plone_context_state')
        url = state.view_url()
        self.request.response.redirect(url)

    def getView(self):
        viewname = self.context.getLayout()
        view = component.queryMultiAdapter((self.context, self.request),
                                           name=viewname)
        if not interfaces.IConfigurableView.providedBy(view):
            return
        return view

    def getProvider(self):
        view = self.getView()
        return interfaces.IConfigurationProvider(view)

    def getMutator(self):
        view = self.getView()
        name = view.settings_mutator
        adapter = component.queryAdapter(
            view,
            interfaces.IConfigurationMutator,
            name
        )
        return adapter


ConfigurationFormView = layout.wrap_form(ConfigurationForm)


class Utils(BrowserView):
    """Utils view"""

    def config_allowed(self):
        #TODO: permission is already checked by plone
        viewname = self.context.getLayout()
        view = component.queryMultiAdapter((self.context, self.request),
                                           name=viewname)
        return interfaces.IConfigurableView.providedBy(view)
