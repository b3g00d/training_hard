import os
from flask import Flask, request, redirect, url_for, flash
from thumbing_worker import thumb_picture
from werkzeug import secure_filename

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOW_EXTENSIONS = set(['jpg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '********'


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOW_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('File not found')
            return request(request.urli)

        file = request.files['file']
        if file.filename == '':
            flash('File empty')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file)
            in_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
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
