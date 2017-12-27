import typing
import re
from hexdi import decorator
from hexdi import core
from hexdi import utils


class AbstractBaseFinder(object):
    def find(self) -> typing.List[typing.AnyStr]:
        pass


class AbstractOneTimeFinder(AbstractBaseFinder):
    def __init__(self):
        self.__found = False
        self.__modules = None

    def _do_find(self) -> typing.List[typing.AnyStr]:
        pass

    def find(self) -> typing.List[typing.AnyStr]:
        if not self.__found:
            self.__modules = self._do_find()
            self.__found = True
        return self.__modules


class RecursiveRegexFinder(AbstractOneTimeFinder):
    __component_re = re.compile(r'@?(?:hexdi\.)?{}'.format(decorator.component.__name__), re.MULTILINE)
    __permanent_re = re.compile(r'@?(?:hexdi\.)?{}'.format(decorator.permanent.__name__), re.MULTILINE)
    __transient_re = re.compile(r'@?(?:hexdi\.)?{}'.format(decorator.transient.__name__), re.MULTILINE)
    __bind_type_re = re.compile(r'[^.]{}'.format(core.DiContainer.bind_type.__name__), re.MULTILINE)
    __bind_inst_re = re.compile(r'[^.]{}'.format(core.DiContainer.bind_instance.__name__), re.MULTILINE)

    __regex_list = [
        __component_re,
        __permanent_re,
        __transient_re,
        __bind_type_re,
        __bind_inst_re
    ]

    def __init__(self, packages):
        super().__init__()
        self.__packages = packages
        self.__found_modules = set()
        self.__context = set()

    def __parse(self, mod):
        module_string = utils.read_module_as_string(mod)
        for regex in self.__regex_list:
            if regex.search(module_string) is not None:
                self.__context.add(mod)
                break

    def __investigate(self, mod):
        if utils.get_package_if_exists(mod):
            submodules = utils.get_submodules(mod)
            for m in submodules:
                self.__investigate(m)
        elif utils.get_module_if_exists(mod):
            self.__found_modules.add(mod)

    def _do_find(self) -> typing.List[typing.AnyStr]:
        for mod in self.__packages:
            self.__investigate(mod)
        for mod in self.__found_modules:
            self.__parse(mod)
        return list(self.__context)
