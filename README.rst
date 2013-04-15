Introduction
============

This add-on does not provide feature to Plone.
It is intended to plone add-ons developers.

It provides base class to let your view being configurable (ie have 'settings').

Features:

* Configuration providers
* Configuration structure defined with zope.interface & zope.schema
* Store configuration using plugins
* Generated form from the schema to let owner configure the current view

Notes on VERSIONS
=================


.. image:: https://secure.travis-ci.org/collective/collective.configviews.png
    :target: http://travis-ci.org/collective/collective.configviews


3.0 is a back to 1.0.

2.0 branch was about to use plone.app.registry on the context using
collective.registry. After doing this the addon loose the ability to have
optimized settings (mixin of globals and locals). So lets revert this and
continue the 1.0 in 3.0 !

Why doing this in an add-on
===========================

Because most of the time developers faced to this issue store data in the
content type, or with annotation on context without trying to optimize,
or without form, ...

How it works
============

This add-ons define three components:

* ConfigurableView
* ConfigurationProvider
* ConfigurationMutator

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
            return self.settings.width

        def height(self):
            return self.settings.height


IConfigurationProvider
======================

This component is responsible to return settings. 
It has been implemented in different adapters

Provider (no named adapter): this provider load default values from the 
interface fields defaults values and it let other providers override values.
It is an aggregation of all providers specified in the view throw the
settings_providers attribute. Warning: The order is important, each settings
are taken from the last provider which provide it.

'site.plone.app.registry': this provider return values from plone.app.registry
(you have to register your settings_schema as records in registry.xml)

'context.zope.app.annotation': this provider return values stored in annotation
on the context of the view.

IConfigurationMutator
=====================

This component is an extension of IConfigurationProvider with the write
settings capabilities (throw its 'set' method).

'context.zope.app.annontation': this mutator store the configuration in
the context of the view.

IConfigurableView
=================

This component is implemented in a browserview you are supposed to inherits
from in your own browser view.

The default behavior is to use 'context.zope.app.annotation' as mutator and
the following providers:

* site.plone.app.registry
* context.zope.app.annotation

Common use case: use a javascript library for a view
====================================================

Most of javascript libraries wait for a dict to load their configuration. You
can achieve this in a very easy way. You just have to define a configuration
schema and add the following snippet in your template to create a javascript
variable with the configuration ::

  <script type="text/javascript" tal:content="view/settings_javascripts"></script>

You can set the variable name throw the jsvarname attribute of your browserview.

You will find examples in the following addons:

* collective.galleria
* collective.galleriffic
* collective.googledocsviewer

Credits
=======

Companies
---------

|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact us <mailto:python@makina-corpus.org>`_

People
------

- JeanMichel FRANCOIS aka toutpt <toutpt@gmail.com>
- Radim Novotny aka naro

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com
