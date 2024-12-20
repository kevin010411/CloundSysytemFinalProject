from custom_module import app
from sqlalchemy import select
from flask import jsonify, render_template, request, redirect, session

from custom_module import db


@app.route('/')
def home():
    user_name = session.get('user_name', None)
    user_id = session.get('user_id', None)

    from custom_module import Video
    video_data = db.session.query(Video).all()
    return render_template('index.html', video_data=video_data, user_id=user_id, user_name=user_name)


@app.route("/register")
def index():
    is_admin = session.get('is_admin', False)
    return render_template("register.html", is_admin=is_admin)


@app.route("/profile/<id>")
def profle(id):
    if not session.get('user_id', False):
        return f"User_{id} Not Found"
    else:
        from custom_module import User, Video
        profile_list = User.query.filter_by(id=id).first()
        video_list = Video.query.filter_by(author=id).all()
        return render_template('profile.html', profile_list=profile_list, video_list=video_list)


@app.route("/user_list")
def user_list():
    from custom_module import User
    user_data = User.query.all()
    return render_template("user_list.html", user_list=user_data)


@app.route("/video_list")
def video_list():
    from custom_module import Video
    video_data = Video.query.all()
    return render_template("video_list.html", video_list=video_data)


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    from custom_module import User
    username = request.form['username']
    password = request.form['password']
    db_session = db.session
    user_data = db_session.query(User).filter_by(name=username).first()
    if user_data:
        if username == user_data.name and password == user_data.password:
            session['user_name'] = username
            session['user_id'] = user_data.id
            return redirect('/')

    return render_template('login.html', error='Invalid username or password')


@app.route('/logout', methods=['POST'])
def user_logout():
    session.pop('user_name', "Error User")
    session.pop('user_id', "Error Id")
    return redirect("/")


@app.route('/video/<video_id>', methods=['GET'])
def video_get(video_id):
    from custom_module import Video, User
    video_data = db.session.query(Video).filter_by(id=video_id).first()
    video_owner = db.session.query(User).filter_by(
        id=video_data.author).first()
    return render_template('video.html', video_data=video_data, video_owner=video_owner)


@app.route('/update/<int:video_id>', methods=['POST'])
def update_video(video_id):
    from custom_module import Video
    video = Video.query.get(video_id)
    if not video:
        return jsonify({'error': 'Video not found'}), 404

    action = request.json.get('action')
    if action == 'like':
        video.good_num += 1
    elif action == 'dislike':
        video.bad_num += 1
    elif action == 'coin':
        video.coin_num += 1
    elif action == 'share':
        video.share_num += 1
    else:
        return jsonify({'error': 'Invalid action'}), 400

    db.session.commit()
    return jsonify({
        'good_num': video.good_num,
        'bad_num': video.bad_num,
        'coin_num': video.coin_num,
        'share_num': video.share_num
    })
