#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, render_template, jsonify, redirect, url_for

# Spotify API wrapper, documentation here: http://spotipy.readthedocs.io/en/latest/
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Authenticate with Spotify using the Client Credentials flow
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

app = Flask(__name__, static_folder='public', template_folder='views')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def homepage():
    # Displays homepage
    return render_template('index.html')
  
@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'spotifyimages/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    return render_template("complete.html")
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
    print(APP_ROOT)
    app.run()
    