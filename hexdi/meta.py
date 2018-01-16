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

__root_type__ = None
__root_container__ = None


def register_root_type(cls) -> bool:
    global __root_type__
    global __root_container__
    if __root_container__ is None:
        __root_type__ = cls
        return True
    return False


def get_root_container():
    global __root_container__
    global __root_type__
    if __root_type__ is not None:
        if __root_container__ is None:
            __root_container__ = __root_type__.__call__()
        return __root_container__
    raise Exception('No one container is registered as future root')


class DiContainerMeta(type):
    def __call__(cls, *args, **kwargs):
        global __root_container__
        instance = super(DiContainerMeta, cls).__call__(*args, **kwargs)
        if __root_container__ is None and register_root_type(cls):
            __root_container__ = instance
        return instance

    def __new__(mcs, *args, **kwargs):
        cls = super(DiContainerMeta, mcs).__new__(mcs, *args, **kwargs)
        register_root_type(cls)
        return cls
