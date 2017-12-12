import hexdi


class SomeA:
    def foo(self): pass


# mark that class as injectable with permanent lifetime for class SomeA
@hexdi.permanent(SomeA)
class SomeAimplementation(SomeA):
    def foo(self):
        return 42


@hexdi.inject(SomeA)
def test_injection(a: SomeA):
    print('test_injection:', a.foo())


class ClassWithDependency:
    @hexdi.inject(SomeA)
    def __init__(self, a: SomeA):
        print('ClassWithDependency.__init__:', a.foo())

    @property
    @hexdi.dependency(SomeA)
    def some_a(self) -> SomeA: pass

    def foo(self):
        print('ClassWithDependency.foo:', self.some_a.foo())

    @hexdi.inject(SomeA)
    def foo_with_injection(self, a: SomeA):
        print('ClassWithDependency.foo_with_injection:', a.foo())


if __name__ == '__main__':
    test_injection()                # prints: test_injection: 42
    cwd = ClassWithDependency()     # prints: ClassWithDependency.__init__: 42
    cwd.foo()                       # prints: ClassWithDependency.foo: 42
    cwd.foo_with_injection()        # prints: ClassWithDependency.foo_with_injection: 42
