from datetime import *
import time
import sys
import telnetlib
import random
import json
import requests
import subprocess
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

# First we set our credentials

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
app = Flask(__name__)
app.debug = True


telnet_host = "34.170.199.102"
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
        telnet_output = tn.read_until(b"\r\n", timeout=5).decode('utf-8')
       
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
    lines = recommendations.strip().split('\n')  # Skip the first and last lines
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
        html += "<h2> Recommended Movies xd</h2>"
       
       
    html += "<pre>" + recommendations + "</pre>" 
    return html

app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = '34.16.195.113'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'users_db'
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('user.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port="5000")
