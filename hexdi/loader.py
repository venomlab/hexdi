import importlib
import typing
import collections


class AbstractBaseLoader(object):
    def load(self):
        pass


class AbstractOneTimeLoader(AbstractBaseLoader):
    def __init__(self):
        self.__loaded = False

    def load(self):
        """
        load classes to providing auto register
        """
        if not self.__loaded:
            self._do_loading()
            self.__loaded = True

    def _do_loading(self):
        pass


class BasicLoader(AbstractOneTimeLoader):
    def __init__(self, modules: typing.Iterable):
        super().__init__()
        self.__modules = modules

    def __get_module_name(self, obj):
        if isinstance(obj, str):
            return obj

        if callable(obj):
            return self.__get_module_name(obj.__call__())

        if isinstance(obj, collections.Iterable):
            lst = list(obj)
            if len(lst) > 0:
                o = lst.pop(0)
                if callable(o):
                    if len(lst) > 0:
                        arguments = lst[1]
                        return self.__get_module_name(o.__call__(*arguments))

        return None

    def _do_loading(self):
        for mod in self.__modules:
            importlib.import_module(self.__get_module_name(mod))
