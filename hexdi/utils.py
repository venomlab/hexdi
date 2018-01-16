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
import importlib
import os
import site


def __get_root_package_directories():
    current_working_dir = os.getcwd()
    root_packages = site.getsitepackages()
    return root_packages + [current_working_dir]


__DIRECTORIES_TO_SEARCH_PACKAGES = __get_root_package_directories()


def get_module_name(obj):
    if isinstance(obj, str):
        return obj

    if callable(obj):
        return get_module_name(obj.__call__())

    if isinstance(obj, collections.Iterable):
        lst = list(obj)
        if len(lst) > 0:
            o = lst.pop(0)
            if callable(o):
                if len(lst) > 0:
                    arguments = lst[1]
                    return get_module_name(o.__call__(*arguments))


def __sanitize_path(mod: str):
    path = mod.replace('.', '/')
    return list([os.path.join(d, path) for d in __DIRECTORIES_TO_SEARCH_PACKAGES])


def __sanitize_module(mod: str):
    paths = __sanitize_path(mod)
    return list(["{}.py".format(path) for path in paths])


def get_submodules(mod):
    package = get_package_if_exists(mod)
    if package is not None:
        lst = os.listdir(package)
        submodules = set()
        for l in lst:
            if l in ['__pycache__']:
                continue
            if __is_module_without_sanitizing(package, l) and l.endswith('.py'):
                submodules.add(l[:-3])
            else:
                submodules.add(l)
        return list(["{}.{}".format(mod, l) for l in submodules])
    else:
        return []


def get_module_if_exists(mod):
    mods = __sanitize_module(mod)
    for m in mods:
        if os.path.isfile(m):
            return m
    return None


def get_package_if_exists(mod):
    paths = __sanitize_path(mod)
    for p in paths:
        if os.path.isdir(p):
            return p
    return None


def __is_module_without_sanitizing(path, mod):
    return os.path.isfile(os.path.join(path, mod))


def read_module_as_string(mod):
    mod_path = get_module_if_exists(mod)
    with open(mod_path, encoding='utf-8', mode='r') as f:
        return f.read()


def load_module(mod: str):
    return importlib.import_module(mod, package=__name__)


def load_class(path: str):
    mod, cls = path.rsplit('.', 1)
    _module = load_module(mod)
    return getattr(_module, cls)


def loading_indicator(percentage, prefix='', suffix='', indicator='❚'):
    percentage_int = int(percentage)
    if 0 <= percentage_int <= 100:
        free_space_int = 100 - percentage_int
        filled = indicator * percentage_int
        free = '-' * free_space_int
        print('%s [%s%s] %s%% %s' % (prefix, filled, free, percentage_int, suffix), end='\r')
