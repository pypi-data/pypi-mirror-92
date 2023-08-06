import shlex
from subprocess import run

from .utils.console import JsonStreams, command_as_str
from .utils.settings import DEFAULT_SETTINGS
from .utils.task import parse_result


def run_command(command, settings=DEFAULT_SETTINGS, **kwargs):
    if isinstance(command, str):
        command = shlex.split(command)

    with JsonStreams(
        log_to_console=settings.log_to_console
    ) as (stdout, stderr, streams):
        streams.push('stdin', text=command_as_str(command))
        process = run(
            command,
            stderr=stderr,
            stdout=stdout,
            bufsize=0,
            **kwargs)

    return dict(
        success=process.returncode == 0,
        console_data=streams.read(wait=True),
    )


def run_script(script, settings=DEFAULT_SETTINGS, **kwargs):
    console_data = []

    for command in script:
        success, new_lines = parse_result(
            run_command(command, settings, **kwargs))
        console_data.extend(new_lines)

        if settings.stop_on_errors and not success:
            return dict(success=False, console_data=console_data, )

    return dict(success=True, console_data=console_data, )
