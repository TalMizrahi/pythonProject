from flask import Flask, request, jsonify, flash
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
from sqlalchemy import create_engine, MetaData
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


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


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


class Todolist(db.Model):
    username = db.Column(db.String(15))
    id = db.Column(db.Integer, primary_key=True)
    board = db.Column(db.String(50))
    task_name = db.Column(db.String(200))
    priority = db.Column(db.String(200))
    status = db.Column(db.String(50))
    due_date = db.Column(db.String)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def is_user_logged_in():
    return current_user.is_authenticated


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=15)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class TodolistForm(FlaskForm):
    task_name = StringField('Goal', validators=[InputRequired(), Length(max=50)])
    due_date = StringField('Due Date', validators=[InputRequired(), Length(max=50)])
    priority = StringField('Priority', validators=[InputRequired(), Length(max=50)])
    status = StringField('Status', validators=[InputRequired(), Length(max=50)])


engine = create_engine("sqlite:///database.db")
metadata = MetaData(bind=engine)


def sql_query(query, params):
   conn = get_db_connection()
   cur = conn.cursor()
   cur.execute(query, params)
   rows = cur.fetchall()
   return rows


# pages of the app:
@app.route("/")
def index():
    user_logged = is_user_logged_in()
    return render_template("index.html", user_logged=user_logged)


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

@app.route("/logout")
def logout():
    logout_user()
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        flash('Thanks for registering')
        db.session.commit()
        sql = """INSERT INTO Todolist (username, board, task_name, due_date, priority, status)
                    VALUES 
                    (?, 'main',' Welcome! :) Click Done to add this to Done-List :)', 'Date in any Format!', 'High-Mid-Low',' To-Do!'),
                    (?, 'main', 'You can double click here to Edit Anytime!','Anytime','High!','In-Progress'),
                    (?, 'main', 'Some important stuff like Pay Bills',' till friday','High','To-Do'),
                    (?, 'main','Plan my Next Vacation','Tomorrow at 20 pm', 'Mid','To-Do'),
                    (?, 'main','Swim','After Work, 21:00', 'Mid','To-Do'),
                    (?, 'main','Buy Flowers to my Wife','14-02-2022', 'Highest','In-Progress')"""
        print(sql)
        data = (form.username.data,form.username.data,form.username.data,form.username.data,form.username.data,form.username.data)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return redirect("login")

    return render_template("register.html", form=form)


@app.route('/about')
def about():
    user_logged = is_user_logged_in()
    return render_template('/about.html/', user_logged=user_logged)


@app.route('/todo_list', methods=['GET', 'POST'])
@login_required
def todolist():
    user_logged = is_user_logged_in()
    if current_user.is_authenticated:
        logged_user = current_user.username
    form = TodolistForm(request.form)
    if request.method == "POST" and form.validate():
        new_todo = Todolist(username=logged_user, board="main",
                            task_name=form.task_name.data, due_date=form.due_date.data,
                            priority=form.priority.data, status=form.status.data)
        db.session.add(new_todo)
        db.session.commit()
    conn = get_db_connection()
    todolist_table = sql_query('SELECT id, task_name, due_date, priority,status FROM `Todolist` WHERE username =? and board=?',
                               [logged_user,'main'])
    done_list_table = sql_query('SELECT id, task_name, due_date, priority,status FROM `Todolist` WHERE username =? and board=?',
                               [logged_user,'done'])
    return render_template("/todo_list.html", form=form, Todolist=Todolist, todolist_table=todolist_table,done_list_table=done_list_table, user_logged=user_logged,logged_user=logged_user)


@app.route("/delete_todo/<string:id>", methods=['GET', 'POST'])
def delete_todo(id):
    user_logged = is_user_logged_in()
    if current_user.is_authenticated:
        logged_user = current_user.username
    form = TodolistForm(request.form)
    try:
            conn = get_db_connection()
            cursor = conn.cursor()
            print("test3")
            print(id, type(id))
            sql = "DELETE FROM Todolist WHERE id=?"
            print(sql)
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, [id])
            conn.commit()
            success = 1
            print("1")
            return redirect("/todo_list")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
    return render_template("/todo_list.html", Todolist=Todolist, form=form)


@app.route("/edit_todo", methods=['GET', 'POST'])
@login_required
def edit_todo():
    user_logged = is_user_logged_in()
    if current_user.is_authenticated:
        logged_user = current_user.username
    form = TodolistForm(request.form)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if request.method == 'POST':
                field = request.form['field']
                value = request.form['value']
                editid = request.form['id']
                print(value, editid, type(value), type(editid))
                if field == "task_name":
                    sql = "UPDATE Todolist SET task_name=? WHERE id=?"
                    print(sql)
                if field == "due_date":
                    sql = "UPDATE Todolist SET due_date=? WHERE id=?"
                    print(sql)
                if field == "priority":
                    sql = "UPDATE Todolist SET priority=? WHERE id=?"
                    print(sql)
                if field == "status":
                    sql = "UPDATE Todolist SET status=? WHERE id=?"
                    print(sql)
                data = (value, editid)
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                success = 1
        return jsonify(success)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
    return render_template("/todo_list.html", Todolist=Todolist, form=form, user_logged=user_logged)

@app.route("/done_todo/<string:row_data>", methods=['GET', 'POST'])
def done_todo(row_data):
    print(row_data)
    row_data = row_data.split("@@@@")
    id = row_data[0]
    task_name = row_data[1]
    due_date = row_data[2]
    priority = row_data[3]
    status = row_data[4]
    user_logged = is_user_logged_in()
    if current_user.is_authenticated:
        logged_user = current_user.username
    form = TodolistForm(request.form)
    try:
            conn = get_db_connection()
            cursor = conn.cursor()
            print("test3")
            print(id, type(id))
            sql = "DELETE FROM Todolist WHERE id=?"
            print(sql)
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql, [id])
            sql = """INSERT INTO Todolist (username, board, task_name, due_date, priority, status)
                        VALUES 
                        (?,'done' ,?, ?,?,?)"""
            print(sql)
            data = (logged_user, task_name, due_date, priority, status)
            cursor.execute(sql, data)
            conn.commit()
            success = 1
            print("1")
            return redirect("/todo_list")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
    return render_template("/todo_list.html", Todolist=Todolist, form=form)


port = 5000  # + random.randint(0, 999)
url = "http://127.0.0.1:{0}".format(port)

threading.Timer(1.25, lambda: webbrowser.open(url)).start()
app.run(port=port, debug=True)