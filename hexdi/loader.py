import importlib
import typing
from hexdi import utils


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

    def _do_loading(self):
        for mod in self.__modules:
            utils.load_module(utils.get_module_name(mod))
