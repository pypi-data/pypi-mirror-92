from argparse import ArgumentParser
from datetime import datetime
import json
import sys
import yaml

from ._version import __version__
from .builtin import functions
from .utils.console import JsonStreams
from .utils.settings import Settings, DEFAULT_SETTINGS_DICT
from .utils.statistics import Statistics
from .utils.task import parse_result, parse_task
from .validate import validate_plan


INVALID_PLAN = 251
NO_PLAN = 252


def _name(input_dict):
    name = input_dict.get('name')
    if not name:
        return ''

    return f': {name}'


def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        'plan_file',
        type=str,
        nargs='?',
        help='Load execution plan from JSON or YAML file.')
    parser.add_argument(
        '--version',
        action='store_true',
        help='Print version information.')

    return parser.parse_args()


def load_plan_from_file(filename):
    if not filename:
        raise ValueError('No input file given.')

    with open(filename, 'r') as f:
        if filename.endswith('.json'):
            plan = json.load(f)
        elif filename.endswith('.yaml') or filename.endswith('.yml'):
            plan = yaml.load(f, Loader=yaml.SafeLoader)
        else:
            raise ValueError(
                'Failed to recognize file type. '
                'File extension must be json, yaml, or yml.')

    return plan


def main(plan):
    try:
        validate_plan(plan)
    except Exception as e:
        print(f'Failed to validate plan: {str(e)}')
        exit(INVALID_PLAN)

    plan_settings = Settings(DEFAULT_SETTINGS_DICT)(plan)
    stats = Statistics()
    console = JsonStreams(plan_settings.log_to_console)

    started = datetime.utcnow()
    tasks = plan.get('tasks')
    console.input(f'# Start plan execution{_name(plan)}')
    console.log(f'pullnrun {__version__}')
    console.log(f'python {sys.version}')
    console.log(sys.executable)

    for i, task in enumerate(tasks, start=1):
        try:
            console.input(f'# Parse task {i}/{len(tasks)}{_name(task)}')
            name, function_name, parameters, settings = parse_task(
                task, plan_settings)
        except ValueError as e:
            console.error(f'Failed to parse task: {str(e)}')
            settings = plan_settings(task)
            if settings.stop_on_errors:
                stats.add('error')
                break
            else:
                stats.add('ignored')
                continue

        console.input(f'# Execute task: {name or function_name}')
        function = functions.get(function_name)
        if not function:
            console.error(f'Function not found for {function_name}.')
            if settings.stop_on_errors:
                stats.add('error')
                break
            else:
                stats.add('ignored')
                continue

        try:
            success, console_data = parse_result(
                function(**parameters, settings=settings))
        except Exception as e:
            console.error(f'Caught error raised from task: {str(e)}')
            if settings.stop_on_errors:
                stats.add('error')
                break
            else:
                stats.add('ignored')
                continue

        console.extend(console_data)
        stats.add('success' if success else 'fail')
        if not success and settings.stop_on_errors:
            break

    elapsed = (datetime.utcnow() - started).total_seconds()

    console.input(text=f'# Plan execution completed{_name(plan)}')
    console.input(text=f'# Execution statistics{_name(plan)}')
    console.log(f'{"Started:":10} {started.isoformat()}Z')
    console.log(f'{"Elapsed:":10} {elapsed} s')
    console.log(stats.as_str(10))

    return (started, elapsed, stats, console.data)


def entrypoint():
    args = get_args()
    if args.version:
        print(f'pullnrun {__version__}')
        return

    try:
        plan = load_plan_from_file(args.plan_file)
    except ValueError as e:
        print(str(e))
        exit(NO_PLAN)

    _, _, stats, _ = main(plan)
    exit(stats.error + stats.fail)
