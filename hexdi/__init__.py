from __future__ import absolute_import

import collections

from hexdi import lifetime, gentype as __gentype__
from hexdi import loader
from hexdi import finder
from hexdi.core import get_root_container, clstype as __clstype__
# Quick access imports
from hexdi.decorator import component, permanent, transient, dependency, inject


# Shortcut functions

def resolve(accessor: __clstype__) -> __gentype__.T:
    """
    shortcut for resolving from root container

    :param accessor: accessor for resolving object
    :return: resolved object of requested type
    """
    return get_root_container().resolve(accessor=accessor)


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
