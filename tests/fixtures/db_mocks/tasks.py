from uuid import UUID
from datetime import datetime
from src.enums.task_status import TaskStatus
from tests.fixtures.db_mocks import (GROUPS, SPRINTS, USERS, BOARDS, COLUMNS)


TASKS = (
    {
        'id': UUID('b04e55bd-8431-4edd-8eb4-632099c0ea65'),
        'title': 'Задача №1',
        'description': 'Выполнить разработку',
        'status': TaskStatus.todo,
        'assignee_id': USERS[0]['id'],
        'assignee': USERS[0]['full_name'],
        'created_at': datetime.now(),
        'author_id': USERS[1]['id'],
        'author': USERS[1]['full_name'],
        'observers': [USERS[2]['id']],
        'column_id': COLUMNS[0]['id'],
        'board_id': BOARDS[0]['id'],
        'sprint_id': None,
        'group_id': None,
    },
    {
        'id': UUID('b04e55bd-8431-4edd-8eb4-632099c0ea66'),
        'title': 'Задача №2',
        'description': 'Задача №2',
        'status': TaskStatus.in_progress,
        'assignee_id': USERS[2]['id'],
        'assignee': USERS[2]['full_name'],
        'created_at': datetime.now(),
        'author_id': USERS[1]['id'],
        'author': USERS[1]['full_name'],
        'observers': [],
        'column_id': COLUMNS[1]['id'],
        'board_id': BOARDS[1]['id'],
        'sprint_id': SPRINTS[0]['id'],
        'group_id': GROUPS[0]['id'],
    },
)