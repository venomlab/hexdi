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

import typing
import hexdi
import hexdi.gentype
import hexdi.lifetime


def component(lifetime, accessor=None):
    def component_wrap(type_to_bind):
        container = hexdi.get_root_container()
        if accessor is None:
            container.bind_type(accessor=type_to_bind, type_to_resolve=type_to_bind, lifetime_manager=lifetime)
        else:
            container.bind_type(accessor=accessor, type_to_resolve=type_to_bind, lifetime_manager=lifetime)
        return type_to_bind

    return component_wrap


def permanent(accessor=None):
    return component(hexdi.lifetime.PermanentLifeTimeManager, accessor)


def transient(accessor=None):
    return component(hexdi.lifetime.PerResolveLifeTimeManager, accessor)


def dependency(cls: typing.Type[hexdi.gentype.T]):
    def dependency_func(func):
        def dependency_func_injection(*args, **kwargs) -> hexdi.gentype.T:
            container = hexdi.get_root_container()
            instance = container.resolve(cls)
            return instance

        return dependency_func_injection

    return dependency_func


def inject(*deps: typing.Optional[typing.Type[hexdi.gentype.T]]):
    def inject_func(func):
        def inject_func_args(*args):
            container = hexdi.get_root_container()
            resolves = list(args)
            for d in deps:
                resolves.append(container.resolve(d))
            return func(*resolves)

        return inject_func_args

    return inject_func
