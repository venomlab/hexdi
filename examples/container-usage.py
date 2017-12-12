import hexdi


class SomeA:
    def foo(self): pass


class SomeAImplementation(SomeA):
    def foo(self):
        return 42


@hexdi.permanent()
class SomeB:
    def foo(self):
        return 69


class SomeC:
    def foo(self):
        return 100500


@hexdi.inject(SomeC)
def test(c):
    print(c.foo())


if __name__ == '__main__':
    # getting of container
    container = hexdi.get_root_container()
    # binding SomeAImplementation on SomeA type with permanent lifetime
    container.bind_type(SomeAImplementation, SomeA, hexdi.lifetime.PermanentLifeTimeManager)
    instance = container.resolve(SomeA)
    print(instance.foo())  # prints: 42
    # resolve decorator-binded SomeB
    instance = container.resolve(SomeB)
    print(instance.foo())  # prints: 69
    # bind SomeC on itself with permanent lifetime
    container.bind_type(SomeC, SomeC, hexdi.lifetime.PermanentLifeTimeManager)
    # we mark SomeC for injection above in test func,
    # but all works fine, because it is lazy injection
    test()  # prints: 100500
