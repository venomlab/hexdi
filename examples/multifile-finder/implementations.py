import hexdi

from examples.multifile.interfaces import SomeA


@hexdi.permanent(SomeA)
class SomeAimplementation(SomeA):
    def foo(self):
        return 69
