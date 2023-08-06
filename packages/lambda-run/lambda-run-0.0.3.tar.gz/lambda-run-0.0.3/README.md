# lambda-run
run python code or shell commands on aws lambda invoke context

### install:
```
# use bare package for production
$ pip install lambda-run

# use to install dev dependencies
# needed to execute commands from cli 
$ pip install lambda-run[cli]
```

#### usage:
wrap your lambda function like this:
```python
import lambda_run

# wrapping will catch 'lambdaRun' events
# otherwise it will pass the event forward
@lambda_run.wrap_handler
def lambda_handler(event, context):
    # your regular lambda handler...
    print(event, context) 
    return 'OK' 
```

execute commands from cli:
```shell
# set AWS env vars for boto3
export AWS_PROFILE=profile AWS_DEFAULT_REGION=eu-west-1

# Usage: lambda-run [OPTIONS] FUNCTION_NAME [PAYLOAD]

# attach payload directly as last argument
lambda-run -m python my-lambda 'import sys; print(sys.path)'

# or by posix pipe/redirect, for example: 
# pipe it
echo 'import sys; print(sys.path)' | lambda-run -m python my-lambda 

# oneliner redirect
lambda-run -m shell my-lambda <<<'python manage.py createsuperuser'

# or multiline
lambda-run -m python my-lambda <<EOF
for i in range(10):
    print(i)
EOF

# or file content
lambda-run -m shell my-lambda <bash-script.sh
```
