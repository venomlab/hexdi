import hexdi


@hexdi.permanent()
class SomeA:
    def foo(self):
        return 42


@hexdi.permanent()
class SomeB:
    def foo(self):
        return 69


@hexdi.inject(SomeA, SomeB)
def test(a, b):
    print(a.foo() + b.foo())


if __name__ == '__main__':
    test()  # prints: 111
