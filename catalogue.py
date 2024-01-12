from datetime import *
import time
import sys
import telnetlib
import random
import json
import requests
import subprocess





# First we set our credentials

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
app = Flask(__name__)
app.debug = True



telnet_host = "35.202.42.46"
telnet_port = 80

def get_recommendations():
    try:
        # Create a Telnet object
        tn = telnetlib.Telnet(telnet_host, telnet_port, timeout=5)

        # Replace the following line with your logic to generate a random number
        random_number = str(random.randint(1, 400))

        # Send the random number to telnet
        tn.write(f"{random_number}\n".encode('ascii'))

        # Read the output from telnet
        telnet_output = tn.read_until(b"\n", timeout=5).decode('utf-8')

        # Close the telnet connection
        tn.close()

        # Print the telnet output for debugging
        print("Telnet Output:", telnet_output)

        return telnet_output
    except Exception as e:
        print(f"Error: {e}")
        return None


def parse_recommendations(recommendations):
    recommendations_list = []
    lines = recommendations.split('\n')[1:-1]  # Skip the first and last lines
    for line in lines:
        parts = line.split(':')
        if len(parts) == 2:
            title, genres = parts[0], parts[1]
            recommendations_list.append({'title': title, 'genres': genres})
    return recommendations_list



@app.route('/Video/<video>')
def video_page(video):
    print (video)
    url = 'http://34.125.114.98/myflix/videos?filter={"video.uuid":"'+video+'"}'
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

    return render_template('video.html', name=video,file=videofile,pic=pic)


@app.route('/')
def cat_page():
    url = "http://34.125.114.98/myflix/videos"
    headers = {}
    payload = json.dumps({ })

    response = requests.get(url)
    print(response)
    print(response.status_code)
    if response.status_code != 200:
        print("Unexpected response:", response)
        return "Unexpected response from myflix service."

    jResp = response.json()
    print(type(jResp))
    html = "<h2> Your Videos</h2>"
    for index in jResp:
        print("----------------")
        for key in index:
            if key != "_id":
                print(index[key])
                for key2 in index[key]:
                    print(key2, index[key][key2])
                    if key2 == "Name":
                        name = index[key][key2]
                    if key2 == "thumb":
                        thumb = index[key][key2]
                    if key2 == "uuid":
                        uuid = index[key][key2]
                html += '<h3>' + name + '</h3>'
                ServerIP = request.host.split(':')[0]
                html += '<a href="http://' + ServerIP + '/Video/' + uuid + '">'
                html += '<img src="http://34.125.64.206/pics/' + thumb + '">'
                html += "</a>"
                print("=======================")

    recommendations = get_recommendations()
    if recommendations is not None:
        # Parse recommendations
        recommended_movies = parse_recommendations(recommendations)

        # Display recommended movies on the main page
        html += "<h2> Recommended Movies</h2>"
        for movie in recommended_movies:
            html += '<h3>' + movie['title'] + '</h3>'
            html += '<p>' + movie['genres'] + '</p>'
    else:
        print("Failed to retrieve recommendations.")

        






    html += "<pre>" + recommendations + "</pre>"
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0',port="5000")
