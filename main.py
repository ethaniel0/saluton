from flask import Flask, render_template, request, redirect, make_response
from flask_socketio import SocketIO, send, emit
from random import choice
from db import db, addUser, getProfilePicture, getPalUsername
import deta
from deta import Deta
import random

app = Flask(__name__)
app.static_folder = 'static'
socketio = SocketIO(app)

number_list = [
    100, 101, 200, 201, 202, 204, 206, 207, 300, 301, 302, 303, 304, 305, 307,
    400, 401, 402, 403, 404, 405, 406, 408, 409, 410, 411, 412, 413, 414, 415,
    416, 417, 418, 421, 422, 423, 424, 425, 426, 429, 431, 444, 450, 451, 500,
    502, 503, 504, 506, 507, 508, 509, 510, 511, 599
]


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
    if not name:
        return redirect('/')
    profpic = getProfilePicture(name)
    palName = getPalUsername(name)
    partnerProfpic = getProfilePicture(palName)
    return render_template('message.html', name=name, profpic=profpic)


@app.route('/signin', methods=['POST'])
def signin():
    name = request.form['username'] or 'Bryan'
    resp = make_response(redirect('/profile'))
    resp.set_cookie('user', name)
    user = db.get(name)
    if not user:
        randomProf = random.randint(1, 15)
        addUser(name, randomProf, request.form['password'])

    return resp


@app.route('/logout', methods=['POST'])
def logout():
    resp = make_response("")
    resp.set_cookie('user', '', expires=0)
    return resp


@app.route('/user/', defaults={'username': None})
@app.route('/user/<username>')
def generate_user(username):
    if not username:
        username = request.args.get('username')

    if not username:
        return 'Sorry error something, malformed request.'

    return render_template('personal_user.html', user=username)


@app.route('/page')
def random_page():
    return render_template('page.html', code=choice(number_list))


socketio.run(app, host='0.0.0.0', port=8080, debug=True)
