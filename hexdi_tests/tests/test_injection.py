from hexdi_tests.tests import basetest
import hexdi


class A:
    def get_value(self): pass


class B:
    def get_value(self): pass


class Aimpl(A):
    def get_value(self):
        return 42


class Bimpl(B):
    def get_value(self):
        return 69


class InjectionTest(basetest.BaseHexDITest):
    def setUp(self):
        super(InjectionTest, self).setUp()
        self.container.bind_type(Aimpl, A, hexdi.lifetime.PermanentLifeTimeManager)
        self.container.bind_type(Bimpl, B, hexdi.lifetime.PermanentLifeTimeManager)

    def test_property_injection(self):
        class TestPropertyInjection:
            @property
            @hexdi.dependency(A)
            def a(self) -> A: pass

            @property
            @hexdi.dependency(B)
            def b(self) -> B: pass

            def test(self):
                return self.a.get_value() + self.b.get_value()

        instance = TestPropertyInjection()
        self.assertEqual(instance.test(), 111)

    def test_parameters_injection(self):
        class TestParametersInjection:
            @hexdi.inject(A, B)
            def test(self, a: A, b: B):
                return a.get_value() + b.get_value()

        instance = TestParametersInjection()
        self.assertEqual(instance.test(), 111)

    def test_init_injection_and_resolving(self):
        @hexdi.permanent()
        class TestInitInjection:
            @hexdi.inject(A, B)
            def __init__(self, a: A, b: B):
                self.a = a
                self.b = b

            def test(self):
                return self.a.get_value() + self.b.get_value()

        instance = self.container.resolve(TestInitInjection)
        self.assertEqual(instance.test(), 111)
