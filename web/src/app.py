import requests
import json
import os
import hashlib
import pdb

from flask import render_template
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(12).hex()


url = "http://api:8080/malware"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    sample = None
    if request.method == 'POST':
        # check if the post request has the file part
        print("Check if file in post request")
        if 'file' not in request.files:
            print("[+] redirecting for some reason")
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        print("Check if filename is empty")
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        print("[+] Saved to ", path)

        # Derive hash
        with open(path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
            res = requests.get(url + f"/{file_hash}")
            sample = json.loads(res.text)
        return render_template('upload.html', sample=sample)
    return render_template('upload.html', sample=sample)

@app.route('/add', methods=['GET', 'POST'])
def add_samples():
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        # Get some stuffs from a form then post it to remote.
        data = {}
        data['name'] = request.form['name']
        data['hash'] = request.form['hash']
        data['tags'] = list(map(str, request.form['tags'].split()))
        print(data)
        res = requests.post(url, json=data)
        return redirect('/')