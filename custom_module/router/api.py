import json
from custom_module import app
from flask import flash, jsonify, request, redirect
from werkzeug.utils import secure_filename
from flask import render_template
import os


@app.route('/api', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    else:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_video filename: ' + filename)
        flash('Video successfully uploaded and displayed below')
        return render_template('upload.html', filename=filename)


@app.route('/api/register_user', methods=["POST"])
def register_user():
    from custom_module import User, db
    data = json.loads(request.data)
    new_user = User(name=data['user_name'], password=data['password'])
    session = db.session
    session.add(new_user)
    session.commit()
    return {"status": "Good"}


@app.route('/api/comments/<video_id>', methods=["GET"])
def get_commend(video_id):
    from custom_module import Comment
    try:
        # 查詢對應影片的所有留言
        comments = Comment.query.filter_by(video_id=video_id).all()

        # 建立巢狀結構
        comment_dict = {c.id: {"id": c.id, "content": c.content, "user_name": c.user_name,
                               "created_at": c.created_at, "replies": []} for c in comments}

        # 配置巢狀關係
        nested_comments = []
        for comment in comments:
            if comment.parent_id:
                comment_dict[comment.parent_id]["replies"].append(
                    comment_dict[comment.id])
            else:
                nested_comments.append(comment_dict[comment.id])

        return jsonify(nested_comments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/comments/<video_id>', methods=['POST'])
def add_comment(video_id):
    from custom_module import Comment, db
    data = request.json
    parent_id = data.get('parent_id')  # 父留言 ID，為 NULL 表示主留言
    content = data['content']
    user_name = data['user_name']
    try:
        # 新增留言到資料庫
        new_comment = Comment(
            video_id=video_id,
            parent_id=parent_id,
            content=content,
            user_name=user_name
        )
        db.session.add(new_comment)
        db.session.commit()

        return jsonify({"message": "Comment added successfully", "id": new_comment.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
