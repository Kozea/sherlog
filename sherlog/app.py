from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unrest import UnRest
from werkzeug.routing import PathConverter

from sherlog import graph
from sherlog.model import Log


class EverythingConverter(PathConverter):
    regex = '.*?'


class Sherlog(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config.from_envvar('FLASK_CONFIG')

        self.before_request(self.before)

        self.url_map.converters['everything'] = EverythingConverter

        self.route('/graph/avg/<server_name>/<ping_service>',
                   methods=['GET', 'POST'])(get_graph_avg)
        self.route('/graph/avg/<everything:ping_service>',
                   methods=['GET', 'POST'])(get_graph_avg)

        self.route('/graph/<server_name>/<ping_service>',
                   methods=['GET', 'POST'])(get_graph)
        self.route('/graph/<everything:ping_service>',
                   methods=['GET', 'POST'])(get_graph)

        self.route('/graph/day/<server_name>/<ping_service>',
                   methods=['GET', 'POST'])(get_graph_day)
        self.route('/graph/day/<everything:ping_service>',
                   methods=['GET', 'POST'])(get_graph_day)

        rest = UnRest(self, self.create_session())
        rest(Log, methods=['GET'])

    def create_session(self):
        return sessionmaker(bind=create_engine(self.config['DB']))()

    def before(self):
        g.session = self.create_session()


def get_graph(ping_service, server_name=None, interval=None):
    return graph.main(ping_service, server_name, interval)


def get_graph_avg(ping_service, server_name=None, interval=None, avg=True):
    return graph.main(ping_service, server_name, interval, avg)


def get_graph_day(ping_service, server_name=None, interval='day'):
    return graph.main(ping_service, server_name, interval)


app = Sherlog(__name__)
