import datetime

from sherlog import log_parser


def test_get_name_service(one_line_service):
    title = one_line_service.split('(')[0]
    assert log_parser.get_name(title) == 'Anne-Laure'


def test_get_name_ping(one_line_ping):
    title = one_line_ping.split('(')[0]
    assert log_parser.get_name(title) == 'Anne-Laure'


def test_convert_to_dict_service(one_line_service):
    title = one_line_service.split('(')[0]
    assert (
        log_parser.convert_to_dict(one_line_service.split(title)[1]) ==
        {
            'response': {
                'code': 200,
                'host': 'hello.promomaker.fr',
                'redirect': [],
                'message': 'Status code is 200',
                'url': 'https://51.15.12.125',
                'ok': True,
                'timeout': False
            },
            'start': datetime.datetime(2018, 1, 22, 22, 34, 31, 933048),
            'end': datetime.datetime(2018, 1, 22, 22, 34, 32, 189937),
            'is_hard': False,
            'status': 'info'
        })


def test_convert_to_dict_ping(one_line_ping):
    title = one_line_ping.split('(')[0]
    assert (
        log_parser.convert_to_dict(one_line_ping.split(title)[1]) == {
            'end': datetime.datetime(2018, 2, 9, 11, 20, 48, 976649),
            'status': 'info',
            'response': {
                'return_code': 0,
                'stderr': b'',
                'command': ['ping6', '-c1', '-W3', '2001:bc8:3261:500::1'],
                'message': 'No message',
                'ok': True,
                'stdout': (
                    b'PING 2001:bc8:3261:500::1(2001:bc8:3261:500::1) '
                    b'56 data bytes64 bytes from 2001:bc8:3261:500::1: '
                    b'icmp_seq=1 ttl=58 time=13.0 ms--- 2001:bc8:3261:500::1 '
                    b'ping statistics ---1 packets transmitted, 1 received, '
                    b'0% packet loss, time 0msrtt min/avg/max/mdev = '
                    b'13.072/13.072/13.072/0.000 ms'
                ),
                'timeout': False
            },
            'start': datetime.datetime(2018, 2, 9, 11, 20, 48, 952867),
            'is_hard': True
        })


def test_build_log_service(one_line_service):
    title = one_line_service.split('(')[0]
    server_name = log_parser.get_name(title)
    desc = log_parser.convert_to_dict(one_line_service.split(title)[1])
    assert (
        log_parser.build_log(server_name, desc) == {
            'return_code': 200,
            'message': 'Status code is 200',
            'url': 'https://51.15.12.125',
            'ok': True,
            'host': 'hello.promomaker.fr',
            'start': datetime.datetime(2018, 1, 22, 22, 34, 31, 933048),
            'stop': datetime.datetime(2018, 1, 22, 22, 34, 32, 189937),
            'status': 'info',
            'stderr': None,
            'stdout': None,
            'command': None,
            'server_name': 'Anne-Laure'
        })


def test_build_log_ping(one_line_ping):
    title = one_line_ping.split('(')[0]
    server_name = log_parser.get_name(title)
    desc = log_parser.convert_to_dict(one_line_ping.split(title)[1])
    assert (
        log_parser.build_log(server_name, desc) == {
            'return_code': 0,
            'message': 'No message',
            'url': None,
            'ok': True,
            'host': None,
            'start': datetime.datetime(2018, 2, 9, 11, 20, 48, 952867),
            'stop': datetime.datetime(2018, 2, 9, 11, 20, 48, 976649),
            'status': 'info',
            'stderr': None,
            'stdout': (
                'PING 2001:bc8:3261:500::1(2001:bc8:3261:500::1) '
                '56 data bytes64 bytes from 2001:bc8:3261:500::1: '
                'icmp_seq=1 ttl=58 time=13.0 ms--- 2001:bc8:3261:500::1 '
                'ping statistics ---1 packets transmitted, 1 received, '
                '0% packet loss, time 0msrtt min/avg/max/mdev = '
                '13.072/13.072/13.072/0.000 ms'
            ),
            'command': 'ping6 -c1 -W3 2001:bc8:3261:500::1',
            'server_name': 'Anne-Laure'
        })
