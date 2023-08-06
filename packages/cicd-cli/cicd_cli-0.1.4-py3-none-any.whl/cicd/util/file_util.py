import os
import yaml
import shutil
import tarfile
from cicd.logger import log

def untar_file(path, outdir=None):
    if tarfile.is_tarfile(path):
        tarfile.open(path)
    else:
        log.warning(f"Tried to untar non tarfile at {path}")


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