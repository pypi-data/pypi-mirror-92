from tests import example
from entities.directory_settings import DirectorySettings


def test_module_settings():
    settings = DirectorySettings(example)

    fields = ["API_TOKEN", "DB_USER", "DB_PASSWORD"]

    for field in fields:
        assert hasattr(settings, field), f"Settings must have got field {field}"
