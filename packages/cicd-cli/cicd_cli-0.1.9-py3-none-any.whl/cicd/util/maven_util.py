import subprocess
import sys
from shutil import which

from cicd import config

from cicd.util import download_util, file_util


def deps():
    if not which('mvn'):
        if sys.platform == 'darwin':
            subprocess.run(['brew', 'install', 'maven'], check=True)
        elif sys.platform == 'linux':
            download_url = 'https://ftp.wayne.edu/apache/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz'
            path, folder = download_util.download_to_tmp(download_url)
            file_util.untar_file(path)
            file_util.add_to_bin(f"{folder}/apache-maven-3.6.3/bin/mvn")


def maven(target, opts='', capture_output=False):
    command = ['mvn']
    if len(opts) > 0:
        command.extend(opts.split(' '))
    if len(target) > 0:
        command.extend(target.split(' '))
    return subprocess.run(command, check=True, capture_output=capture_output)

def install(opts=''):
    maven('clean install', opts)

def get_version():
    versionOutput = maven('exec:exec', "-q -Dexec.executable=echo -Dexec.args='${project.version}' --non-recursive", capture_output=True).stdout
    return versionOutput.decode("utf-8").strip()
