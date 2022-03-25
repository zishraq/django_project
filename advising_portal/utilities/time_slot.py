import time
import datetime

time_slots = {
    'S01': {
        'time_slot_id': 'S01',
        'day': 'S',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
    },
    'S02': {
        'time_slot_id': 'S02',
        'day': 'S',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
    },
    'S03': {
        'time_slot_id': 'S03',
        'day': 'S',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=20, second=0).time()
    },
    'S04': {
        'time_slot_id': 'S04',
        'day': 'S',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=0, second=0).time()
    },
    'S05': {
        'time_slot_id': 'S05',
        'day': 'S',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=40, second=0).time()
    },
    'S06': {
        'time_slot_id': 'S06',
        'day': 'S',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
    },
    'S07': {
        'time_slot_id': 'S07',
        'day': 'S',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
    },
    'S08': {
        'time_slot_id': 'S08',
        'day': 'S',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=30, second=0).time()
    },
    'S09': {
        'time_slot_id': 'S09',
        'day': 'S',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=18, minute=50, second=0).time()
    },
    'S10': {
        'time_slot_id': 'S10',
        'day': 'S',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=14, minute=50, second=0).time()
    },
    'S11': {
        'time_slot_id': 'S11',
        'day': 'S',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=19, minute=50, second=0).time()
    },
    'M01': {
        'time_slot_id': 'M01',
        'day': 'M',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
    },
    'M02': {
        'time_slot_id': 'M02',
        'day': 'M',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
    },
    'M03': {
        'time_slot_id': 'M03',
        'day': 'M',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=20, second=0).time()
    },
    'M04': {
        'time_slot_id': 'M04',
        'day': 'M',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=0, second=0).time()
    },
    'M05': {
        'time_slot_id': 'M05',
        'day': 'M',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=40, second=0).time()
    },
    'M06': {
        'time_slot_id': 'M06',
        'day': 'M',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
    },
    'M07': {
        'time_slot_id': 'M07',
        'day': 'M',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
    },
    'M08': {
        'time_slot_id': 'M08',
        'day': 'M',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=30, second=0).time()
    },
    'M09': {
        'time_slot_id': 'M09',
        'day': 'M',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=18, minute=50, second=0).time()
    },
    'M10': {
        'time_slot_id': 'M10',
        'day': 'M',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=14, minute=50, second=0).time()
    },
    'M11': {
        'time_slot_id': 'M11',
        'day': 'M',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=19, minute=50, second=0).time()
    },
    'T01': {
        'time_slot_id': 'T01',
        'day': 'T',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
    },
    'T02': {
        'time_slot_id': 'T02',
        'day': 'T',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
    },
    'T03': {
        'time_slot_id': 'T03',
        'day': 'T',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=20, second=0).time()
    },
    'T04': {
        'time_slot_id': 'T04',
        'day': 'T',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=0, second=0).time()
    },
    'T05': {
        'time_slot_id': 'T05',
        'day': 'T',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=40, second=0).time()
    },
    'T06': {
        'time_slot_id': 'T06',
        'day': 'T',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
    },
    'T07': {
        'time_slot_id': 'T07',
        'day': 'T',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
    },
    'T08': {
        'time_slot_id': 'T08',
        'day': 'T',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=30, second=0).time()
    },
    'T09': {
        'time_slot_id': 'T09',
        'day': 'T',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=18, minute=50, second=0).time()
    },
    'T10': {
        'time_slot_id': 'T10',
        'day': 'T',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=14, minute=50, second=0).time()
    },
    'T11': {
        'time_slot_id': 'T11',
        'day': 'T',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=19, minute=50, second=0).time()
    },
    'W01': {
        'time_slot_id': 'W01',
        'day': 'W',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
    },
    'W02': {
        'time_slot_id': 'W02',
        'day': 'W',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
    },
    'W03': {
        'time_slot_id': 'W03',
        'day': 'W',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=20, second=0).time()
    },
    'W04': {
        'time_slot_id': 'W04',
        'day': 'W',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=0, second=0).time()
    },
    'W05': {
        'time_slot_id': 'W05',
        'day': 'W',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=40, second=0).time()
    },
    'W06': {
        'time_slot_id': 'W06',
        'day': 'W',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
    },
    'W07': {
        'time_slot_id': 'W07',
        'day': 'W',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
    },
    'W08': {
        'time_slot_id': 'W08',
        'day': 'W',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=30, second=0).time()
    },
    'W09': {
        'time_slot_id': 'W09',
        'day': 'W',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=18, minute=50, second=0).time()
    },
    'W10': {
        'time_slot_id': 'W10',
        'day': 'W',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=14, minute=50, second=0).time()
    },
    'W11': {
        'time_slot_id': 'W11',
        'day': 'W',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=19, minute=50, second=0).time()
    },
    'R01': {
        'time_slot_id': 'R01',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
    },
    'R02': {
        'time_slot_id': 'R02',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=40, second=0).time()
    },
    'R03': {
        'time_slot_id': 'R03',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=20, second=0).time()
    },
    'R04': {
        'time_slot_id': 'R04',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=0, second=0).time()
    },
    'R05': {
        'time_slot_id': 'R05',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=40, second=0).time()
    },
    'R06': {
        'time_slot_id': 'R06',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=8, minute=00, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=0, second=0).time()
    },
    'R07': {
        'time_slot_id': 'R07',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=10, minute=10, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=12, minute=10, second=0).time()
    },
    'R08': {
        'time_slot_id': 'R08',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=13, minute=30, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=15, minute=30, second=0).time()
    },
    'R09': {
        'time_slot_id': 'R09',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=18, minute=50, second=0).time()
    },
    'R10': {
        'time_slot_id': 'R10',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=11, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=14, minute=50, second=0).time()
    },
    'R11': {
        'time_slot_id': 'R11',
        'day': 'R',
        'start_time': datetime.datetime(year=2020, month=1, day=1, hour=16, minute=50, second=0).time(),
        'end_time': datetime.datetime(year=2020, month=1, day=1, hour=19, minute=50, second=0).time()
    }
}
