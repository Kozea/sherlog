import configparser
# datetime is needed because log contains datetime object
import datetime  # noqa
import os
from threading import Thread

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func

from sherlog.model import Log
from sherlog.tail import LogTail


def get_config():
    config_path = os.path.dirname(os.path.abspath(__file__))
    path = os.getenv(
        'PARSER_CFG', os.path.join(config_path, 'application.ini'))
    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_session(config):
    engine = create_engine(config['DEFAULT'].get('DB'))
    Session = sessionmaker(bind=engine)
    return Session()


def convert_to_dict(data):
    return eval(data.rstrip()[1:-1].replace('\n', ''))


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
        'stderr': (response.get('stderr').decode('utf-8')
                   if response.get('stderr', None) else None),
        'stdout': (response.get('stdout').decode('utf-8')
                   if response.get('stdout', None) else None),
        'command': (' '.join(response.get('command', None))
                    if response.get('command', None) else None),
        'server_name': server_name
    }


def get_max_stop(dbsession):
    date = dbsession.query(func.max(Log.stop)).first()[0]
    if date is None:
        return datetime.datetime.min
    else:
        return date


def insert_log(line, dbsession, max_stop=None):
    if 'Archive' not in line:
        title = line.split('(')[0]
        server_name = get_name(title)
        desc = convert_to_dict(line.split(title)[1])
        if max_stop and desc['end'] > max_stop:
            log = Log(**build_log(server_name, desc))
            dbsession.add(log)

def insert_missing_lines():
    config = get_config()
    dbsession = get_session(config)
    logfile = config['DEFAULT'].get('LOGFILE')
    max_stop = get_max_stop(dbsession)
    count = 0
    with open(logfile, 'r') as fd:
        for line in fd:
            count += 1
            insert_log(line, dbsession, max_stop)
            if count == 100000:
                dbsession.commit()
                count = 0
    dbsession.commit()


def insert_new_lines():
    config = get_config()
    dbsession = get_session(config)
    fd = LogTail(config['DEFAULT'].get('LOGFILE'))
    for line in fd.tail():
        insert_log(line, dbsession)
        dbsession.commit()

if __name__ == '__main__':
    Thread(target = insert_missing_lines).start()
    Thread(target = insert_new_lines).start()
