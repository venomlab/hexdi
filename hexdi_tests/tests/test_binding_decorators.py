from hexdi_tests.tests import basetest
import hexdi


class TestAMeta(type):
    NUMBER = 0

    def __call__(cls, *args, **kwargs):
        instance = super(TestAMeta, cls).__call__(*args, **kwargs)
        instance.a = TestAMeta.NUMBER
        TestAMeta.NUMBER += 1
        return instance


class TestA(metaclass=TestAMeta):
    def __init__(self):
        self.a = None

    def test(self):
        return self.a


class BindingDecoratorTest(basetest.BaseHexDITest):
    def setUp(self):
        super(BindingDecoratorTest, self).setUp()
        TestAMeta.NUMBER = 0

    def test_decorator_permanent_binding(self):
        @hexdi.permanent(TestA)
        class TestAPermanent(TestA):
            pass

        instance = self.container.resolve(TestA)
        self.assertEqual(instance.__class__.__name__, TestAPermanent.__name__)
        self.assertEqual(0, instance.test())
        instance = self.container.resolve(TestA)
        self.assertEqual(instance.__class__.__name__, TestAPermanent.__name__)
        self.assertEqual(0, instance.test())

    def test_decorator_permanent_alias_binding(self):
        @hexdi.permanent('test_a_alias_permanent')
        class TestAPermanentAlias(TestA):
            pass

        instance = self.container.resolve('test_a_alias_permanent')
        self.assertEqual(instance.__class__.__name__, TestAPermanentAlias.__name__)
        self.assertEqual(0, instance.test())
        instance = self.container.resolve('test_a_alias_permanent')
        self.assertEqual(instance.__class__.__name__, TestAPermanentAlias.__name__)
        self.assertEqual(0, instance.test())

    def test_decorator_transient_binding(self):
        @hexdi.transient(TestA)
        class TestATransient(TestA):
            pass

        instance = self.container.resolve(TestA)
        self.assertEqual(instance.__class__.__name__, TestATransient.__name__)
        self.assertEqual(0, instance.test())
        instance = self.container.resolve(TestA)
        self.assertEqual(instance.__class__.__name__, TestATransient.__name__)
        self.assertEqual(1, instance.test())

    def test_decorator_transient_alias_binding(self):
        @hexdi.transient('test_a_alias_transient')
        class TestATransient(TestA):
            pass

        instance = self.container.resolve('test_a_alias_transient')
        self.assertEqual(instance.__class__.__name__, TestATransient.__name__)
        self.assertEqual(0, instance.test())
        instance = self.container.resolve('test_a_alias_transient')
        self.assertEqual(instance.__class__.__name__, TestATransient.__name__)
        self.assertEqual(1, instance.test())
