#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
#from client import spotipy as S 
from flask import Flask, request, render_template, jsonify, redirect, url_for, send_from_directory
import json, base64, sys, requests
# Spotify API wrapper, documentation here: http://spotipy.readthedocs.io/en/latest/
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from werkzeug.utils import secure_filename
from spotipy.oauth2 import SpotifyClientCredentials

# Authenticate with Spotify using the Client Credentials flow
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = '/app/images'

GOOGLE_API_KEY = "AIzaSyDShfsGYS3OsyrP46Ea-Lpj_tOvN8fpiVc"
GOOGLE_CLOUD_VISION_URL = "https://vision.googleapis.com/v1/images:annotate"

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
  
  
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

  
@app.route("/upload", methods=['POST'])
def upload():
    print("hi")
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
            tempfile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            img = open(tempfile,"rb") # reading file from glitch's local
            bitimage = base64.b64encode(img.read())
            img.close()
            
            req_data = {
              "requests":[
                {    
                  "image":{
                     "content":bitimage
                  },
                  "features":[
                    {
                      "type":"LABEL_DETECTION",
                      "maxResults":10
                    }
                  ]  
                }
              ]
            }
            
            rt = requests.post("%s?key=%s" % (GOOGLE_CLOUD_VISION_URL, GOOGLE_API_KEY), json.dumps(req_data), headers={'content-type': 'application/json'})
            # print(r.text)
            r = rt.json()
            
            for i in range(len(r["responses"][0]["labelAnnotations"])):
              keyword = r["responses"][0]["labelAnnotations"][i]["description"]
              result = sp.search(keyword, limit = 1, type='playlist')
              
              if(len(result["playlists"]["items"]) >0):
                print(result["playlists"]["items"][0]["name"].encode('utf-8').strip())
            
              if ( i < 1):
                requestBody = {
                            "context_uri": "spotify:album:5ht7ItJgpBH7W6vJ5BqpPr",
                            "offset": {
                                        "position": 5
                                      },
                            "position_ms": 0
                            }
                
                auth = {"Authorization: Bearer BQBaMqBpr_eO9qR48mHin6eHRDjYXA7wvg9jPCIdw8rBuqfu6kwEm1yRz43IKp3lToCfHEXeP2C7WYhMA0PuWvVJoydYRbs56RyqDvi7YQGm8ov75H0TgjdbX8l3LXSwfwofivbh9rAKlTrIaGglxM9QxZMlBpoBwoTbq-OjY8w7j30ZFS6fW89YQwD43jFU-R8TVOz_gtpF8z-WARR6cMkVBXQCnglvK_t64ktl3e9aEryMnj1N4BhET7C9Hj6ToRQ815rn2yLXNWvGrtAKNpg"}
                
                req = requests.put("https://api.spotify.com/v1/me/player/play", data=requestBody, headers = auth )
                
                
            
            return redirect(url_for('uploaded_file', filename=filename))
    
    return render_template("looking_for_music.html")
  
  
@app.route('/upload_image', methods=['GET'])
def upload_image(): #this is old 'def new_releases()' 
  
    # Use the country from the query parameters, if provided
    if 'country' in request.args:
        country = request.args['country']
    else:
        country = 'SE'
    
    # Send request to the Spotify API
    new_releases = sp.new_releases(country=country, limit=20, offset=0)
    
    # Return the list of new releases
    return jsonify(new_releases)

if __name__ == '__main__':
    app.run()
    
################FLASK SPOTIPY#############    
# import os
# from flask import Flask, request, render_template, jsonify

# # Spotify API wrapper, documentation here: http://spotipy.readthedocs.io/en/latest/
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# # Authenticate with Spotify using the Client Credentials flow
# client_credentials_manager = SpotifyClientCredentials()
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# app = Flask(__name__, static_folder='public', template_folder='views')

# @app.route('/')
# def homepage():
#     # Displays homepage
#     return render_template('index.html')
  
# name = fid_dict(predction1)
# results = sp.search(q='track:' + name, type='track')
# print results

  
# @app.route('/new_releases', methods=['GET'])
# def new_releases():
  
#     # Use the country from the query parameters, if provided
#     if 'country' in request.args:
#         country = request.args['country']
#     else:
#         country = 'SE'
    
#     # Send request to the Spotify API
#     new_releases = sp.new_releases(country=country, limit=20, offset=0)
    
#     # Return the list of new releases
#     return jsonify(new_releases)

# if __name__ == '__main__':
#     app.run()
    