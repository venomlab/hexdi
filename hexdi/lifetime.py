#    Highly extensible Dependency injection framework for humans
#    Copyright (C) 2017 Dmitriy Selischev
#    The MIT License (MIT)
#    
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files
#    (the "Software"), to deal in the Software without restriction,
#    including without limitation the rights to use, copy, modify, merge,
#    publish, distribute, sublicense, and/or sell copies of the Software,
#    and to permit persons to whom the Software is furnished to do so,
#    subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

class BaseLifeTimeManager(object):
    def __init__(self, cls):
        self._cls = cls

    def resolve(self): pass

    def is_instantiated(self): pass


class PermanentLifeTimeManager(BaseLifeTimeManager):
    def __init__(self, cls):
        super().__init__(cls)
        self.instance = None

    def resolve(self):
        if self.instance is None:
            self.instance = self._cls.__call__()
        return self.instance


class PerResolveLifeTimeManager(BaseLifeTimeManager):
    def resolve(self):
        return self._cls.__call__()


class PreparedInstanceLifeTimeManager(BaseLifeTimeManager):
    def resolve(self):
        return self._cls
