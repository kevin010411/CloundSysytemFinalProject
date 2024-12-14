from custom_module import User, db, app
import json
import sys


@app.route("/api/admin/test")
def read_csv():

    data = dict(
        user_name="admin",
        password="admin"
    )
    new_user = User(name=data['user_name'], password=data['password'])
    session = db.session
    session.add(new_user)
    session.commit()
