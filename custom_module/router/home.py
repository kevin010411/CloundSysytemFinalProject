from custom_module import app
from sqlalchemy import select
from flask import render_template, request, redirect, session

from custom_module import User, db


@app.route("/")
def index():
    is_admin = session.get('is_admin', False)
    return render_template("home.html", is_admin=is_admin)


@app.route("/user_list")
def user_list():
    user_data = User.query.all()
    return render_template("user_list.html", user_list=user_data)


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    db_session = db.session
    user_data = db_session.query(User).filter_by(name=username).first()
    if user_data:
        if username == user_data.name and password == user_data.password:
            session['login'] = True
            session['is_admin'] = user_data.is_admin
            return redirect('/')

    return render_template('login.html', error='Invalid username or password')


@app.route('/video', methods=['GET'])
def video_get():
    return render_template('video.html')
