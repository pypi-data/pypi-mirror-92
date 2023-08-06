from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from logging import getLogger
from os import fdopen, remove
from runpy import run_path
from subprocess import PIPE, STDOUT, run
from tempfile import mkstemp
from traceback import format_exc
from types import SimpleNamespace as NS

for _logger_handler in getLogger().handlers:
    if hasattr(_logger_handler, 'log_sink'): break
    else: _logger_handler = NS(log_sink=None)


class redirect_log_sink:
    def __init__(self, new):
        self._new = NS(log=new.write, log_error=lambda msgs: new.write('\n'.join(msgs) + '\n'))
        self._olds = []

    def __enter__(self):
        self._olds.append(_logger_handler.log_sink)
        _logger_handler.log_sink = self._new

    def __exit__(self, *exc):
        _logger_handler.log_sink = self._olds.pop()


# using `run_path` over `exec`
# - offers better traceback
# - returns the code as a module
def run_code(code, *args, **kw):
    fd, fp = mkstemp('.py')
    with fdopen(fd, 'w') as f: f.write(code)
    try: return run_path(fp, *args, **kw)
    finally: remove(fp)


def wrap_handler(handler):
    def wrapped(ev, ctx):
        [mode, payload], rsp = ev.get('lambdaRun', ['', '']), None

        if mode in ['py', 'python']:
            rsp = NS(returncode=0, stdout=StringIO())
            try:
                with redirect_stderr(rsp.stdout), \
                     redirect_stdout(rsp.stdout), \
                     redirect_log_sink(rsp.stdout):
                    run_code(payload)
            except:
                rsp.returncode = 1
                rsp.stdout.write(format_exc())
            rsp.stdout = rsp.stdout.getvalue()

        elif mode in ['sh', 'shell']:
            rsp = run(payload, shell=True, stderr=STDOUT, stdout=PIPE, text=True)

        if rsp: return rsp.returncode, rsp.stdout.strip()
        return handler(ev, ctx)

    return wrapped
