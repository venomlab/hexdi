class BaseLifeTimeManager(object):
    def __init__(self, cls):
        self._cls = cls

    def resolve(self): pass

    def is_instantiated(self): pass


class PermanentLifeTimeManager(BaseLifeTimeManager):
    def __init__(self, cls):
        super().__init__(cls)
        self.instance = None

    def resolve(self):
        if self.instance is None:
            self.instance = self._cls.__call__()
        return self.instance


class PerResolveLifeTimeManager(BaseLifeTimeManager):
    def resolve(self):
        return self._cls.__call__()


class PreparedInstanceLifeTimeManager(BaseLifeTimeManager):
    def resolve(self):
        return self._cls
