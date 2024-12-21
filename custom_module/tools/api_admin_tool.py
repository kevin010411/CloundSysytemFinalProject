from custom_module import User
import random

from flask import request
from custom_module import Video, User, db, app
import csv


def generate_usernames(count=10):
    # 名字的組成部分
    first_parts = ["Happy", "Sad", "Cool", "Smart",
                   "Shiny", "Angry", "Lazy", "Brave", "Funny", "Crazy"]
    second_parts = ["Cat", "Dog", "Tiger", "Panda",
                    "Lion", "Bear", "Fox", "Wolf", "Koala", "Monkey"]
    numbers = list(range(100, 999))  # 三位數字

    # 組合名字
    usernames = []
    for _ in range(count):
        first = random.choice(first_parts)
        second = random.choice(second_parts)
        number = random.choice(numbers)
        username = f"{first}{second}{number}"
        usernames.append(username)

    return usernames


@app.route("/api/admin/create_dummy_user", methods=["GET"])
def create_dummy_user():
    counts = request.args.get("counts", default=10, type=int)
    create_admin_user()
    username_list = generate_usernames(counts)
    user_list = []
    for username in username_list:
        password = "admin"
        existing_user = User.query.filter_by(name=username).first()
        if existing_user:
            print(f"{username}已經存在")
            continue
        new_user = User(name=username,
                        password=password, is_admin=False)
        user_list.append(new_user)
    session = db.session
    session.add_all(user_list)
    session.commit()
    return "Add Dummy User Sucess"


@app.route("/api/admin/read_item_info", methods=["GET"])
def read_item_info():
    from sqlalchemy.sql.expression import func
    VIDEO_COUNTS = request.args.get("counts", default=100, type=int)
    with open(app.static_folder+"/item_info.csv", mode='r', encoding="UTF-8", newline='') as csv_file:
        reader = list(csv.DictReader(csv_file))
        session = db.session
        videos = []
        random_user = db.session.query(User.id).order_by(
            func.random()).limit(VIDEO_COUNTS).all()
        for row in reader[:VIDEO_COUNTS]:
            # 建立 Video 實例
            video = Video(
                title=row["title"],
                video_name="rick_and_roll.mp4",  # 替換為實際的預設路徑
                cover_img_name=row["item_id"],  # 替換為實際的預設路徑
                watch_num=int(float(row["view_number"])),
                good_num=int(float(row["thumbup_number"])),
                author=random.choice(random_user).id,
                tag=row["tag"],
                share_num=int(float(row["share_number"])),
                coin_num=int(float(row["coin_number"])),
                description=row["description"],
            )
            videos.append(video)

        BATCH_SIZE = 16
        for start in range(0, len(videos), BATCH_SIZE):
            batch = videos[start:start + BATCH_SIZE]
            session.bulk_save_objects(batch)  # 批量插入資料
            session.commit()

    return "add Video and Connect to User"


def create_admin_user():
    data = dict(
        user_name="admin",
        password="admin"
    )
    existing_user = User.query.filter_by(name=data["user_name"]).first()
    if existing_user:
        return f"{data['user_name']}已經存在"
    new_user = User(name=data['user_name'],
                    password=data['password'], is_admin=True)
    session = db.session
    session.add(new_user)
    session.commit()
    return "create a admin user"


@app.route('/api/admin/dp/create_all')
def dp_create_all():
    db.create_all()
    return 'dp create successfully'


@app.route('/api/admin/dp/drop_all')
def dp_drop_all():
    db.drop_all()
    return 'dp delete successfully'
