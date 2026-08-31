from uuid import UUID
from datetime import datetime

USERS = (
    {
        'id': UUID('f447b29d-8e56-4b07-9f53-8add7e10e9cd'),
        'full_name': 'Имя Исполнителя 1',
        'email': 'executor1@example.com',
        'created_at': datetime.now(),
    },
    {
        'id': UUID('d66e86ca-a56f-41af-a2c6-b946fb9def2a'),
        'full_name': 'Имя Автора 1',
        'email': 'author1@example.com',
        'created_at': datetime.now(),
    },
    {
        'id': UUID('f447b29d-8e56-4b07-9f53-8add7e10e9cf'),
        'full_name': 'Имя Исполнителя 2',
        'email': 'executor2@example.com',
        'created_at': datetime.now(),
    },
)