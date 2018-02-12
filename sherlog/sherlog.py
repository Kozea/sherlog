import datetime

from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unrest import UnRest

from .model import Log


class Sherlog(Flask):
    def create_session(self):
        return sessionmaker(bind=create_engine(self.config['DB']))()

    def before(self):
        g.session = self.create_session()

    def initialize(self):
        self.before_request(self.before)

        rest = UnRest(self, self.create_session())

        rest(Log, methods=['GET'])


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


def insert_log(line):
    if 'Archive' not in line:
        title = line.split('(')[0]
        server_name = get_name(title)
        desc = convert_to_dict(line.split(title)[1])
        g.session.add(Log(build_log(server_name, desc)))
