from flask import Flask, url_for, jsonify
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

app = Flask(__name__, template_folder='template')
# Example of URL Checking:
# Exmaple of URL checking:
# @app.route('/')
# def index():
#     return 'index'
#
# @app.route('/login')
# def login():
#     return 'login'
#
# @app.route('/user/<username>')
# def profile(username):
#     return f'{username}\'s profile'
#
# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('profile', username='John Doe'))

###example of pages:


from flask import stream_with_context, request, Response

name = 'dani'
##didn't understand
@app.route('/stream')
def streamed_response():
    @stream_with_context
    def generate():
        yield 'Hello '
        yield request.args[name]
        yield '!'
    return Response(generate())



def show_the_login_form():
    return """
    <form action="action_page.php" method="post">
  <div class="imgcontainer">
    <img src="img_avatar2.png" alt="Avatar" class="avatar">
  </div>

  <div class="container">
    <label for="uname"><b>Username</b></label>
    <input type="text" placeholder="Enter Username" name="uname" required>
    <label for="psw"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required>

    <button type="submit">Login</button>
    <label>
      <input type="checkbox" checked="checked" name="remember"> Remember me
    </label>
  </div>

  <div class="container" style="background-color:#f1f1f1">
    <button type="button" class="cancelbtn">Cancel</button>
    <span class="psw">Forgot <a href="#">password?</a></span>
  </div>
</form>"""

from flask import request, render_template


@app.route('/hello2/')
@app.route('/hello2/<name>')
def hello2(name=None):
    return render_template('html.html', name=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

#    {print(about_css.read())}

about_css = open('static\static.css', 'r')
print(about_css.read())
@app.route('/about')
def about():
    return """
    <!DOCTYPE html>
    <html>
    <style>
body {background-color: #FFFFCC;}
h1   {color: blue;}
p    {color: red;}
</style>
    <h>Hello</h>
    <p>I'm P</p>
        <link rel="stylesheet"  type="text/css" href="{ url_for('static', filename='static.css') }">
    <link rel="stylesheet"  type="text/css" href="{ url_for('static', filename='static.css') }">
    <head>
        <title>Hello!!!</title>
         <meta charset="utf-8">
         <meta name="viewport" content="width=device-width/2, initial-scale=1">
    </head>
    <body>
    <h1>i'm h1!</h1>
    <p>Body</p>
    </body>
    </html>"""
def css():
    return url_for('/about', filename='static/static.css')


from markupsafe import escape
@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"
@app.route('/')
def index():
    return 'Index Page'

import random, threading, webbrowser
port = 5000 + random.randint(0, 999)
url = "http://127.0.0.1:{0}".format(port)
threading.Timer(1.25, lambda: webbrowser.open(url) ).start()
app.run(port=port, debug=True)