# hexdi
Highly extensible Dependency Injection framework for humans

# Installation
```bash
pip install hexdi
```
You **should** have python 3.5.* or higher

# Usage

All of that usages you can find in **examples** directory

## Quick usage reference

```python
import hexdi


class SomeA:
    def foo(self): pass


# mark that class as injectable with permanent lifetime for class SomeA
@hexdi.permanent(SomeA)
class SomeAimplementation(SomeA):
    def foo(self):
        return 42


#inject instance of SomeA as a first argument
@hexdi.inject(SomeA)
def test_injection(a: SomeA):
    print('test_injection:', a.foo())


class ClassWithDependency:
    #constructor injection
    @hexdi.inject(SomeA)
    def __init__(self, a: SomeA):
        print('ClassWithDependency.__init__:', a.foo())

    #after that we can use property like an instance of SomeA class
    @property
    @hexdi.dependency(SomeA)
    def some_a(self) -> SomeA: pass

    def foo(self):
        print('ClassWithDependency.foo:', self.some_a.foo())

    #method injection also works fine. Because injection members are passing after all transmitted positional arguments
    @hexdi.inject(SomeA)
    def foo_with_injection(self, a: SomeA):
        print('ClassWithDependency.foo_with_injection:', a.foo())


if __name__ == '__main__':
    test_injection()                # prints: test_injection: 42
    cwd = ClassWithDependency()     # prints: ClassWithDependency.__init__: 42
    cwd.foo()                       # prints: ClassWithDependency.foo: 42
    cwd.foo_with_injection()        # prints: ClassWithDependency.foo_with_injection: 42


```

## Self-binding

```python
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

```

## Multiple injection arguments

```python
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

```

## Permanent lifetime and transient lifetime

```python
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

```

## Usage of container. Demonstration of lazy injection

```python
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
```