Introduction
============

This add-on does not provide new feature to Plone. It is intended to plone
add-ons developers.

If you need to create a browser view with configuration this add-on will make 
your life easier.

Features:

* Configuration providers
* Configuration structure defined with zope.interface & zope.schema
* Store configuration with plone.app.registry
* Auto form to manage the configuration of the current view

Why doing this in an add-on
===========================

Because most of the time developers faced to this issue store data in the
content type, or with annotation on context without trying to optimize, or without
form, ...

How it works
============

This add-ons define two components:

* ConfigurableView
* Registry (IConfigurationStorage)

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


IConfigurationStorage
---------------------

This component is responsible to return settings. It has been implemented
as an adapter from your configurable view.


IConfigurableView
-----------------

This component is implemented as a browserview. You have to inherits from 
this one to create your own browser view.

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

Authors

- JeanMichel FRANCOIS aka toutpt <toutpt@gmail.com>

Contributors

- Radim Novotny aka naro

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com
