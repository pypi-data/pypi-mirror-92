import cicd.logger as logger
import subprocess
import os
import cicd.secret as secret

def run_tests(capture_output=False):
    return python('setup.py test')

def build():
    return python('setup.py sdist bdist_wheel')

def get_version():
    version_output = python('setup.py --version', capture_output=True).stdout
    return version_output.decode('utf-8').strip()

def publish(name, version):
    if 'not_found' == secret.PYPI_USER or 'not_found' == secret.PYPI_PASS:
        raise Exception('Pypi credentials must be set to publish a python package')
    command = [
        'twine',
        'upload',
        f"dist/{name}-{version}-*",
        '-u', secret.PYPI_USER,
        '-p', secret.PYPI_PASS,
    ]
    subprocess.run(command, check=True)
    

def get_name():
    name_output = python('setup.py --name', capture_output=True).stdout
    name = name_output.decode('utf-8').strip()
    return name.replace('-', '_')

def python(args: str, path='python3', capture_output=False):
    command = [ path ]
    args = args.split(' ')
    command.extend(args)
    return subprocess.run(
        command,
        check=True,
        capture_output=capture_output,
    )
