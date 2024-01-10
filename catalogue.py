from datetime import *
import time
import sys

import json
import requests
# First we set our credentials

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
app = Flask(__name__)
app.debug = True

@app.route('/Video/<video>')
def video_page(video):
    print (video)
    url = 'http://34.16.96.108/myflix/videos?filter={"video.uuid":"'+video+'"}'
    headers = {}
    payload = json.dumps({ })
    print (request.endpoint)
    response = requests.get(url)
    print (url)
    if response.status_code != 200:
      print("Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message']))
      return "Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message'])
    jResp = response.json()
    print (type(jResp))
    print (jResp)
    recommendations = get_recommendations_for_user(1)
    for index in jResp:
        for key in index:
           if (key !="_id"):
              print (index[key])
              for key2 in index[key]:
                  print (key2,index[key][key2])
                  if (key2=="Name"):
                      video=index[key][key2]
                  if (key2=="file"):
                      videofile=index[key][key2]
                  if (key2=="pic"):
                      pic=index[key][key2]
    return render_template('video.html', name=video,file=videofile,pic=pic, recommendations=recommendations)

@app.route('/')
def cat_page():
    url = "http://34.16.96.108/myflix/videos"
    headers = {}
    payload = json.dumps({ })

    response = requests.get(url)
    #print (response)
    # exit if status code is not ok
    print (response)
    print (response.status_code)
    if response.status_code != 200:
      print("Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message']))
      return "Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message'])
    jResp = response.json()
    print (type(jResp))
    html="<h2> Your Videos</h2>"
    for index in jResp:
       #print (json.dumps(index))
       print ("----------------")
       for key in index:

           if (key !="_id"):
              print (index[key])
              for key2 in index[key]:
                  print (key2,index[key][key2])
                  if (key2=="Name"):
                      name=index[key][key2]
                  if (key2=="thumb"):
                      thumb=index[key][key2]
                  if (key2=="uuid"):
                      uuid=index[key][key2]  
              html=html+'<h3>'+name+'</h3>'
              ServerIP=request.host.split(':')[0]
              html=html+'<a href="http://'+ServerIP+'/Video/'+uuid+'">'
              html=html+'<img src="http://35.228.171.94/pics/'+thumb+'">'
              html=html+"</a>"        
              print("=======================")

    return html

RECOMMENDATION_ENGINE_URL = 'http://34.67.49.32'

@app.route('/recommendation/<int:user_id>')
def get_recommendations_for_user(user_id):
    try:
        response = requests.get(f'{RECOMMENDATION_ENGINE_URL}/{user_id}')
        response.raise_for_status()
        recommendations = response.json()
        return render_template('recommendation.html', user_id=user_id, recommendations=recommendations)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []
         


if __name__ == '__main__':
    app.run(host='0.0.0.0',port="5000")
