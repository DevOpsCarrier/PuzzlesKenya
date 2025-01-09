import sqlite3 as lite
import click
from flask import current_app, g


def get_db():
    """
    :Get the database connection
    :return: db connection for user instance
    """
    if 'db' not in g:
        g.db = lite.connect(
            current_app.config['DATABASE'],
            detect_types=lite.PARSE_DECLTYPES
        )
        g.db.row_factory = lite.Row

    return g.db


def close_db(e=None):
    """
    :close the db connection
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    : Initialise the database with values
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')  # create a command to init db
def init_db_command():
    """
        : clears existing data and creates new tables
        """
    init_db()
    click.echo('Database Initialised')


def init_app(app):
    """
    : Registers the functions for use in the app
    """
    app.teardown_appcontext(close_db)  # does cleanup
    app.cli.add_command(init_db_command)  # adds the new command
