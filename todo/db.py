import datetime
import random
import psycopg2
import click
import os
import urllib.parse as urlparse
from flask import current_app,g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        url = urlparse.urlparse(current_app.config['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        g.db = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    f = current_app.open_resource("sql/initial.sql")
    sql_code = f.read()
    
    cur = db.cursor()
    cur.execute(sql_code)
    db.commit()
    cur.close()
    close_db()
    
    
@click.command('initdb',help="initilaise the database")
@with_appcontext
def init_db_command():
    init_db()
     

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
