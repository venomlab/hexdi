__root_type__ = None
__root_container__ = None


def register_root_type(cls) -> bool:
    global __root_type__
    global __root_container__
    if __root_container__ is None:
        __root_type__ = cls
        return True
    return False


def get_root_container():
    global __root_container__
    global __root_type__
    if __root_type__ is not None:
        if __root_container__ is None:
            __root_container__ = __root_type__.__call__()
        return __root_container__
    raise Exception('No one container is registered as future root')


class DiContainerMeta(type):
    def __call__(cls, *args, **kwargs):
        global __root_container__
        instance = super(DiContainerMeta, cls).__call__(*args, **kwargs)
        if __root_container__ is None and register_root_type(cls):
            __root_container__ = instance
        return instance

    def __new__(mcs, *args, **kwargs):
        cls = super(DiContainerMeta, mcs).__new__(mcs, *args, **kwargs)
        register_root_type(cls)
        return cls
