from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unrest import UnRest

from sherlog import graph
from sherlog.model import Log


class Sherlog(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config.from_envvar('FLASK_CONFIG')

        self.before_request(self.before)

        self.route('/graph/<server_name>/<ping_service>',
                   methods=['GET', 'POST'])(get_graph)
        self.route('/graph/<ping_service>',
                   methods=['GET', 'POST'])(get_graph)

        rest = UnRest(self, self.create_session())
        rest(Log, methods=['GET'])

    def create_session(self):
        return sessionmaker(bind=create_engine(self.config['DB']))()

    def before(self):
        g.session = self.create_session()


def get_graph(ping_service, server_name=''):
    graph.build_graph(server_name, ping_service)


app = Sherlog(__name__)
