from datetime import datetime

from jinja2.exceptions import UndefinedError

from .data import Data, Meta


class Task(Data):
    def __init__(self, meta, function_name, parameters, settings, error=None):
        super().__init__(dict(
            **meta.json,
            started=datetime.utcnow(),
            function=function_name,
            parameters=parameters,
            settings=settings,
        ))
        self.error = error

    def result(self, console, result, return_value=None):
        if result in ('error', 'fail',) and not self.settings.stop_on_errors:
            result = 'ignored'

        json = {
            **self.json,
            'started': f'{self.started.isoformat()}Z',
            'settings': self.settings.json,
        }

        return dict(
            **json,
            elapsed=(datetime.utcnow() - self.started).total_seconds(),
            console_data=console.data,
            result=result,
            return_value=return_value,
        )


def _parse_task_settings(task, env, settings):
    try:
        when = env.resolve_expression(task.get('when'))
    except UndefinedError:
        when = False

    task = {
        **task,
        'when': when
    }

    task_settings = settings(task)
    meta = Meta(task)

    for key in [*settings.keys(), *meta.keys()]:
        task.pop(key, None)

    return (meta, task, task_settings)


def parse_task(task, env, settings):
    meta, task, task_settings = _parse_task_settings(task, env, settings)

    task_index = env.get('pullnrun_task_index')
    task_count = env.get('pullnrun_task_count')
    meta.index = (
        f'{task_index}/{task_count}' if task_index and task_count else None)

    if not task_settings.when:
        return Task(meta, None, None, task_settings)

    if len(task.keys()) != 1:
        error = (
            'Task must contain exactly one function key, '
            f'but {len(task.keys())} were given ({", ".join(task.keys())}).')
        return Task(meta, None, None, task_settings, error=error)
    function_name, parameters = next(i for i in task.items())

    if task_settings.resolve_templates:
        parameters = env.resolve_templates(parameters)

    return Task(meta, function_name, parameters, task_settings,)


def parse_return_value(result):
    return (result.get('success'), result.get(
        'console_data'), result.get('vars'), )
