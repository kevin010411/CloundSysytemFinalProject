import os
from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

UPLOAD_FOLDER = "./static/uploads"


app.secret_key = 'secret_key'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
connection_string = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING_T')
connection_string_temp = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')
try:
    connection = psycopg2.connect(connection_string_temp)
    log = f"訪問成功{connection_string_temp}"
except:
    log = f"不能訪問{connection_string_temp}"

if connection_string is None:
    connection_string = "dbname=media-database host=media-server.postgres.database.azure.com port=5432 sslmode=require user=htrwgnqpug password=yG4h138eOi1Q$LsP"

if connection_string is None:
    # 這是FU的本地postgres
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1111111k@127.0.0.1:5432/postgres"
else:
    # 這是Azure的postgres
    print(connection_string)
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route("/log")
def display_log():
    return render_template("log.html", log=log)
