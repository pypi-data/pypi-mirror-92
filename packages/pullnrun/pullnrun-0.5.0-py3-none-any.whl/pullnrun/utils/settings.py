DEFAULT_SETTINGS_DICT = dict(
    log_to_console=True,
    stop_on_errors=True,
)


class Settings:
    def __init__(self, defaults):
        self._data = {**defaults}

    def update(self, input_dict=None, no_none_check=False):
        if not input_dict:
            return self

        for key in self._data.keys():
            value = input_dict.get(key)
            if value is not None or no_none_check:
                self._data[key] = value

        return self

    def new(self, input_dict=None):
        return Settings(self._data).update(input_dict)

    def keys(self):
        return self._data.keys()

    def __call__(self, input_dict=None):
        return self.new(input_dict)

    def __getattr__(self, name):
        return self._data.get(name)


DEFAULT_SETTINGS = Settings(DEFAULT_SETTINGS_DICT)
