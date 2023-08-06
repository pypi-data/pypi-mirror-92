INITIAL_STATS = dict(
    success=0,
    ignored=0,
    fail=0,
    error=0,
)


class Statistics:
    def __init__(self, initial=None):
        self._data = {**(initial or INITIAL_STATS)}

    def add(self, key):
        self._data[key] = self._data[key] + 1

    def as_str(self, width=10):
        return '\n'.join(
            f'{key.title() + ":":{width}} {value}' for key,
            value in self._data.items())

    def __getattr__(self, name):
        return self._data.get(name)
