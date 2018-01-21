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
    __component_re = re.compile(r'@?hexdi\.{}'.format(decorator.component.__name__), re.MULTILINE)
    __permanent_re = re.compile(r'@?hexdi\.{}'.format(decorator.permanent.__name__), re.MULTILINE)
    __transient_re = re.compile(r'@?hexdi\.{}'.format(decorator.transient.__name__), re.MULTILINE)
    __bind_type_re = re.compile(r'[^.]{}'.format(core.DiContainer.bind_type.__name__), re.MULTILINE)
    __bind_inst_re = re.compile(r'[^.]{}'.format(core.DiContainer.bind_instance.__name__), re.MULTILINE)
    __bind_type_stc_re = re.compile(r'hexdi\.bind_type', re.MULTILINE)
    __bind_permanent_stc_re = re.compile(r'hexdi\.bind_permanent', re.MULTILINE)
    __bind_transient_stc_re = re.compile(r'hexdi\.bind_transient', re.MULTILINE)

    __regex_list = [
        __component_re,
        __permanent_re,
        __transient_re,
        __bind_type_re,
        __bind_inst_re,
        __bind_type_stc_re,
        __bind_permanent_stc_re,
        __bind_transient_stc_re,
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
                if mod.endswith('.__init__'):
                    module_to_add, suffix = mod.rsplit('.', 1)
                else:
                    module_to_add = mod
                self.__context.add(module_to_add)
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
