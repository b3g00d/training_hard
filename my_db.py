# import os
from functools import reduce
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'  # + \
# os.path.dirname(os.path.abspath(__file__)) + '/db/test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


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

    def filter(name, user):
        command = [Album.path.contains(name), Album.user_id == user.id]
        return Album.query.filter(reduce(lambda x, y: (x) & (y), command))


if __name__ == '__main__':
    db.create_all()
    manager.run()
