# -*- coding: utf-8 -*-

from zope.interface import implementer
from zope.component.interfaces import ObjectEvent
from .interfaces import IConfigurationChangedEvent


@implementer(IConfigurationChangedEvent)
class ConfigurationChangedEvent(ObjectEvent):
    """Event fired when the view configuration is changed"""

    def __init__(self, context, configuration, old_configuration):
        super(ConfigurationChangedEvent, self).__init__(context)
        self.configuration = configuration
        self.old_configuration = old_configuration
