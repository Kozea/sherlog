import locale
import os

from urllib.parse import urlparse

from .app import app


def drop_db():
    filename = urlparse(app.config['DB']).path
    if os.path.isfile(filename):
        os.remove(filename)


app.cli.command()(drop_db)
