from custom_module import Video, db, app
import csv

from custom_module.table.main_table import User


@app.route("/api/admin/read_item_info", methods=["GET"])
def read_item_info():
    with open(app.static_folder+"/item_info.csv", mode='r', encoding="UTF-8", newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        session = db.session
        videos = []
        for row in list(reader)[:50]:
            # 建立 Video 實例
            video = Video(
                title=row["title"],
                video_name="rick_and_roll.mp4",  # 替換為實際的預設路徑
                cover_img_name=row["item_id"],  # 替換為實際的預設路徑
                watch_num=int(float(row["view_number"])),
                good_num=int(float(row["thumbup_number"])),
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

    return "Admin add to User Table"


@app.route("/api/admin/create_user", methods=["GET"])
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


@app.route('/api/admin/dp/create_all')
def dp_create_all():
    db.create_all()
    return 'dp create successfully'


@app.route('/api/admin/dp/drop_all')
def dp_drop_all():
    db.drop_all()
    return 'dp delete successfully'
