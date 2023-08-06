import os
from mjango import exceptions


class SettingsDesc:
    def __init__(self, default=None):
        self._value = default

    def __get__(self, instance, cls):
        return self._value

    def __set__(self, instance, value):
        self._value = value


class Settings:
    db_host = SettingsDesc()
    db_name = SettingsDesc()


db_settings = Settings()
