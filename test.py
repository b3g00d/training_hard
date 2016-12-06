#!/usr/bin/env python3
import click


@click.command()
@click.option('--count', default=1)
@click.option('--name', prompt='Your name')
def hello(count, name):
    for x in range(count):
        click.echo('Hi %s!' % name)


if __name__ == '__main__':
    hello()
