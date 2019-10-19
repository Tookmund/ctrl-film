from tempfile import TemporaryDirectory
from werkzeug.utils import secure_filename
import os

import siv


def processURL(url):
    pass


def processFile(file):
    # Get filename
    filename = secure_filename(file)

    # Create temporary directory
    with TemporaryDirectory() as dir:
        file.save(os.path.join(dir, filename))
