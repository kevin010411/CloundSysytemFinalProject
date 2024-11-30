from custom_module import app
from sqlalchemy import text
from flask import render_template

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
