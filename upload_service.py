import os
from flask import Flask, request, redirect, url_for, flash, send_from_directory
from werkzeug import secure_filename
from PIL import Image

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOW_EXTENSIONS = set(['jpg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
SIZE_16_16 = (16, 16)
SIZE_32_32 = (32, 32)
SIZE_64_64 = (64, 64)
SIZES = [SIZE_16_16, SIZE_32_32, SIZE_64_64]
NAME_16_16 = '.thumbnail16'
NAME_32_32 = '.thumbnail32'
NAME_64_64 = '.thumbnail64'
NAMES = [NAME_16_16, NAME_32_32, NAME_64_64]


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOW_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return request(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            in_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(in_file)
            in_file_name = os.path.splitext(in_file)[0]
            out_files = [in_file_name + name for name in NAMES]
            for index in range(len(SIZES)):
                im = Image.open(in_file)
                im.thumbnail(SIZES[index])
                im.save(out_files[index], "JPEG")
            return redirect(url_for('upload_file', filename=filename))

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
