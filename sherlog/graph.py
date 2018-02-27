import datetime
from itertools import groupby

import pygal

from sherlog.log_parser import get_config, get_session
from sherlog.model import Log


def gen_graph(data, date_range, title):
    line_chart = pygal.Line()
    line_chart.title = title
    line_chart.x_labels = map(str, date_range)
    line_chart.add('', data)
    line_chart.range = [0, 100]
    return line_chart.render_response()


def compute_status_percent(data, occurences):
    status_info = [x.status for x in data].count('info')
    return '%.2f' % (status_info * 100 / occurences)


def build_list_ping(data):
    return [x for x in data if x.command]


def build_list_service(data):
    return [x for x in data if not x.command]


def get_data(server_name, ping_service, start):
    dbsession = get_session(get_config())
    if 'ping6' in ping_service:
        data = (
            dbsession.query(Log)
            .filter(Log.server_name == server_name)
            .filter(Log.command.contains('ping6'))
            .filter(Log.start > start)
            .all()
        )
    elif 'ping' in ping_service:
        data = (
            dbsession.query(Log)
            .filter(Log.server_name == server_name)
            .filter(Log.command.contains('ping '))
            .filter(Log.start > start)
            .all()
        )
    else:
        data = (
            dbsession.query(Log)
            .filter(Log.host == ping_service)
            .filter(Log.command == None) # noqa
            .filter(Log.start > start)
            .all()
        )
    return data


def build_graph(server_name, ping_service, interval, begin, group):
    data = get_data(server_name, ping_service, begin)
    if 'ping' in ping_service:
        build_data = build_list_ping(data)
    else:
        build_data = build_list_service(data)
    build_data.sort(key=group)
    grouped_by_days = groupby(build_data, group)
    data = []
    data_range = []
    for key, group in grouped_by_days:
        group = list(group)
        data.append(float(compute_status_percent(group, len(group))))
        data_range.append(key)
    title = server_name + ' ' + ping_service if server_name else ping_service
    return gen_graph(data, data_range, title)


def main(ping_service, server_name, interval):
    if not interval:
        begin = datetime.datetime.today().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)
        return build_graph(server_name, ping_service, interval,
                           begin, lambda data: data.start.day)
    elif interval == 'day':
        begin = datetime.datetime.today().replace(
            hour=0, minute=0, second=0, microsecond=0)
        return build_graph(server_name, ping_service, interval,
                           begin, lambda data: data.start.hour)
