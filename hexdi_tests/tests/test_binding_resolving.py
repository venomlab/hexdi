from hexdi_tests.tests import basetest
import hexdi


class TestA(object):
    def test(self): pass


class TestAimpl(TestA):
    def test(self):
        return 42


class BindingResolvingTest(basetest.BaseHexDITest):
    def test_binding_resolving_class(self):
        self.container.bind_type(TestAimpl, TestA, hexdi.lifetime.PermanentLifeTimeManager)
        instance = self.container.resolve(TestA)
        self.assertEqual(instance.__class__.__name__, TestAimpl.__name__)
        self.assertFalse(hasattr(instance, 'attr1'))
        self.assertEqual(instance.test(), 42)

    def test_binding_resolving_instance(self):
        instance = TestAimpl()
        setattr(instance, 'attr1', 42)
        self.container.bind_instance(instance, TestA)
        instance = self.container.resolve(TestA)
        self.assertEqual(instance.__class__.__name__, TestAimpl.__name__)
        self.assertTrue(hasattr(instance, 'attr1'))
        self.assertEqual(getattr(instance, 'attr1'), 42)
        self.assertEqual(instance.test(), 42)
