import unittest
from injecta.mocks.Bar import Bar
from injecta.mocks.Foo import Foo
from pyfonycore.bootstrap import bootstrappedContainer

class containerInitTest(unittest.TestCase):

    def test_basic(self):
        container = bootstrappedContainer.init('test')

        foo = container.get(Foo)
        bar = container.get('injecta.mocks.Bar')

        self.assertIsInstance(foo, Foo)
        self.assertIsInstance(bar, Bar)

if __name__ == '__main__':
    unittest.main()
