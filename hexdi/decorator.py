import typing
import hexdi
import hexdi.gentype
import hexdi.lifetime


def component(lifetime, base_type=None):
    def component_wrap(type_to_reg):
        container = hexdi.get_root_container()
        if base_type is None:
            container.bind_type(cls=type_to_reg, resolver=type_to_reg, lifetime_manager=lifetime(type_to_reg))
        else:
            container.bind_type(cls=base_type, resolver=type_to_reg, lifetime_manager=lifetime(type_to_reg))
        return type_to_reg

    return component_wrap


def permanent(base_type=None):
    return component(hexdi.lifetime.PermanentLifeTimeManager, base_type)


def transient(base_type=None):
    return component(hexdi.lifetime.PerResolveLifeTimeManager, base_type)


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
