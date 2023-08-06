import os
import sys

from jinja2 import __version__ as _jinja2_version, Environment, PackageLoader

from pullnrun import __version__
from pullnrun.utils.data import Data, DEFAULT_SETTINGS, Statistics
from pullnrun.utils.console import JsonStreams, detail


def log_versions(settings=DEFAULT_SETTINGS):
    console = JsonStreams(settings.log_to_console)

    console.input(f'# Log versions')
    console.log(f'pullnrun {__version__}')
    console.log(f'jinja2 {_jinja2_version}')
    console.log(f'python {sys.version}')
    console.log(sys.executable)

    return dict(success=True, console_data=console.data, )


def log_plan_statistics(plan_return_value, settings=DEFAULT_SETTINGS):
    console = JsonStreams(settings.log_to_console)

    data = Data(plan_return_value)

    console.input(text=f'# Execution statistics{detail(data.name)}')
    console.log(f'{"Started:":10} {data.started}')
    console.log(f'{"Elapsed:":10} {data.elapsed} s')
    console.log(Statistics(data.statistics).as_str(10))

    return dict(success=True, console_data=console.data, )


def _prefix_if(str_in, prefix, condition):
    return f'{prefix}{str_in}' if condition else str_in


def generate_report(plan_return_value, settings=DEFAULT_SETTINGS):
    console = JsonStreams(settings.log_to_console)

    env = Environment(loader=PackageLoader('pullnrun'))
    env.filters['prefix_if'] = _prefix_if
    template = env.get_template('report.html.j2')
    stream = template.stream(**plan_return_value)

    report_filename = 'pullnrun_report.html'
    with open(report_filename, 'w') as f:
        stream.dump(f)

    console.log(f'Log available in {os.path.realpath(report_filename)}')

    return dict(success=True, console_data=[], )
