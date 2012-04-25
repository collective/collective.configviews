import unittest2 as unittest

from collective.configviews import testing as layer

class UnitTestCase(unittest.TestCase):
    pass

class IntegrationTestCase(unittest.TestCase):

    layer = layer.INTEGRATION


class FunctionalTestCase(unittest.TestCase):

    layer = layer.FUNCTIONAL
