import os
from flask import Flask, request, redirect, url_for, flash, send_from_directory
from worker_test import thumb_picture
from werkzeug import secure_filename
UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOW_EXTENSIONS = set(['jpg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOW_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print(request)
    if request.method == 'POST':
        if 'file' not in request.files:
            return request(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # import ipdb;ipdb.set_trace()
            in_file = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(in_file)
            thumb_picture.delay(in_file)
            return redirect(url_for('upload_file',
                                    filename=file.filename))

    return '''
    <!doctype html>
    <title>Upload file</title>
    <hl>Upload file</hl>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
if __name__ == '__main__':
    app.run()
