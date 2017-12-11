import typing
import hexdi
import hexdi.gentype
import hexdi.lifetime


def component(lifetime, accessor=None):
    def component_wrap(type_to_bind):
        container = hexdi.get_root_container()
        if accessor is None:
            container.bind_type(accessor=type_to_bind, type_to_resolve=type_to_bind, lifetime_manager=lifetime)
        else:
            container.bind_type(accessor=accessor, type_to_resolve=type_to_bind, lifetime_manager=lifetime)
        return type_to_bind

    return component_wrap


def permanent(accessor=None):
    return component(hexdi.lifetime.PermanentLifeTimeManager, accessor)


def transient(accessor=None):
    return component(hexdi.lifetime.PerResolveLifeTimeManager, accessor)


def dependency(cls: typing.Type[hexdi.gentype.T]):
    def dependency_func(func):
        def dependency_func_injection(*args, **kwargs) -> hexdi.gentype.T:
            container = hexdi.get_root_container()
            instance = container.resolve(cls)
            return instance

        return dependency_func_injection

    return dependency_func


def inject(*deps: typing.Optional[typing.Type[hexdi.gentype.T]]):
    def inject_func(func):
        def inject_func_args(*args):
            container = hexdi.get_root_container()
            resolves = list(args)
            for d in deps:
                resolves.append(container.resolve(d))
            return func(*resolves)

        return inject_func_args

    return inject_func
