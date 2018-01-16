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

import collections
import typing
from hexdi import gentype
from hexdi import meta
from hexdi import lifetime
from hexdi import utils

clstype = typing.Union[str, typing.Type[gentype.T]]
restype = typing.Union[str, gentype.T]
ltype_instance = lifetime.BaseLifeTimeManager
ltype = typing.Type[ltype_instance]


class DiContainer(metaclass=meta.DiContainerMeta):
    def __init__(self):
        self.container = dict()

    @staticmethod
    def _sanitize_accessor(o):
        if isinstance(o, str):
            return o
        else:
            return o.__name__

    def binded(self, accessor) -> bool:
        return self.container.get(self._sanitize_accessor(accessor)) is not None

    def bind_type(self, type_to_resolve: restype, accessor, lifetime_manager: ltype) -> None:
        if isinstance(type_to_resolve, str):
            type_to_resolve = utils.load_class(type_to_resolve)
        if isinstance(accessor, str) or issubclass(type_to_resolve, accessor):
            self._bind_type(accessor, lifetime_manager(type_to_resolve))
        elif isinstance(accessor, collections.Iterable):
            for element in accessor:
                self.bind_type(type_to_resolve, element, lifetime_manager)

    def _bind_type(self, accessor, lifetime_manager: ltype_instance):
        if not self.binded(accessor):
            self.container[self._sanitize_accessor(accessor)] = lifetime_manager
        else:
            raise Exception('already registered instance by \'%s\'' % self._sanitize_accessor(accessor))

    def bind_instance(self, instance: gentype.T, accessor):
        self._bind_type(accessor, lifetime.PreparedInstanceLifeTimeManager(instance))

    def unbind(self, accessor) -> None:
        if self.binded(accessor):
            del self.container[self._sanitize_accessor(accessor)]
        else:
            raise Exception('class %s is not registered' % self._sanitize_accessor(accessor))

    def resolve(self, accessor: clstype) -> gentype.T:
        if self.binded(accessor):
            return self.container.get(self._sanitize_accessor(accessor)).resolve()
        else:
            raise Exception('class %s is not registered' % self._sanitize_accessor(accessor))

    def destroy(self):
        self.container.clear()


def get_root_container() -> DiContainer:
    return meta.get_root_container()
