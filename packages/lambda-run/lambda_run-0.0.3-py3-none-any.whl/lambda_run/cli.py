try:
    from boto3 import client
    from click import BadParameter, UsageError, argument, command, option
except ImportError:
    (print('import error for boto3, click' '\n'
           'did you install `lambda-run[cli]`?'), exit(1))
from json import dumps, loads
from sys import stdin


def invoke(fn, mode, payload):
    returncode, stdout = loads(client('lambda').invoke(
        FunctionName=fn,
        Payload=dumps({'lambdaRun': [mode, payload]})
    )['Payload'].read())
    (print(stdout), exit(returncode))


modes = ['py', 'python', 'sh', 'shell']


@command()
@option('--mode', '-m', help=', '.join(modes))
@argument('fn', metavar='FUNCTION_NAME')
@argument('payload', required=False)
def main(fn, mode, payload):
    if mode not in modes:
        raise BadParameter(', '.join(modes))
    if not payload and not stdin.isatty():
        payload = ''.join(stdin)
    if not payload:
        raise UsageError("Missing argument 'PAYLOAD'.")
    invoke(fn, mode, payload)


if __name__ == '__main__':
    main()
