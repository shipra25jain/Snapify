#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, render_template, jsonify, redirect, url_for, send_from_directory

# Spotify API wrapper, documentation here: http://spotipy.readthedocs.io/en/latest/
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = '/path/to/the/uploads'

# Authenticate with Spotify using the Client Credentials flow
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

app = Flask(__name__, static_folder='public', template_folder='views')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/')
def homepage():

    # print(A)
    return render_template('index.html')
  
@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    
    return render_template("looking_for_music.html")
  
  
# @app.route('/upload_image', methods=['GET'])
# def upload_image(): #this is old 'def new_releases()' 
  
#     # Use the country from the query parameters, if provided
#     if 'country' in request.args:
#         country = request.args['country']
#     else:
#         country = 'SE'
    
#     # Send request to the Spotify API
#     new_releases = sp.new_releases(country=country, limit=20, offset=0)
    
#     # Return the list of new releases
#     return jsonify(new_releases)

if __name__ == '__main__':
    app.run()
    