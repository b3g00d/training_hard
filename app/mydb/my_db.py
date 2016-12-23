# -*- coding: utf-8 -*-
import os
import time
from hashlib import sha256
from functools import reduce
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
USER_ID = os.environ.get('USER_ID', 'user')
USER_PASS = os.environ.get('USER_PASS', 'default')
MYSQL_URL = os.environ.get('MYSQL_URL')
SQLALCHEMY_DATABASE_URL = ''.join(["mysql://",
                                   USER_ID,
                                   ":",
                                   USER_PASS,
                                   "@",
                                   MYSQL_URL,
                                   "/mydb"])
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(64), unique=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = sha256(password).hexdigest()

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def filter(username, password):
        return User.query.filter_by(
            username=username, password=sha256(password).hexdigest()).first()


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User', backref=db.backref(
            'picture', lazy='dynamic'))

    def __init__(self, path, user):
        self.path = path
        self.user = user

    def __repr__(self):
        return '<Picture %r>' % self.path

    @staticmethod
    def filter(name, user):
        command = [Album.path.contains(name), Album.user_id == user.id]
        return Album.query.filter(reduce(lambda x, y: (x) & (y), command))


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref(
        'token_id', lazy='dynamic'))
    time_create = db.Column(db.Integer, unique=False)
    token_value = db.Column(db.String(64), unique=True)

    def __init__(self, user):
        self.user = user
        self.time_create = int(time.time())
        self.token_value = sha256('{username}{timestamp}'.format(
            username=self.user.username,
            timestamp=self.time_create
        )).hexdigest()

    @staticmethod
    def get_token_with_time(user):
        result = 0
        token = Token.query.filter_by(user_id=user.id).first()
        current_time = int(time.time())
        TIME_TO_LIVE = 10 * 60  # 10 phut
        if not (current_time - token.time_create) > TIME_TO_LIVE:
            result = token.token_value
        else:
            try:
                token.token_value = sha256('{username}{timestamp}'.format(
                    username=user.username,
                    timestamp=current_time
                )).hexdigest()

                db.session.commit()
                result = token.token_value
            except:
                db.session.rollback()
        return result

    @staticmethod
    def get_token(user):
        result = 0
        current_time = int(time.time())
        token = Token.query.filter_by(user_id=user.id).first()
        try:
            token.token_value = sha256('{username}{timestamp}'.format(
                username=user.username,
                timestamp=current_time
            )).hexdigest()

            db.session.commit()
            result = token.token_value
        except:
            db.session.rollback()
            result = -1
        if result == -1:
            result = "Failed"
        return result


if __name__ == '__main__':
    manager.run()
