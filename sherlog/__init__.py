import locale
import os

from flask import Flask
from urllib.parse import urlparse

from .sherlog import *


locale.setlocale(locale.LC_ALL, 'fr_FR')

app = Sherlog(__name__)
app.config.from_envvar('FLASK_CONFIG')

app.initialize()

# engine = create_engine(app.config['DB'])

@app.cli.command()
def drop_db():
    filename = urlparse(app.config['DB']).path
    if os.path.isfile(filename):
        os.remove(filename)
