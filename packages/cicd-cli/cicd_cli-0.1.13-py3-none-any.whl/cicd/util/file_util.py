import os
import stat
import yaml
import shutil
import tarfile
import subprocess

from cicd import config

from cicd.logger import log


def untar_file(path):
    if tarfile.is_tarfile(path):
        subprocess.run(['tar', 'xf', path], cwd=os.path.dirname(path), check=True)
    else:
        log.warning(f"Tried to untar non tarfile at {path}")


def unzip_file(path):
    subprocess.run(['unzip', path], cwd=os.path.dirname(path), check=True)


def add_to_bin(path, symlink=False):
    filename = os.path.basename(path)
    target = f"{config.BIN_DIR}/{filename}"
    if symlink:
        os.symlink(path, target)
    else:
        copyfile(path, target)
    make_executable(target)


def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(path, mode)


def readYamlFile(path):
    with open(path) as configs:
        return yaml.load(configs, Loader=yaml.FullLoader)

def readFileAsString(path):
    with open(path, 'r') as template:
        return template.read()

def getFilesInFolder(path):
    files = []
    for (filepath, _, filenames) in os.walk(path):
        for filename in filenames:
            files.append(f"{filepath}/{filename}")
    return files

def isFile(path):
    return os.path.exists(path)

def copyfile(source, target):
    shutil.copyfile(source, target)

def get_cwd():
    return os.getcwd()

def rm(path, ignore_errors=False):
    if os.path.exists(path):
        if (os.path.isdir(path)):
            shutil.rmtree(path, ignore_errors=ignore_errors)
        else:
            os.remove(path)

def abspath(path):
    return os.path.abspath(path)