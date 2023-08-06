from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='lambda-run',
    version='0.0.3',
    author='Amit Marcus',
    author_email='marxus@gmail.com',
    description='run code or subprocess on aws lambda invoke context',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/marxus/lambda-run',
    packages=['lambda_run'],
    extras_require={'cli': ['boto3', 'click']},
    entry_points={'console_scripts': ['lambda-run=lambda_run.cli:main [cli]']}
)
