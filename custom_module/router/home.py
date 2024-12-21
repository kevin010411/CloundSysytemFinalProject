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

    from custom_module import User, Post
    profile = User.query.filter_by(id=id).first()
    if not profile:
        return f"User_{id} Not Found"
    else:
        posts = sorted(
            profile.posts, key=lambda post: post.created_at, reverse=True)
    return render_template('profile.html', profile=profile, social_posts=posts)


@app.route("/add_post", methods=["POST"])
def add_post():
    from custom_module import User, Post
    from flask import url_for

    if "user_name" not in session:
        return redirect(url_for("index"))  # 未登入的用戶無法發布

    post_title = request.form.get("post_title")
    post_content = request.form.get("post_content")
    user_name = session["user_name"]
    next_url = request.referrer.split(request.host_url)[-1]
    if post_title and post_content:
        # 獲取當前用戶
        user = User.query.filter_by(name=user_name).first()
        if user:
            new_post = Post(
                user_id=user.id,
                title=post_title,
                content=post_content
            )
            db.session.add(new_post)
            db.session.commit()
    return redirect(next_url)


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
    return render_template('video.html', video_data=video_data)


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
