from entities import Settings

class TestDefaultSettingsWithName1:
    name = "NAME"


class TestDefaultSettingsWithName2:
    name = "OTHER NAME"


class TestSettings1:
    field1 = 1
    field2 = 2


class TestSettings2:
    field3 = 3
    field4 = 4


def test_init():
    settings = Settings(TestSettings1)

    assert settings.field1 == 1
    assert settings.field2 == 2


def test_add():
    settings = Settings(TestSettings1) + Settings(TestSettings2)

    fields = ["field1", "field2", "field3", "field4"]

    for field in fields:
        assert hasattr(settings, field), f"Settings must hase got field {field}"


def test_iter():
    settings = Settings(TestSettings1)

    for key, value in settings:
        assert key in ["field1", "field2"]


def test_extend():
    settings = Settings(TestSettings1)
    assert not (hasattr(settings, "field3"))

    settings.extend(TestSettings2)
    assert hasattr(settings, "field3")


def test_extend_collisions():
    settings1 = Settings(TestDefaultSettingsWithName1)
    settings2 = Settings(TestDefaultSettingsWithName2)

    assert (settings1 + settings2).name == "OTHER NAME"
    assert (settings2 + settings1).name == "NAME"
