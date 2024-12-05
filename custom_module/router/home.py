from custom_module import app
from sqlalchemy import text
from flask import render_template, request, session

from custom_module import User


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/user_list")
def user_list():
    user_data = User.query.all()
    print(user_data)
    for data in user_data:
        print(type(data.name))
    return render_template("user_list.html", user_list=user_data)


USER_CREDENTIALS = {
    "username": "admin",
    "password": "000000"
}


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            session['login'] = True
            return render_template('home.html')
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')
