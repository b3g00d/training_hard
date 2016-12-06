#!/usr/bin/env python3
import click
import os


def allowed_file(filename):
    ALLOW_EXTENSIONS = set(['jpg'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOW_EXTENSIONS


@click.command()
@click.option('--req', default='GET', help='Request method')
@click.option('--files', default='')
def upload_file(req, files):
    UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
    if req != 'POST' and req != 'GET':
        click.echo('Error REQ')
        return None
    elif req == 'POST':
        files = files.split()
        if not len(files):
            return click.echo("Syntax Error. No File in command")

        for file in files:
            if file == '':
                click.echo('Name empty')

            if allowed_file(file):
                in_file = os.path.join(UPLOAD_FOLDER, file)
                click.echo('Success {}'.format(in_file))

            else:
                click.echo('File not allow: {}'.format(file))

        return click.echo('Done!!!')
    else:
        return click.echo('''
            GET req
        ''')

if __name__ == '__main__':
    upload_file()
