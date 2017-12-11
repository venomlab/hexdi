import collections
import typing
from hexdi import gentype
from hexdi import meta
from hexdi import lifetime

clstype = typing.Union[str, typing.Type[gentype.T]]


class DiContainer(metaclass=meta.DiContainerMeta):
    def __init__(self):
        self.container = dict()

    @staticmethod
    def _get_name(o):
        if isinstance(o, str):
            return o
        else:
            return o.__name__

    def binded(self, cls: clstype) -> bool:
        return self.container.get(self._get_name(cls)) is not None

    def bind_type(self, resolver: typing.Type[gentype.T],
                  cls: typing.Union[typing.Iterable[clstype], clstype, ...],
                  lifetime_manager: lifetime.BaseLifeTimeManager) -> None:
        if isinstance(cls, str) or issubclass(resolver, cls):
            self._bind_type(cls, lifetime_manager)
        elif isinstance(cls, collections.Iterable):
            for element in cls:
                self.bind_type(resolver, element, lifetime_manager)

    def _bind_type(self, cls: clstype, lifetime_manager):
        if not self.binded(cls):
            self.container[self._get_name(cls)] = lifetime_manager
        else:
            raise Exception('already registered instance by \'%s\'' % self._get_name(cls))

    def bind_instance(self, instance: gentype.T, cls: clstype):
        self._bind_type(cls, lifetime.PermanentLifeTimeManager(instance))

    def unbind(self, cls: clstype) -> None:
        if self.binded(cls):
            del self.container[self._get_name(cls)]
        else:
            raise Exception('class %s is not registered' % self._get_name(cls))

    def resolve(self, cls: clstype) -> gentype.T:
        if self.binded(cls):
            return self.container.get(self._get_name(cls)).resolve()
        else:
            raise Exception('class %s is not registered' % self._get_name(cls))


def get_root_container() -> DiContainer:
    return meta.get_root_container()
