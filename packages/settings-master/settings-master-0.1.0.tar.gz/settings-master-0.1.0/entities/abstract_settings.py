class AbstractSettings:
    def __init__(self, obj=None):
        self.extend(obj)

    def extend(self, obj):
        pass

    @property
    def data(self) -> dict:
        pass

    def __add__(self, other):
        cls = self.__class__
        settings = cls()

        settings.extend(self)
        settings.extend(other)

        return settings

    def __iter__(self):
        return iter(self.data.items())
