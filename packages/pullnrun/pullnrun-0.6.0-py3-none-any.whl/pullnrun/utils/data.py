class Data:
    def __init__(self, defaults):
        super().__setattr__('_data', {**defaults})

    def __getattr__(self, name):
        return self._data.get(name)

    def __setattr__(self, name, value):
        self._data[name] = value

    @property
    def json(self):
        return self._data

    def keys(self):
        return self._data.keys()


class Meta(Data):
    def __init__(self, data):
        super().__init__(
            {key: data.get(key) for key in ['name', 'description']})


DEFAULT_SETTINGS_DICT = dict(
    debug=False,
    log_to_console=True,
    stop_on_errors=True,
    resolve_templates=True,
    register='pullnrun_last_return_value',
    when=True,
)


class Settings(Data):
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


DEFAULT_SETTINGS = Settings(DEFAULT_SETTINGS_DICT)


INITIAL_STATS = dict(
    success=0,
    ignored=0,
    fail=0,
    error=0,
    skipped=0,
)


class Statistics(Data):
    def __init__(self, data=None):
        super().__init__(data or INITIAL_STATS)

    def add(self, key):
        self._data[key] = self._data[key] + 1

    def as_str(self, width=10):
        return '\n'.join(
            f'{key.title() + ":":{width}} {value}' for key,
            value in self._data.items())
