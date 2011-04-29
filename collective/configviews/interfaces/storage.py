from zope import interface
from zope import schema

class IConfigurationStorage(interface.Interface):
    """Configuration storage manager"""

    def set(configuration):
        """Create or update configuration stored in instance."""

    def get():
        """-> dict with configuration like if it was extracted from the form
        """
