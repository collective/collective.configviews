import unittest2 as unittest
from plone.app import testing
from collective.configviews.tests import layer

class UnitTestCase(unittest.TestCase):
    pass

class IntegrationTestCase(unittest.TestCase):

    layer = layer.INTEGRATION


class FunctionalTestCase(unittest.TestCase):

    layer = layer.FUNCTIONAL
