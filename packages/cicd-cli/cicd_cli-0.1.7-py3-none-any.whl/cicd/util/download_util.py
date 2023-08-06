import wget
import tempfile


def download_to_bin(url):
    wget.download(url, '/usr/local/bin')


def download_to_tmp(url):
    tfile = tempfile.mkdtemp()
    return wget.download(url, tfile), tfile
