import configparser
import datetime
import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sherlog.model import Log


def get_config():
    config_path = os.path.dirname(os.path.abspath(__file__))
    path = os.getenv('PARSER_CFG', os.path.join(config_path, 'application.ini'))
    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_session(config):
    engine = create_engine(config['DEFAULT'].get('DB'))
    Session = sessionmaker(bind=engine)
    return Session()


def convert_to_dict(data):
    return eval(data[1:-1].replace('\n', ''))


def get_name(data):
    return data.split(' ')[-2]


def build_log(server_name, desc):
    response = desc.get('response')
    code_keys = ('code', 'return_code')
    return {
        'return_code': (response.get('code', response.get('return_code'))
                        if any(key in response.keys() for key in code_keys)
                        else None),
        'message': response.get('message'),
        'url': response.get('url', None),
        'ok': response.get('ok'),
        'host': response.get('host', None),
        'start': desc.get('start'),
        'stop': desc.get('end'),
        'status': desc.get('status'),
        'stderr': response.get('stderr', None),
        'stdout': response.get('stdout', None),
        'command': response.get('command', None),
        'server_name': server_name
    }


def insert_log(line, dbsession):
    if 'Archive' not in line:
        title = line.split('(')[0]
        server_name = get_name(title)
        desc = convert_to_dict(line.split(title)[1])
        dbsession.add(Log(build_log(server_name, desc)))


def read_log(logfile):
    logfile.seek(0, 2)
    while True:
        line = logfile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield(line)


if __name__ == '__main__':
    config = get_config()
    dbsession = get_session(config)
    logfile = open(config['DEFAULT'].get('LOGFILE'), 'r')
    loglines = read_log(logfile)
    for line in loglines:
        insert_log(line, dbsession)
