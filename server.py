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

@app.route("/getimage" methods=['GET'])

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(request.form['token'])
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            tempfile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # imagedataFile = open('/app/public/imagedataFile.txt','w')
            # imagedataFile.write(tempfile)
            # imagedataFile.close()
            img = open(tempfile,'rb') # reading file from glitch's local
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
                            "context_uri": result["playlists"]["items"][0]["uri"].encode('utf-8').strip()
                            }
                print(requestBody)
                
                token = request.form['token']
                
                auth = {"Authorization": "Bearer {0}".format(token)}
                auth["Content-Type"] = "application/json"
                print(auth)
                
                
                req = requests.put("https://api.spotify.com/v1/me/player/play", data=json.dumps(requestBody), headers = auth )
                print(req.text)
                
            
            return redirect(url_for('uploaded_file', filename=filename))
    
    return render_template("looking_for_music.html")


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
    