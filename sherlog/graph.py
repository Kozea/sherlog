import datetime

import pygal

from itertools import groupby
from operator import attrgetter
from sherlog.log_parser import get_config, get_session
from sherlog.model import Log


def gen_graph(data, date_range, title):
    line_chart = pygal.Line()
    line_chart.title = title
    line_chart.x_labels = map(str, date_range)
    line_chart.add('', data)
    return line_chart.render_response()


def compute_ok_percent(data, occurences):
    ok_true = [x.ok for x in data].count(True)
    return ok_true * 100 / occurences


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
            .filter(Log.command.contains('ping'))
            .filter(Log.start > start)
            .all()
        )
    else:
        data = (
            dbsession.query(Log)
            .filter(Log.server_name == server_name)
            .filter(Log.command == '')
            .filter(Log.start > start)
            .all()
        )
    return data


def build_graph(server_name, interval, ping_service):
    current_date = datetime.datetime.now()
    tmp_date = datetime.datetime(2018, 1, 5, 14, 13, 37, 903083)
    data = get_data(server_name, ping_service, tmp_date)
    if 'ping' in ping_service:
        build_data = build_list_ping(data)
    else:
        build_data = build_list_service(data)
    build_data.sort(key=lambda data: data.start.day)
    grouped_by_days = groupby(build_data, lambda data:data.start.day)
    for key,group in grouped_by_days:
        group = list(group)
        res = compute_ok_percent(group, len(group))
        print(res)
