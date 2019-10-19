from tempfile import TemporaryDirectory
from werkzeug.utils import secure_filename
import os

from hash import hash
import siv


def processURL(url):
    # Hash URL
    token = hash(url)

    siv.v2json(url, token)

    return token


def processFile(file):
    # Get filename
    filename = secure_filename(file.filename)

    # Hash file
    token = hash(file)

    # Save upload to directory
    path = os.path.join('/uploads', f'{filename}_{token}')
    file.save(path)
    siv.v2json(path, token)

    return token
