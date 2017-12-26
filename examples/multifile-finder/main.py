import hexdi
from examples.multifile.interfaces import SomeA

# That finder will find that
finder = hexdi.get_finder(['examples.multifile-finder'])
loader = hexdi.get_loader(finder.find())


@hexdi.inject(SomeA)
def test(a: SomeA):
    print(a.foo())


if __name__ == '__main__':
    loader.load()
    test()  # prints: 69
