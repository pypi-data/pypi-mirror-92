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
            path = download_util.download_to_dir(download_url, config.MAVEN_HOME)
            file_util.untar_file(path)
            file_util.add_to_bin(f"{config.MAVEN_HOME}/apache-maven-3.6.3/bin/mvn", symlink=True)
            file_util.rm(f"{config.MAVEN_HOME}/apache-maven-3.6.3-bin.tar.gz")


def maven(target, opts='', capture_output=False):
    command = ['mvn']
    if config.MAVEN_SETTINGS is not None:
        command.extend(['-s', config.MAVEN_SETTINGS])
    if len(opts) > 0:
        command.extend(opts.split(' '))
    if len(target) > 0:
        command.extend(target.split(' '))
    return subprocess.run(command, check=True, capture_output=capture_output)


def install(opts=''):
    maven('clean install', opts)


def get_version():
    version_output = maven(
        'exec:exec', "-q -Dexec.executable=echo -Dexec.args='${project.version}' --non-recursive",
        capture_output=True
    ).stdout
    return version_output.decode("utf-8").strip()
