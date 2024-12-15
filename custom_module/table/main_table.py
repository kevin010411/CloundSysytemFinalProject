from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text
from flask_sqlalchemy import SQLAlchemy

from custom_module import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "all_user"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(32), unique=True)
    password = Column(String(32), nullable=False)
    subcribe_num = Column(Integer, default=0)
    is_admin = Column(Boolean, default=False)


class Video(db.Model):
    __tablename__ = "video"
    id = Column(Integer, primary_key=True, unique=True)
    title = Column(Text, unique=True, nullable=False)
    #author=Column(Integer, nullable=False) !!!!!!!!!!!!!!!!!!!!!important!!!!!!!!!!!!!!!!!!!
    video_name = Column(String(255), nullable=False)
    cover_img_name = Column(String(255), nullable=False)
    watch_num = Column(Integer, default=0)
    good_num = Column(Integer, default=0)
    bad_num = Column(Integer, default=0)
    share_num = Column(Integer, default=0)
    coin_num = Column(Integer, default=0)
    tag = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
