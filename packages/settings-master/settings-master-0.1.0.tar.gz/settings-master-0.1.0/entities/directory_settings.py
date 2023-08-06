from entities import Settings


class DirectorySettings(Settings):
    _directory = None

    def extend(self, directory):
        self._directory = directory

        if directory is not None:
            self._extend_module_settings()

    def _extend_module_settings(self):
        for module in self._get_directory_modules():
            self._extend_settings(module)

    def _get_directory_modules(self) -> list:
        fields_names = self._get_directory_modules_names()

        return list(map(
            lambda field_name: getattr(self._directory, field_name),
            fields_names
        ))

    def _get_directory_modules_names(self) -> list:
        return list(
            self._get_object_data(self._directory).keys()
        )

