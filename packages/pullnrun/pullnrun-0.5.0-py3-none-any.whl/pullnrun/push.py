from requests import request

from .utils.console import JsonStreams
from .utils.settings import DEFAULT_SETTINGS


def push_http(
        url,
        method='PUT',
        filename=None,
        settings=DEFAULT_SETTINGS,
        **kwargs):
    console = JsonStreams(settings.log_to_console)
    console.input(f'# Push {filename or "data"} to {url}')

    try:
        if filename:
            with open(filename, 'rb') as f:
                r = request(method, url, files=dict(file=f), **kwargs)
        else:
            r = request(method, url, **kwargs)

        console.log(
            f'{method.title()} {filename or "data"} returned {r.status_code}.')
        r.raise_for_status()
    except Exception as e:
        console.error(f'Pushing {filename or "data"} failed: {str(e)}')
        return dict(success=False, console_data=console.data, )

    return dict(success=True, console_data=console.data, )
