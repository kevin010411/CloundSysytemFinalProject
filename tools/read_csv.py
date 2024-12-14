import json
from custom_module import db
from custom_module import User, db

if __name__ == "__main__":

    data = dict(
        user_name="admin",
        password="admin"
    )
    new_user = User(name=data['user_name'], password=data['password'])
    session = db.session
    session.add(new_user)
    session.commit()
