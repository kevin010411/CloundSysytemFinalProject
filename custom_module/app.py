import os
from flask import Flask

app = Flask(__name__)

UPLOAD_FOLDER = "./static/uploads"


app.secret_key = 'secret_key'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
connection_string = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')
if connection_string is None:
    # 這是FU的本地postgres
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1111111k@127.0.0.1:5432/postgres"
else:
    # 這是Azure的postgres
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
