import hexdi
from tests.cases.test_multifile import SomeTestA


@hexdi.permanent(SomeTestA)
class SomeTestAImpl(SomeTestA):
    def foo(self):
        return 42
