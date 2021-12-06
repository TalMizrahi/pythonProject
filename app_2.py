from flask import Flask, request, flash
from flask import url_for
from flask import redirect
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import threading
import webbrowser
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager
from sqlalchemy import create_engine, MetaData, Table


# General Settings
app = Flask(__name__, template_folder='template')
Bootstrap(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


class Todolist(db.Model):
    username = db.Column(db.String(15))
    task_id = db.Column(db.Integer, primary_key=True)
    board = db.Column(db.String(50))
    task_name = db.Column(db.String(200))
    priority = db.Column(db.String(200))
    status = db.Column(db.String(50))
    due_date = db.Column(db.String)


def create_db():
    db.create_all()
    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm (FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=15)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class TodolistForm(FlaskForm):
    task_name = StringField('Goal Name', validators=[InputRequired(), Length(max=50)])
    due_date = StringField('Due Date', validators=[InputRequired(), Length(max=50)])
    priority = StringField('Priority', validators=[InputRequired(), Length(max=50)])
    status = StringField('Status', validators=[InputRequired(), Length(max=50)])


engine = create_engine("sqlite:///database.db")
metadata = MetaData(bind=engine)

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
                login_user(user, remember=form.remember.data)
                return redirect(url_for('todolist'))
        return "<h1> incorrect username or password </h1>"

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


@app.route('/todo_list', methods=['GET', 'POST'])
@login_required
def todolist():
    # data = Todolist.quray.
    if current_user.is_authenticated:
        logged_user = current_user.username
    # todo_table.select(todo_table.username == logged_user).execexecute().first()
    form = TodolistForm(request.form)
    if request.method == "POST" and form.validate():
        new_todo = Todolist(username=logged_user, board="Main",
        task_name=form.task_name.data, due_date=form.due_date.data,
        priority=form.priority.data, status=form.status.data)
        db.session.add(new_todo)
        db.session.commit()
    return render_template("/todo_list.html", form=form)
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
db.create_all()
