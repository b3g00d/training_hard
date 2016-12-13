#!/usr/bin/env python3
import json
import unittest
import shutil
import tempfile
import io

try:
    from ..upload_service import app
    from ..my_db import db, User, Album
except:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from upload_service import app
    import thumbing_worker
    from my_db import db, User, Album


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        thumbing_worker.app.conf.update(CELERY_ALWAYS_EAGER=True)
        self.test_dir = tempfile.mkdtemp()
        self.app = app
        self.app.config['TESTING'] = True
        # self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' + \
        #     os.path.dirname(os.path.abspath(__file__)) + '/db/test.db'

        self.db = db
        self.db.create_all()
        self.final_path = path.join(self.test_dir, 'pic.jpg')
        with open(self.final_path, 'w') as f:
            f.write('test')

        self.User = User
        self.user = self.User(
            username='test',
            email='test@gmail.com'
        )
        self.Album = Album
        self.pic = self.Album(
            path=self.final_path,
            user=self.user
        )
        self.db.session.add(self.user)
        self.db.session.add(self.pic)
        self.db.session.commit()
        self.app.debug = True

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        self.db.session.remove()
        self.db.drop_all()

    def test_Upload(self):
        client = self.app.test_client()
        resp1 = client.post('/')
        resp2 = client.post(
            '/',
            data=dict(
                file=(None, ''),
                id='test'
            ),
            content_type="multipart/form-data"
        )

        resp3 = client.post(
            '/',
            data=dict(
                file=(io.BytesIO(b'test data'), 'test.jpg'),
                id='test'
            ),
            content_type="multipart/form-data"
        )
        assert '400' in str(resp1.status)
        assert '404' in str(resp2.status)
        assert '302' in str(resp3.status)

    def test_create_user(self):
        assert self.User.query.count() == 1
        self.db.session.add(self.User('test2', 'abc@gmail.com'))
        self.db.session.commit()
        assert self.User.query.count() == 2

    def test_get_user(self):
        user = self.User.query.first()
        assert user.username == 'test'
        assert user.email == 'test@gmail.com'

    def test_delete_user(self):
        user = self.User.query.first()
        assert self.User.query.count() == 1
        self.db.session.delete(user)
        self.db.session.commit()
        assert self.User.query.count() == 0

    def test_add_pic(self):
        assert self.Album.query.count() == 1
        self.db.session.add(self.Album('test/path', self.user))
        self.db.session.commit()
        assert self.Album.query.count() == 2

    def test_get_pic(self):
        assert self.Album.query.count() == 1
        pic = self.Album.query.first()
        assert pic.path == self.final_path

    def test_delete_pic(self):
        assert self.Album.query.count() == 1
        self.db.session.delete(self.Album.query.first())
        self.db.session.commit()
        assert self.Album.query.count() == 0

    def test_api(self):
        client = self.app.test_client()
        api_images = client.get('/images')
        assert '200' in api_images.status
        api_rename = client.put('/images/rename',
                                content_type='application/json',
                                data=json.dumps({
                                    'name': 'pic',
                                    'rename': 'repic',
                                    'user': 'test'
                                }))
        assert '200' in api_rename.status
        api_select = client.get('/images/select',
                                data=json.dumps({
                                    'name': 'repic',
                                    'user': 'test'
                                }))
        assert '200' in api_select.status

        api_detele = client.put('/images/delete',
                                content_type='application/json',
                                data=json.dumps({
                                    'name': 'repic',
                                    'user': 'test'
                                }))
        assert '200' in api_detele.status

if __name__ == '__main__':
    unittest.main()
