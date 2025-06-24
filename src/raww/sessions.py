import time, datetime

import click
from tabulate import tabulate

from .data import rewrite_data, get_tags, get_active_session, get_sessions, read_data
from .views import format_work_time_info


def sort_sessions_by_date_range(sessions: list, dr: str):

    if '..' in dr:
        dates = dr.split('..')
        start_date = datetime.date.fromisoformat(dates[0])
        end_date = datetime.date.today() if dates[1] == '' else datetime.date.fromisoformat(dates[1])
    elif dr == 'today':
        start_date = datetime.date.today()
        end_date = datetime.date.today()
    elif dr == 'all':
        return sessions

    dates_range = f'{start_date} - {end_date}'
    new_sessions: list[dict] = []

    for s in sessions:
        s_start = datetime.date.fromisoformat(s.get('start').get('date'))
        if (s_start >= start_date) and (s_start <= end_date):
            new_sessions.append(s)

    return new_sessions

def create_matrix(sessions: list):

    data = [
        ['tags', 'start', 'end', 'breaks', 'total time']
    ]

    for s in sessions:
        total_time = s.get('total time')
        hours = total_time.get('hours')
        minutes = total_time.get('minutes')
        seconds = total_time.get('seconds')
        work_time_info = format_work_time_info(hours, minutes, seconds)

        data.append([
                ''.join(f'{tag}, '[:-2] for tag in s.get('tags')),
                s.get('start').get('date') + ' ' + s.get('start').get('time')[:-7],
                s.get('end').get('date') + ' ' + s.get('end').get('time')[:-7],
                s.get('breaks'),
                work_time_info
        ])
    
    return data


@click.command('sessions')
@click.option('--dr', default='all')
def check_sessions(dr: str):

    all_sessions = get_sessions()

    if all_sessions == []:
        click.echo('🦇 there are no sessions yet')
        exit(1)

    sessions = sort_sessions_by_date_range(all_sessions, dr)

    if sessions == []:
        click.echo(f'🦇 no sessions on this range: {dr}')
        exit(1)

    data = create_matrix(sessions)
    click.echo(tabulate(data, headers='firstrow', tablefmt='grid'))


@click.command('begin')
@click.argument('tags', nargs=-1)
def begin_session(tags: tuple):

    active_session = get_active_session()

    if active_session:
        click.echo('🦇 there is already an active session')
        exit(1)

    if tags == ():
        click.echo('🦇 at least one tag is required to begin a new session')
        exit(1)
    
    mytags = get_tags()
    sessions = get_sessions()

    for tag in tags:
        if tag not in mytags:
            click.echo(f'🦇 tag {tag} does not exist yet')
            exit(1)

    start = datetime.datetime.now()

    new_data = {
        'tags': [*mytags],
        'active_session': {
            'tags': [*tags],
            'start': f'{start}',
            'breaks': 0
        },
        'sessions': [*sessions]
    }

    rewrite_data(new_data)

    click.echo('🦇 session started')
    click.echo()

    if len(tags) == 1:
        click.echo(f'tag - {tags[0]}')
    else:
        click.echo(f'tags: * {tags[0]}')
        for tag in tags[1:]:
            click.echo(f'      * {tag}')

@click.command('finish')
def finish_session():

    active_session = get_active_session()

    if not active_session:
        click.echo('🦇 there is no active session yet')
        exit(1)

    mytags = get_tags()
    mysessions = get_sessions()

    # start & end info
    start_datetime: datetime = datetime.datetime.fromisoformat(active_session.get('start'))
    start_date = datetime.date(start_datetime.year, start_datetime.month, start_datetime.day)
    start_time = datetime.time(start_datetime.hour, start_datetime.minute, start_datetime.second, start_datetime.microsecond)

    end_datetime = datetime.datetime.now()
    end_date = datetime.date(end_datetime.year, end_datetime.month, end_datetime.day)
    end_time = datetime.time(end_datetime.hour, end_datetime.minute, end_datetime.second, end_datetime.microsecond)
    breaks: int = active_session.get('breaks')
    timedelta = ((end_datetime - start_datetime).seconds) - breaks
    hours = timedelta // 3600
    timedelta -= hours*3600
    minutes = timedelta // 60
    timedelta -= minutes * 60
    seconds = timedelta

    tags = [*(active_session.get('tags'))]

    total_time = {
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    }

    new_session = {
        'tags': [*tags],
        'start': {
            'date': f'{start_date}',
            'time': f'{start_time}'
        },
        'end': {
            'date': f'{end_date}',
            'time': f'{end_time}'
        },
        'breaks': breaks,
        'total time': total_time
    }

    new_data = {
        'tags': [*mytags],
        'active_session': {},
        'sessions': [*mysessions, new_session]
    }

    rewrite_data(new_data=new_data)

    click.echo('the session has ended 🦇')
    click.echo()

    work_time_info = format_work_time_info(hours=hours, minutes=minutes, seconds=seconds)
    
    if len(tags) == 1:
        click.echo(f'you did {tags[0]} for {work_time_info}')
    else:
        click.echo(f'you did: * {tags[0]}')
        for tag in tags[1:]:
            click.echo(f'         * {tag}')
            click.echo(f'for {work_time_info}')

@click.command('pause')
def pause_session():

    active_session = get_active_session()

    if not active_session:
        click.echo('🦇 there is no active session yet')
        exit(1)

    tags: list = active_session.get('tags')
    breaks: int = active_session.get('breaks')
    data = read_data()

    click.echo('🦇 the session is paused')
    
    while True:
        time.sleep(1)
        breaks += 1

        active_session['breaks'] = breaks
        data['active_session'] = active_session
        rewrite_data(data)
