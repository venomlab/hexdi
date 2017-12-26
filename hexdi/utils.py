import collections
import importlib
import os


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
    return mod.replace('.', '/')


def __sanitize_module(mod: str):
    path = __sanitize_path(mod)
    return "{}.py".format(path)


def get_submodules(mod):
    if is_package(mod):
        path = __sanitize_path(mod)
        lst = os.listdir(path)
        submodules = list()
        for l in lst:
            if l in ['__pycache__']:
                continue
            if __is_module_without_sanitizing(path, l) and l.endswith('.py'):
                submodules.append(l[:-3])
            else:
                submodules.append(l)
        return list(["{}.{}".format(mod, l) for l in submodules])
    else:
        return []


def is_module(mod):
    return os.path.isfile(__sanitize_module(mod))


def __is_module_without_sanitizing(path, mod):
    return os.path.isfile(os.path.join(path, mod))


def is_package(mod):
    return os.path.isdir(__sanitize_path(mod))


def read_module_as_string(mod):
    with open(__sanitize_module(mod), encoding='utf-8', mode='r') as f:
        return f.read()


def load_module(mod: str):
    return importlib.import_module(mod, package=__name__)


def load_class(path: str):
    splitted = path.split('.')
    mod = splitted[:-1]
    cls = splitted[-1:]
    module_path = ".".join(mod)
    _module = load_module(module_path)
    return _module.get(cls)


def loading_indicator(percentage, prefix='', suffix='', indicator='❚'):
    percentage_int = int(percentage)
    if 0 <= percentage_int <= 100:
        free_space_int = 100 - percentage_int
        filled = indicator * percentage_int
        free = '-' * free_space_int
        print('%s [%s%s] %s%% %s' % (prefix, filled, free, percentage_int, suffix), end='\r')
