import time
import datetime

time_slots = [
    {
        'time_slot_id': 'R01',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
    },
    {
        'time_slot_id': 'R02',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
    },
    {
        'time_slot_id': 'R03',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=20, second=0).time()
    },
    {
        'time_slot_id': 'R04',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=0, second=0).time()
    },
    {
        'time_slot_id': 'R05',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=40, second=0).time()
    },
    {
        'time_slot_id': 'R06',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
    },
    {
        'time_slot_id': 'R07',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
    },
    {
        'time_slot_id': 'R08',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=1, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=3, minute=30, second=0).time()
    },
    {
        'time_slot_id': 'R08',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=6, minute=50, second=0).time()
    },
    {
        'time_slot_id': 'R09',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=0, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=0, second=0).time()
    },
    {
        'time_slot_id': 'R10',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=2, minute=50, second=0).time()
    },
    {
        'time_slot_id': 'R11',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=4, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=7, minute=50, second=0).time()
    }
]
