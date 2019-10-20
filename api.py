from flask import jsonify
from werkzeug.utils import secure_filename
import os

from hash import hash
import siv
import s3


def processURL(url):
    # Hash URL
    token = hash(url)

    siv.v2json(url, token)

    return token


def processFile(file):
    # Get filename
    filename = secure_filename(file.filename)
    if(filename == ''):
        filename = 'video'


    # Save upload to directory
    path = os.path.join('/tmp', f'{token}_{filename}')
    file.save(path)

    # Hash file
    file.seek(0)
    token = hash(file)
    siv.v2json(path, token)

    return token


def getTranscript(token):
    result = s3.download(f'{token}')
    if not result:
        return jsonify({'message': 'Transcript not found.'}), 404
    else:
        return result
