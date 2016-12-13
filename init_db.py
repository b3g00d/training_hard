#!/usr/bin/env python3
from my_db import db, User, Album

if __name__ == '__main__':
    db.create_all()
    db.session.add(User('admin', 'admin@gmail.com'))
    db.session.commit()
