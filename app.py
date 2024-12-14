from flask import redirect, url_for, render_template
from flask import render_template
from custom_module import app, db


def create_sql_db():
    # db.drop_all()
    db.create_all()
    # print(db.metadata.tables.keys())


@app.route('/admin/dp/create_all')
def upload_form():
    db.create_all()
    return render_template('dp create successfully')


@app.route('/admin/dp/drop_all')
def upload_form():
    db.drop_all()
    return render_template('dp delete successfully')


@app.route('/upload')
def upload_form():
    return render_template('upload.html')


@app.route('/display/<filename>')
def display_video(filename):
    # print('display_video filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    with app.app_context():
        create_sql_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
