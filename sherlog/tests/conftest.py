from os.path import dirname, join

import pytest

import sherlog
from alembic import command
from alembic.config import Config


@pytest.yield_fixture(scope='function')
def app():
    app_roadhog = sherlog.Sherlog(__name__)
    app_roadhog.config.from_pyfile('testing_settings.py')
    app_roadhog.initialize()
    return app_roadhog


@pytest.yield_fixture(scope='function')
def db_session(app, alembic_config):
    session = app.create_session()
    yield session


@pytest.yield_fixture(scope='function')
def alembic_config(app):
    ini_location = join(dirname(__file__), '..', '..', 'alembic.ini')
    sqlalchemy_url = app.config['DB']
    config = Config(ini_location)
    config.set_main_option('sqlalchemy.url', sqlalchemy_url)
    command.upgrade(config, 'head')
    yield config
    command.downgrade(config, 'base')


@pytest.fixture(scope='function')
def one_line_service():
    return (
        "Promomaker Hello on Anne-Laure ({'response': {'code': 200, 'host': "
        "'hello.promomaker.fr', 'redirect': [], 'message': "
        "'Status code is 200', 'url': 'https://51.15.12.125', 'ok': True, "
        "'timeout': False}, 'start': datetime.datetime(2018, 1, 22, 22, 34, "
        "31, 933048), 'end': datetime.datetime(2018, 1, 22, 22, 34, 32, "
        "189937), 'is_hard': False, 'status': 'info'})")


@pytest.fixture(scope='function')
def one_line_ping():
    return (
        "Ping IPv6 on Anne-Laure ({'end': datetime.datetime(2018, 2, 9, 11, "
        "20, 48, 976649), 'status': 'info', 'response': {'return_code': 0, "
        "'stderr': b'', 'command': ['ping6', '-c1', '-W3', "
        "'2001:bc8:3261:500::1'], 'message': 'No message', 'ok': True, "
        "'stdout': b'PING 2001:bc8:3261:500::1(2001:bc8:3261:500::1) "
        "56 data bytes\n64 bytes from 2001:bc8:3261:500::1: icmp_seq=1 "
        "ttl=58 time=13.0 ms\n\n--- 2001:bc8:3261:500::1 ping statistics "
        "---\n1 packets transmitted, 1 received, 0% packet loss, time "
        "0ms\nrtt min/avg/max/mdev = 13.072/13.072/13.072/0.000 ms\n', "
        "'timeout': False}, 'start': datetime.datetime(2018, 2, 9, 11, 20, "
        "48, 952867), 'is_hard': True})")
