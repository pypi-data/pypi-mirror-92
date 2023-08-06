from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
import re
from sys import stderr, stdout

from pullnrun.validate import validate_console


def command_as_str(command):
    return ' '.join(i if not re.search(r'\s', i)
                    else f"'{i}'" for i in command)


def _current_timestamp():
    return f'{datetime.utcnow().isoformat()}Z'


def _get_stream(stream_name):
    if stream_name not in ['stderr', 'stdin', 'stdout']:
        raise ValueError(
            'Value of stream_name must be stderr, stdin, or stdout.')

    return stderr if stream_name == 'stderr' else stdout


def _read_stream(stream_name, stream_fd, encoding, log_to_console):
    f = os.fdopen(stream_fd, encoding=encoding, errors='backslashreplace')
    data = []

    for line in iter(f.readline, ''):
        text = line.rstrip('\n')
        data.append(dict(
            stream=stream_name,
            timestamp=_current_timestamp(),
            text=text)),
        if log_to_console:
            stream = _get_stream(stream_name)
            print(text, file=stream)

    f.close()
    return data


class JsonStreams:
    def __init__(self, log_to_console=False):
        self._writes = []
        self._futures = []
        self._pool = ThreadPoolExecutor(max_workers=3)
        self._data = []
        self._log_to_console = log_to_console

    def __enter__(self):
        stdout = self.create('stdout')
        stderr = self.create('stderr')

        return (stdout, stderr, self,)

    def __exit__(self, type_, value, traceback):
        self.close()

    def log(self, text):
        return self.push('stdout', text=text)

    def input(self, text):
        return self.push('stdin', text=text)

    def error(self, text):
        return self.push('stderr', text=text)

    def push(self, stream_name=None, timestamp=None, text=None):
        if not (stream_name and text):
            raise ValueError(
                'Cannot push data without both stream_name and text.')

        stream = _get_stream(stream_name)

        if not timestamp:
            timestamp = _current_timestamp()

        self._data.append(dict(
            stream=stream_name,
            timestamp=timestamp,
            text=text,
        ))

        if self._log_to_console:
            if stream_name == 'stdin' and not text.startswith('# '):
                text = f'+ {text}'

            print(text, file=stream)

    def extend(self, data):
        validate_console(data)
        self._data.extend(data)

    def create(self, stream_name, encoding='utf-8'):
        read_fd, write_fd = os.pipe()
        self._writes.append(write_fd)
        self._futures.append(
            self._pool.submit(
                _read_stream,
                stream_name,
                read_fd,
                encoding,
                self._log_to_console
            ))
        return write_fd

    def close(self):
        for f in self._writes:
            os.close(f)

    def read(self, wait=False):
        data = []
        data.extend(self._data)

        for future in self._futures:
            if not wait and not future.done():
                return None

            data.extend(future.result())

        data.sort(key=lambda i: i.get('timestamp'))
        return data

    @property
    def data(self):
        return self.read()
