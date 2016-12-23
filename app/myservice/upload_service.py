# -*- coding: utf-8 -*-
import os
import sys
from hashlib import sha256
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug import secure_filename
from flask_cors import CORS
sys.path.insert(0, os.path.dirname(os.getcwd()))
from worker import celery_worker
from mydb.my_db import User, Album, db, Token

ASSET = '/static/asset/'
UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + ASSET
ALLOW_EXTENSIONS = set(['jpg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get("APP_SECRET_KEY", "")
CORS(app)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOW_EXTENSIONS


def get_user_from_token(value):
    result = -1
    token = Token.query.filter_by(token_value=value).first()
    if token:
        user = User.query.filter_by(id=token.user_id).first()
        if token.token_value == Token.get_token_with_time(user):
            result = user
    if result == -1:
        return None
    return user


@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        identify = request.form.get('token', None)
        if 'file' not in request.files or not identify:
            return "Bad request", 400

        file = request.files['file']
        if file.filename == '':
            return "File empty", 404
        user = get_user_from_token(identify)

        if user and file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], user.username)
            if not os.path.exists(path):
                os.makedirs(path)
            in_file = os.path.join(path, filename)
            file.save(in_file)
            celery_worker.send_task(
                'worker.thumb_picture', args=[
                    in_file, user.username])
            return redirect(url_for('upload_file',
                                    filename=file.filename))

        return "Failed"

    return '''
    <!doctype html>
    <title>Upload file</title>
    <hl>Upload file</hl>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=token name=token>
         <input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


def get_length(file):
    return os.path.getsize(file.path)


def get_name(file):
    names = file.path.rsplit('/', 1)[-1]
    return names, names.rsplit('.', 1)[0]


def rename(file, name):
    exten = file.path.rsplit('.', 1)[1]
    return os.path.join(os.path.dirname(file.path), name + '.' + exten)


@app.route('/images', methods=['GET'])
def api():
    if request.method == 'GET':
        try:
            pictures = Album.query.all()
            if pictures:
                images = dict()
                for pic in pictures:
                    full_name, real_name = get_name(pic)
                    size = get_length(pic)
                    images[full_name] = {
                        'name': real_name,
                        'path': pic.path,
                        'size': size
                    }
            else:
                images = {}
            return jsonify(result=images)
        except:
            return jsonify(result={})


@app.route('/images/rename', methods=['PUT'])
def rename_pic():
    if request.method == 'PUT':
        data = request.get_json()
        name = data.get('name', '')
        re_name = data.get('rename', '')
        token = data.get('token', '')
        if not name or not token or not re_name:
            return 'wrong name or user'

        user = get_user_from_token(token)
        if not user:
            return 'No user in table'

        pics = Album.filter(name, user).all()
        if not pics:
            return 'Pics with that name'

        for pic in pics:
            path = rename(pic, re_name)
            try:
                os.rename(pic.path, path)

            except:
                return 'File in folder not found'
            pic.path = path
        try:
            db.session.commit()
            return 'Done!!!'
        except:
            db.session.rollback()
            return 'Error db locked'


@app.route('/images/delete', methods=['PUT'])
def detele_pic():
    if request.method == 'PUT':
        data = request.get_json()
        name = data.get('name', '')
        token = data.get('token', '')
        if not name or not token:
            return 'wrong name or user'

        user = get_user_from_token(token)
        if not user:
            return 'No user in table'

        pics = Album.filter(name, user).all()
        if not pics:
            return 'No pics with that name'

        for pic in pics:
            db.session.delete(pic)
            try:
                os.remove(pic.path)
            except:
                return 'File in folder not found'
        try:
            db.session.commit()
            return 'Done!!!'
        except:
            db.session.rollback()
            return 'Error db locked'


@app.route('/images/select', methods=['GET'])
def select_pic():
    if request.method == 'GET':
        name = request.args.get('name', '')
        token = request.args.get('token', '')
        if not name or not token:
            return ' wrong name or user'

        user = get_user_from_token(token)
        if not user:
            return 'No user in table'

        pic = Album.filter(name, user).first()
        if not pic:
            return 'No pick with that name'
        full_name, real_name = get_name(pic)
        size = get_length(pic)
        return jsonify(result={
            full_name: {
                'name': real_name,
                'path': pic.path,
                'size': size
            }
        })


@app.route('/login', methods=['POST'])
def login():
    result = 0
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        if not username or not password:
            result = -1
        else:
            user = User.filter(username, password)
            if not user:
                result = -1
            elif user.password == sha256(password).hexdigest():
                result = Token.get_token(user)
            else:
                result = -1
        if result == -1:
            result = "Result not found"
        return jsonify(token=result)


@app.route('/reg', methods=['POST'])
def reg():
    result = 0
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        repass = data.get('repassword', '')
        email = data.get('email', '')
        if not username or not email or not password or not (
                password == repass):
            result = -1
        else:
            user = User.query.filter_by(username=username, email=email).first()
            if not user:
                user = User(username, email, password)
                db.session.add(user)
                try:
                    db.session.commit()
                    token = Token(user)
                    db.session.add(token)
                    db.session.commit()
                    result = token.token_value
                except:
                    db.session.rollback()
                    result = -1
            else:
                result = -1
        if result == -1:
            return "Failed"
        return jsonify(token=result)


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
