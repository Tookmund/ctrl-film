from flask import Flask, jsonify, request
import tempfile
import os
import forms
import siv
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key=os.environ.get("SECRET_KEY") or os.urandom(16)


def formToJSON():
    form = forms.upload()
    if form.validate_on_submit():
        with tempfile.TemporaryDirectory() as td:
            filename = secure_filename(form.f.file.filename)
            file_path = os.path.join(td, filename)
            form.fileName.file.save(file_path)
            j = siv.v2json(file_path)
            return j
    else:
        return jsonify({'message', 'No form sent.'}), 400


@app.route('/')
def index():
    return 'Hello World!\n'


@app.route('/video/', methods=['GET', 'POST'])
def video():
    if request.method == "POST":
        return formToJSON()
    else:
        return jsonify({'message': 'Video data retrieval not yet available.'}), 501
