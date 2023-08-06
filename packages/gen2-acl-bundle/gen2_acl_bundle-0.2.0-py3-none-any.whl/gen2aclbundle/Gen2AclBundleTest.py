import unittest
from injecta.testing.servicesTester import testServices
from pyfonycore.bootstrap import bootstrappedContainer

class Gen2AclBundleTest(unittest.TestCase):

    def test_init(self):
        container = bootstrappedContainer.init('test')

        testServices(container)

if __name__ == '__main__':
    unittest.main()
