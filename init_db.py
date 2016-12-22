#!/usr/bin/env python2
from my_db import db, User, Token

if __name__ == '__main__':
    db.create_all()
    user = User('admin', 'admin@gmail.com', 'adminpass')
    db.session.add(user)
    db.session.add(Token(user))
    db.session.commit()
