import typing
import re
import hexdi
import hexdi.core
import hexdi.utils


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
    __component_re = re.compile(r'@?(?:hexdi\.)?{}'.format(hexdi.component.__name__), re.MULTILINE)
    __permanent_re = re.compile(r'@?(?:hexdi\.)?{}'.format(hexdi.permanent.__name__), re.MULTILINE)
    __transient_re = re.compile(r'@?(?:hexdi\.)?{}'.format(hexdi.transient.__name__), re.MULTILINE)
    __bind_type_re = re.compile(r'[^.]{}'.format(hexdi.core.DiContainer.bind_type.__name__), re.MULTILINE)
    __bind_inst_re = re.compile(r'[^.]{}'.format(hexdi.core.DiContainer.bind_instance.__name__), re.MULTILINE)

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
        self.__context = set()

    def __parse(self, mod):
        module_string = hexdi.utils.read_module_as_string(mod)
        for regex in self.__regex_list:
            if regex.match(module_string) is not None:
                self.__context.add(mod)
                break

    def __investigate(self, mod):
        if hexdi.utils.is_module(mod):
            self.__parse(mod)
        elif hexdi.utils.is_package(mod):
            submodules = hexdi.utils.get_submodules(mod)
            for m in submodules:
                self.__investigate(m)

    def _do_find(self) -> typing.List[typing.AnyStr]:
        for mod in self.__packages:
            self.__investigate(mod)
        return list(self.__context)
