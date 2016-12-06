#!/usr/bin/env python3
import argparse


def allowed_file(filename):
    ALLOW_EXTENSIONS = set(['jpg'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOW_EXTENSIONS


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('f', nargs='*')

    arg = argp.parse_args()
    for file in arg.f:
        print(allowed_file(file))

if __name__ == '__main__':
    main()
