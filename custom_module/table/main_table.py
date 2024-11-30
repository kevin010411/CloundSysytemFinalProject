from sqlalchemy import Column, ForeignKey, Integer, String
from flask_sqlalchemy import SQLAlchemy

from custom_module import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "all_user"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(32), unique=True)
    password = Column(String(32), nullable=False)
    subcribe_num = Column(Integer, default=0)


class Video(db.Model):
    __tablename__ = "video"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(64), unique=True, nullable=False)
    video_position = Column(String(128), nullable=False)
    watch_num = Column(Integer, default=0)
    good_num = Column(Integer, default=0)
    bad_num = Column(Integer, default=0)
    revenue = Column(Integer, default=0)
