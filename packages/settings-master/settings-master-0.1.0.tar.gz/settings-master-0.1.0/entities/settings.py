from entities.abstract_settings import AbstractSettings


class Settings(AbstractSettings):
    def extend(self, obj):
        if obj is not None:
            self._extend_settings(obj)

    def _extend_settings(self, obj):
        data = self._get_object_data(obj)

        self.__dict__.update(data)

    def _get_object_data(self, obj) -> dict:
        all_object_data = self._get_object_all_data(obj)

        return {
            key: value

            for key, value in all_object_data.items() if not key.startswith("_")
        }

    @staticmethod
    def _get_object_all_data(obj):
        return obj.__dict__

    @property
    def data(self) -> dict:
        return self._get_object_data(self)
