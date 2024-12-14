import json
from custom_module import app
from flask import flash, request, redirect
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
