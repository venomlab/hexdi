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

from __future__ import absolute_import

import collections

from hexdi import lifetime, gentype as __gentype__
from hexdi import loader
from hexdi import finder
import hexdi.core
# Quick access imports
from hexdi.decorator import component, permanent, transient, dependency, inject
from hexdi.core import get_root_container


# Shortcut functions

def resolve(accessor: hexdi.core.clstype) -> __gentype__.T:
    """
    shortcut for resolving from root container

    :param accessor: accessor for resolving object
    :return: resolved object of requested type
    """
    return hexdi.core.get_root_container().resolve(accessor=accessor)


def get_loader(modules: collections.Iterable) -> loader.AbstractBaseLoader:
    """
    shortcut for constructing of basic loader

    :param modules: list of modules to load
    :return: constructed basic class loader
    """
    return loader.BasicLoader(modules)


def get_finder(packages: collections.Iterable) -> finder.AbstractBaseFinder:
    """
    shortcut for constructing of recursive regex finder

    :param packages:
    """
    return finder.RecursiveRegexFinder(packages)


def bind_type(type_to_bind: hexdi.core.restype, accessor: hexdi.core.clstype, lifetime_manager: hexdi.core.ltype):
    """
    shortcut for bind_type on root container

    :param type_to_bind: type that will be resolved by accessor
    :param accessor: accessor for resolving object
    :param lifetime_manager: type of lifetime manager for this binding
    """
    hexdi.core.get_root_container().bind_type(type_to_bind, accessor, lifetime_manager)


def bind_permanent(type_to_bind: hexdi.core.restype, accessor: hexdi.core.clstype):
    """
    shortcut for bind_type with PermanentLifeTimeManager on root container

    :param type_to_bind: type that will be resolved by accessor
    :param accessor: accessor for resolving object
    """
    hexdi.core.get_root_container().bind_type(type_to_bind, accessor, lifetime.PermanentLifeTimeManager)


def bind_transient(type_to_bind: hexdi.core.restype, accessor: hexdi.core.clstype):
    """
    shortcut for bind_type with PerResolveLifeTimeManager on root container

    :param type_to_bind: type that will be resolved by accessor
    :param accessor: accessor for resolving object
    """
    hexdi.core.get_root_container().bind_type(type_to_bind, accessor, lifetime.PerResolveLifeTimeManager)
