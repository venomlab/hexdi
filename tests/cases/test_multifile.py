import hexdi

from tests.cases import basetest


class SomeTestA(object):
    def foo(self):
        pass


class SomeTestB(object):
    def foo(self):
        pass


class MultifileTest(basetest.BaseHexDITest):
    def test_finder_loader_found(self):
        finder = hexdi.get_finder(['tests.cases.multifile'])
        modules = finder.find()
        self.assertIn('tests.cases.multifile.multifile-for-finder-a', modules)
        self.assertIn('tests.cases.multifile.multifile-for-finder-b', modules)
        self.assertEqual(len(modules), 2)
        loader = hexdi.get_loader(modules)
        loader.load()
        self.assertTrue(self.container.binded(SomeTestA))
        self.assertTrue(self.container.binded(SomeTestB))
        testa = self.container.resolve(SomeTestA)
        testb = self.container.resolve(SomeTestB)
        self.assertEqual(42, testa.foo())
        self.assertEqual(69, testb.foo())
