import datetime
from sqlalchemy import Column, ForeignKey, DateTime, Integer, String, Boolean, Text
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


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(Integer, nullable=False)  # 對應影片 ID
    parent_id = db.Column(Integer, ForeignKey(
        'comments.id'), nullable=True)  # 父留言的 ID
    content = db.Column(Text, nullable=False)  # 留言內容
    created_at = db.Column(DateTime, default=str(
        datetime.datetime.now()))  # 留言時間
    user_name = db.Column(String(100), nullable=False)  # 留言者名稱

    # 父留言關聯
    parent = db.relationship('Comment', remote_side=[id], backref='replies')
