from flask import Flask
from flask import  url_for
from  flask import  redirect
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import threading
import webbrowser
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import  generate_password_hash
from werkzeug.security import  check_password_hash

# General Settings
app = Flask(__name__, template_folder='template')
Bootstrap(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


class LoginForm (FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=15)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


# pages of the app:
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                return redirect(url_for('about'))
        return "<h1> incorrect username or password </h1>"

        # return "<h1>" + form.username.data + " " + form.password.data + "</h1>"
    return render_template("login.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1> new user has created </h1>'
    # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data

    return render_template("register.html", form=form)


@app.route('/about')
def about():
    return render_template('/about.html/')


@app.route('/todo_list')
def todolist():

    return render_template("/todo_list.html")




# Run the server on a local host:


port = 5000  # + random.randint(0, 999)
url = "http://127.0.0.1:{0}".format(port)

threading.Timer(1.25, lambda: webbrowser.open(url)).start()
app.run(port=port, debug=True)

admin = User('admin', 'admin@example.com')
guest = User('guest', 'guest@example.com')
db.session.add(admin)
db.session.add(guest)
db.session.commit()
users = User.query.all()
print (users)