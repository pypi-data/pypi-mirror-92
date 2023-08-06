from ._misc import generate_report, log_plan_statistics, log_versions
from ._pull import pull_http, pull_git
from ._push import push_http
from ._run import run_command, run_script

functions = dict(
    generate_report=generate_report,
    log_plan_statistics=log_plan_statistics,
    log_versions=log_versions,
    pull_git=pull_git,
    pull_http=pull_http,
    push_http=push_http,
    run_command=run_command,
    run_script=run_script,
)
