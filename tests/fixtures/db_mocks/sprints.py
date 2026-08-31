from uuid import UUID
from datetime import datetime


SPRINTS = (
    {
        'id': UUID('f879f8de-3c91-4f29-8fcb-effb40127999'),
        'name': 'Спринт 1',
        'start_date': datetime(2023, 1, 1),
        'end_date': datetime(2023, 1, 15),
    },
    {
        'id': UUID('b3a7db69-fb51-4e92-8f88-f1db4757e81c'),
        'name': 'Спринт 2',
        'start_date': datetime(2023, 2, 1),
        'end_date': datetime(2023, 2, 15),
    },
)