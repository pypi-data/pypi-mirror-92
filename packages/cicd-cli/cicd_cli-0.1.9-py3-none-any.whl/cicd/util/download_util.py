import wget
import tempfile

from cicd import config
from cicd.util import file_util


def download_to_bin(url):
    path = wget.download(url, config.BIN_DIR)
    file_util.make_executable(path)


def download_to_tmp(url):
    tfile = tempfile.mkdtemp()
    return wget.download(url, tfile), tfile
