Introduction
============

If you need to create a browser view with configuration this add-on will make 
your life easier.

Features:

* Configuration providers
* Configuration structure defined with zope.interface & zope.schema
* Auto form to manage the configuration of the current view

Why doing this in an add-on
===========================

Because most of the time developers faced to this issue store data in the
content type, or with annotation on context without trying to optimize, or without
form, ...

How it works
============

This add-ons define three components:

* IConfigurableView
* IConfigurationProvider
* IConfigurationMutator

The main idea, is you just have to create an zope.interface to define settings
schema and set this schema in the 'settings_schema' attributes of the view.

For example::

    class IMyViewSettings(interface.Interface):
        width = schema.ASCIILine(title=u"Width",
                                 default='620')
 
        height = schema.ASCIILine(title=u"Height",
                                  default='620')

    class MyView(ConfigurableBaseView):
        settings_schema = IMyViewSettings

        def width(self):
            return self.settings['width']

        def height(self):
            return self.settings['height']


IConfigurationProvider
----------------------

This component is responsible to return settings. It has been implemented
in different adapters

Provider (no named adapter): this provider force the use of the 
'default.zope.interface' provider and aggregate all providers specified in the
view throw the settings_provider attributes. Warning: The order is important,
each settings are taken from the last provider which provide it.

'default.zope.interface': this provider return default values of each field of 
the settings schema

'site.plone.app.registry': this provider return values from plone.app.registry
(you have to register your settings_schema as records in registry.xml)

'context.zope.app.annotation': this provider return values stored in annotation
on the context of the view.

'user.plone.app.users': TODO (not implemented yet)

IConfigurationMutator
---------------------

This component is an extension of IConfigurationProvider with the write
settings capabilities (throw its 'set' method). 

'context.zope.app.annontation': this mutator store the configuration in the 
context of the view.

IConfigurableView
-----------------

This component is implemented in a browserview you are supposed to inherits from
in your own browser view.

The default behavior is to use 'context.zope.app.annotation' as mutator and
the following providers:

* default.zope.interface
* site.plone.app.registry
* context.zope.app.annotation

