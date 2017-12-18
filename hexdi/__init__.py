from __future__ import absolute_import

import collections

# Quick access imports
from hexdi.decorator import component, permanent, transient, dependency, inject
from hexdi.core import get_root_container, clstype as __clstype__
from hexdi import lifetime, gentype as __gentype__
from hexdi import loader


# Shortcut functions

def resolve(accessor: __clstype__) -> __gentype__.T:
    """
    shortcut for resolving from root container

    :param accessor: accessor for resolving object
    :return: resolved object of requested type
    """
    return get_root_container().resolve(accessor=accessor)


def basic_loader(modules: collections.Iterable) -> loader.AbstractBaseLoader:
    """
    shortcut for constructing of basic loader

    :param modules: list of modules to load
    :return: constructed basic class loader
    """
    return loader.BasicLoader(modules)
