import hexdi


@hexdi.permanent()
class SomeA:
    def foo(self):
        return 42


@hexdi.inject(SomeA)
def test(a):
    print(a.foo())


if __name__ == '__main__':
    test()  # prints: 42
