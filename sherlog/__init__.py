import os

from flask import Flask
from urllib.parse import urlparse

from sqlalchemy import create_engine


app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG')

engine = create_engine(app.config['DB'])

@app.cli.command()
def drop_db():
    filename = urlparse(app.config['DB']).path
    if os.path.isfile(filename):
        os.remove(filename)


from .sherlog import *
