import subprocess
from cicd.util import aws_util, download_util, file_util
from shutil import which
import sys


def deps():
    if not which('helm'):
        if sys.platform == 'darwin':
            subprocess.run(['brew', 'install', 'helm'], check=True)
        if sys.platform == 'linux':
            path, folder = download_util.download_to_tmp("https://get.helm.sh/helm-v3.5.0-linux-amd64.tar.gz")
            file_util.untar_file(path)
            file_util.copyfile(f"{folder}/linux-amd64/helm", '/usr/local/bin')


def deploy(application_name, lifecycle, version, chart):
    repository = aws_util.get_repository(application_name, lifecycle)
    repository_uri = repository['repositoryUri']
    opts = [
        '--install',
        '-f', '.cicd_config.yml',
        '-n', lifecycle,
        '--set', f"deployment.image={repository_uri}",
        '--set', f"deployment.version={version}",
        '--set', f"deployment.env.LIFECYCLE={lifecycle}",
        application_name, chart,
    ]
    helm('upgrade', opts)

def delete(application_name, lifecycle):
    helm('delete', [
        '-n', lifecycle,
        application_name,
    ])

def update_repo():
    helm('repo', ['add', 'pago', 's3://pago-charts'])
    helm('repo', ['update'])

def helm(action, opts=[]):
    command = ['helm', action]
    command.extend(opts)
    subprocess.run(command, check=True)
