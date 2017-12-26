import hexdi
from tests.cases.test_multifile import SomeTestB


@hexdi.permanent(SomeTestB)
class SomeTestBImpl(SomeTestB):
    def foo(self):
        return 69
