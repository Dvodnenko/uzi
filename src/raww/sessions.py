import time, datetime

import click
from tabulate import tabulate

from .data import Data, Session


def sort_sessions_by_date_range(sessions: list[Session], dr: str):

    if '..' in dr:
        dates = dr.split('..')
        start_date = datetime.date.fromisoformat(dates[0])
        end_date = datetime.date.today() if dates[1] == '' else datetime.date.fromisoformat(dates[1])
    elif dr == 'today':
        start_date = datetime.date.today()
        end_date = datetime.date.today()
    elif dr == 'all':
        return sessions
    
    new_sessions: list[Session] = []

    for s in sessions:
        s_start = s.start.date
        if (s_start >= start_date) and (s_start <= end_date):
            new_sessions.append(s)

    return new_sessions

def create_matrix(sessions: list[Session]):

    data = [
        ['tags', 'start', 'end', 'breaks', 'total time']
    ]

    for s in sessions:
        data.append([
                ''.join(f'{tag}, ' for tag in s.tags)[:-2],
                str(s.start.date) + ' ' + str(s.start.time),
                str(s.end.date) + ' ' + str(s.end.time),
                s.breaks,
                s.total.infostr
        ])
    
    return data


@click.command('sessions')
@click.option('--dr')
@click.option('--lxd', type=int) # lxd - think of it like "last X days". for instance: "--lxd 10" means "last 10 days"
@click.pass_context
def check_sessions(ctx: click.Context, dr: str, lxd: int):

    if dr is None and lxd is None:
        click.echo('🦇 you should provide --dr or --lxd option')
        exit(1)

    if dr != None and lxd != None:
        click.echo('🦇 you cannot provide both --dr and --lxd options')
        exit(1)

    if lxd != None:
        if lxd <= 0:
            click.echo(f'🦇 you cannot see info about "last {lxd} days". lxd should be grater than 0')
            exit(1)
        else:
            dr = f'{datetime.date.today() - datetime.timedelta(days=(lxd-1))}..{datetime.date.today()}'

    raww_directory = ctx.obj['raww_directory']
    data = Data(raww_directory)
    all_sessions = data.sessions

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
@click.option('--msg', '-m', default='')
@click.option('--tags', '-t', type=str, help='comma-separated tags', default='')
@click.pass_context
def begin_session(ctx: click.Context, tags: str, msg: str):
    if tags == '':
        tags = []
    else:
        tags = tags.split(',')

    raww_directory = ctx.obj['raww_directory']
    data = Data(raww_directory)

    if data.active_session:
        click.echo('🦇 there is already an active session')
        exit(1)
    
    mytags = data.tags

    for tag in tags:
        if tag not in mytags:
            click.echo(f'🦇 tag {tag} does not exist yet')
            exit(1)

    active_session = data.begin_session(tags, msg)

    click.echo('🦇 session started')
    click.echo()
    click.echo(active_session.msg if active_session.msg != '' else 'no message provided')
    click.echo()

    if tags == []:
        click.echo('no tags provided')
    elif len(tags) == 1:
        click.echo(f'tag - {tags[0]}')
    else:
        click.echo(f'tags: * {tags[0]}')
        for tag in tags[1:]:
            click.echo(f'      * {tag}')

@click.command('finish')
@click.pass_context
def finish_session(ctx: click.Context):

    raww_directory = ctx.obj['raww_directory']
    data = Data(raww_directory)
    active_session = data.active_session

    if not active_session:
        click.echo('🦇 there is no active session yet')
        exit(1)

    session = data.finish_session()

    click.echo('the session has ended 🦇')
    click.echo()
    if session.msg == '':
        click.echo('there was no message in the session')
    else:
        click.echo(session.msg)
        click.echo()

    tags = session.tags
    work_time_info = session.total.infostr
    
    if tags == []:
        click.echo('there were no tags in the session')
    elif len(tags) == 1:
        click.echo(f'tags: {tags[0]}')
    else:
        click.echo(f'tags: * {tags[0]}')
        for tag in tags[1:]:
            click.echo(f'      * {tag}')
    click.echo(f'you worked for {work_time_info}')

@click.command('pause')
@click.pass_context
def pause_session(ctx: click.Context):

    raww_directory = ctx.obj['raww_directory']
    data = Data(raww_directory)
    active_session = data.active_session

    if not active_session:
        click.echo('🦇 there is no active session yet')
        exit(1)

    click.echo('🦇 the session is paused')
    while True:
        time.sleep(1)

        active_session.breaks = active_session.breaks + 1
        data.active_session = active_session
