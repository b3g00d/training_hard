import unittest
import io
from flask import Flask, request


class FlaskrTestCase(unittest.TestCase):

    def allowed_file(self, filename):
        ALLOW_EXTENSIONS = set(['jpg'])
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOW_EXTENSIONS

    def setUp(self):
        self.app = Flask(__name__)
        self.app.debug = True

        @self.app.route('/', methods=['GET', 'POST'])
        def upload():
            if request.method == 'POST':
                if 'file' not in request.files:
                    return 'Not selected file'

                file = request.files['file']
                if file.filename == '':
                    return 'File not found'
                if file and self.allowed_file(file.filename):
                    return 'OK'

    def test_Upload(self):
        client = self.app.test_client()
        resp1 = client.post('/')
        resp2 = client.post('/',
                            data=dict(
                                file=(None, '')
                            ))
        resp3 = client.post(
            '/',
            data=dict(
                file=(io.BytesIO(b'test'),
                      'test.jpg'),
            ),
            content_type="multipart/form-data",)

        assert 'Not selected file' in str(resp1.data)
        assert 'File not found' in str(resp2.data)
        assert 'OK' in str(resp3.data)

if __name__ == '__main__':
    unittest.main()
