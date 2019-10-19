from flask import Flask
import tempfile
import os
import forms
import siv

app = Flask(__name__)

app.secret_key=os.environ.get("SECRET_KEY") or os.urandom(16)

@app.route('/')
def index():
    return 'Hello World!\n'

@app.route('/video/', methods=['GET', 'POST'])
def video():
    form = forms.upload()
    if form.validate_on_submit():
        with tempfile.TemporaryDirectory() as td:
            filename = secure_filename(form.f.file.filename)
            file_path = os.path.join(td, filename)
            form.fileName.file.save(file_path)
            j = siv.v2json(file_path)
            return j
    else:
        return 'no form yet\n'
