import hexdi


@hexdi.permanent()
class SomeA:
    NUMBER = 0

    def __init__(self):
        self.num = SomeA.NUMBER
        SomeA.NUMBER += 1

    def foo(self):
        print(self.__class__.__name__, self.num)


@hexdi.transient()
class SomeB:
    NUMBER = 0

    def __init__(self):
        self.num = SomeB.NUMBER
        SomeB.NUMBER += 1

    def foo(self):
        print(self.__class__.__name__, self.num)


@hexdi.inject(SomeA)
def test_a(a):
    a.foo()


@hexdi.inject(SomeB)
def test_b(b):
    b.foo()


if __name__ == '__main__':
    test_a()  # prints: SomeA 0
    test_a()  # prints: SomeA 0
    test_a()  # prints: SomeA 0
    test_b()  # prints: SomeB 0
    test_b()  # prints: SomeB 1
    test_b()  # prints: SomeB 2
