from flask import Flask, jsonify, request
import os

import api

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(16)


@app.route('/video/', methods=['GET', 'POST'])
def video():
    if request.method == "POST":
        token = 'INVALID'
        if 'file' in request.files:
            token = api.processFile(request.files['file'])
        else:
            url = request.form['url']
            if url != '':
                token = api.processURL(request.form['url'])
        return jsonify({'token': token}), 202
    else:
        if 'token' in request.form:
            return api.getTranscript(request.form['token'])
        else:
            return api.getTranscript(request.args.get('token'))
