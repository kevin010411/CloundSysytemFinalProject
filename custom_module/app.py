import os
from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

UPLOAD_FOLDER = "./static/uploads"


app.secret_key = 'secret_key'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
connection_string = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')

try:
    connection = psycopg2.connect(connection_string)
    log = f"psycopg2訪問成功{connection_string}"
except:
    log = f"psycopg2不能訪問{connection_string}"

if connection_string is None:
    # 這是FU的本地postgres
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1111111k@127.0.0.1:5432/postgres"
else:
    # 這是Azure的postgres
    param = dict(item.split("=")
                 for item in connection_string.split(" "))
    connection_string = f'postgresql://{param["user"]}:{param["password"]}@{param["host"]}:{param["port"]}/{param["dbname"]}?sslmode={param["sslmode"]}'
    print(connection_string)
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route("/log")
def display_log():
    return render_template("log.html", logs=[log, connection_string, "測試log畫面"])
