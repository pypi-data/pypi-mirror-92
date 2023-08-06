import traceback

from .builtin import functions
from .utils.console import JsonStreams, detail
from .utils.task import parse_task, parse_return_value


def execute_task(task_data, plan_settings, env):
    console = JsonStreams(plan_settings.log_to_console)

    task = parse_task(task_data, env, plan_settings)
    task_progress = f' {task.index}' if task.index else ''
    if task.error:
        console.error(f'Failed to parse task{task_progress}: {task.error}')
        return task.result(console, 'error')

    if not task.settings.when:
        console.input(f'# Skip task{task_progress}{detail(task.name)}')
        return task.result(console, 'skipped')

    console.input(
        f'# Execute task{task_progress}: {task.name or task.function}')
    console.log(task.description)

    function = functions.get(task.function)
    if not function:
        console.error(f'Function not found for {task.function}.')
        return task.result(console, 'error')

    try:
        return_value = function(**task.parameters, settings=task.settings)
        success, console_data, new_vars = parse_return_value(return_value)
    except Exception as e:
        console.error(f'Caught error raised from task: {str(e)}')
        if task.settings.debug:
            console.error(traceback.format_exc())
        return task.result(console, 'error')

    if task.settings.register:
        env.register(task.settings.register, return_value)
    if new_vars:
        for key, value in new_vars.items():
            env.register(key, value)

    console.extend(console_data)
    result = 'success' if success else 'fail'
    return task.result(console, result, )
