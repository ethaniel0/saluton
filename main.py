from flask import Flask, render_template, request, redirect, make_response
from flask_socketio import SocketIO, send, emit
from random import choice
from db import db, addUser, getProfilePicture, getPalUsername, makePals, getPrevMessages, registerMessage
import deta
from deta import Deta
import random

app = Flask(__name__)
app.static_folder = 'static'
socketio = SocketIO(app)

allPeople = {}

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    name = request.cookies.get('user')
    if name: return redirect('/profile')
    return render_template('login.html')


@app.route('/profile')
def profile():
    name = request.cookies.get('user')
    if not name:
        return redirect('/')
    profpic = getProfilePicture(name)
    return render_template('profile.html', name=name, profpic=profpic)
  
@app.route('/message')
def message():
    name = request.cookies.get('user')
    if not name: return redirect('/')
    profpic = getProfilePicture(name)
    palName = getPalUsername(name)
    if not palName: return redirect('/')
    partnerProfpic = getProfilePicture(palName)
    
    return render_template('message.html', name=name, profpic=profpic, palName=palName, palPic=partnerProfpic)


@app.route('/signin', methods=['POST'])
def signin():
    name = request.form['username'] or 'Bryan'
    resp = make_response(redirect('/profile'))
    resp.set_cookie('user', name)
    user = db.get(name)
    if not user:
        randomProf = random.randint(1, 15)
        addUser(name, randomProf, request.form['password'])
        allAccounts = db.fetch()
        for i in allAccounts.items:
          if i['value'][0] == None and i['key'] != name:
            makePals(name, i['key'])
    return resp


@app.route('/logout', methods=['POST'])
def logout():
    resp = make_response("")
    resp.set_cookie('user', '', expires=0)
    return resp

@socketio.on('connect')
def connect():
  name = request.cookies.get('user')
  messages, senders = getPrevMessages(name)
  data = {
    "texts": messages,
    "senders": senders
  }
  emit('connect', data)
  allPeople[name] = request.sid

@socketio.on('newMessage')
def newMessage(text):
  name = request.cookies.get('user')
  palName = getPalUsername(name)
  if (palName in allPeople):
    emit('message', {"sent": False, "text": text}, room = allPeople[palName])
  emit('message', {"sent": True, "text": text})
  registerMessage(name, palName, text)

@socketio.on('disconnect')
def test_disconnect():
  name = request.cookies.get('user')
  del allPeople[name]
  print('Client disconnected', name)

socketio.run(app, host='0.0.0.0', port=8080)
