import hexdi
from examples.multifile.interfaces import SomeA

loader = hexdi.basic_loader([
    'examples.multifile.implementations'
])


@hexdi.inject(SomeA)
def test(a: SomeA):
    print(a.foo())


if __name__ == '__main__':
    loader.load()
    test()  # prints: 42
