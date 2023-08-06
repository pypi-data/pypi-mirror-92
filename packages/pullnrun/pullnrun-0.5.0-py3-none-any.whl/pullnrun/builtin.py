from .pull import pull_http, pull_git
from .push import push_http
from .run import run_command, run_script

functions = dict(
    pull_git=pull_git,
    pull_http=pull_http,
    push_http=push_http,
    run_command=run_command,
    run_script=run_script,
)
