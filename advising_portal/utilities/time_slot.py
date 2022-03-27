import time
import datetime

time_slots = {
    'S01': {
        'time_slot_id': 'S01',
        'day': 'S',
        'start_time': datetime.time(hour=8, minute=30, second=0),
        'end_time': datetime.time(hour=10, minute=0, second=0)
    },
    'S02': {
        'time_slot_id': 'S02',
        'day': 'S',
        'start_time': datetime.time(hour=10, minute=10, second=0),
        'end_time': datetime.time(hour=11, minute=40, second=0)
    },
    'S03': {
        'time_slot_id': 'S03',
        'day': 'S',
        'start_time': datetime.time(hour=11, minute=50, second=0),
        'end_time': datetime.time(hour=13, minute=20, second=0)
    },
    'S04': {
        'time_slot_id': 'S04',
        'day': 'S',
        'start_time': datetime.time(hour=13, minute=30, second=0),
        'end_time': datetime.time(hour=15, minute=0, second=0)
    },
    'S05': {
        'time_slot_id': 'S05',
        'day': 'S',
        'start_time': datetime.time(hour=15, minute=10, second=0),
        'end_time': datetime.time(hour=16, minute=40, second=0)
    },
    'S06': {
        'time_slot_id': 'S06',
        'day': 'S',
        'start_time': datetime.time(hour=8, minute=00, second=0),
        'end_time': datetime.time(hour=10, minute=0, second=0)
    },
    'S07': {
        'time_slot_id': 'S07',
        'day': 'S',
        'start_time': datetime.time(hour=10, minute=10, second=0),
        'end_time': datetime.time(hour=12, minute=10, second=0)
    },
    'S08': {
        'time_slot_id': 'S08',
        'day': 'S',
        'start_time': datetime.time(hour=13, minute=30, second=0),
        'end_time': datetime.time(hour=15, minute=30, second=0)
    },
    'S09': {
        'time_slot_id': 'S09',
        'day': 'S',
        'start_time': datetime.time(hour=16, minute=50, second=0),
        'end_time': datetime.time(hour=18, minute=50, second=0)
    },
    'S10': {
        'time_slot_id': 'S10',
        'day': 'S',
        'start_time': datetime.time(hour=11, minute=50, second=0),
        'end_time': datetime.time(hour=14, minute=50, second=0)
    },
    'S11': {
        'time_slot_id': 'S11',
        'day': 'S',
        'start_time': datetime.time(hour=16, minute=50, second=0),
        'end_time': datetime.time(hour=19, minute=50, second=0)
    },
    'M01': {
        'time_slot_id': 'M01',
        'day': 'M',
        'start_time': datetime.time(hour=8, minute=30, second=0),
        'end_time': datetime.time(hour=10, minute=0, second=0)
    },
    'M02': {
        'time_slot_id': 'M02',
        'day': 'M',
        'start_time': datetime.time(hour=10, minute=10, second=0),
        'end_time': datetime.time(hour=11, minute=40, second=0)
    },
    'M03': {
        'time_slot_id': 'M03',
        'day': 'M',
        'start_time': datetime.time(hour=11, minute=50, second=0),
        'end_time': datetime.time(hour=13, minute=20, second=0)
    },
    'M04': {
        'time_slot_id': 'M04',
        'day': 'M',
        'start_time': datetime.time(hour=13, minute=30, second=0),
        'end_time': datetime.time(hour=15, minute=0, second=0)
    },
    'M05': {
        'time_slot_id': 'M05',
        'day': 'M',
        'start_time': datetime.time(hour=15, minute=10, second=0),
        'end_time': datetime.time(hour=16, minute=40, second=0)
    },
    'M06': {
        'time_slot_id': 'M06',
        'day': 'M',
        'start_time': datetime.time(hour=8, minute=00, second=0),
        'end_time': datetime.time(hour=10, minute=0, second=0)
    },
    'M07': {
        'time_slot_id': 'M07',
        'day': 'M',
        'start_time': datetime.time(hour=10, minute=10, second=0),
        'end_time': datetime.time(hour=12, minute=10, second=0)
    },
    'M08': {
        'time_slot_id': 'M08',
        'day': 'M',
        'start_time': datetime.time(hour=13, minute=30, second=0),
        'end_time': datetime.time(hour=15, minute=30, second=0)
    },
    'M09': {
        'time_slot_id': 'M09',
        'day': 'M',
        'start_time': datetime.time(hour=16, minute=50, second=0),
        'end_time': datetime.time(hour=18, minute=50, second=0)
    },
    'M10': {
        'time_slot_id': 'M10',
        'day': 'M',
        'start_time': datetime.time(hour=11, minute=50, second=0),
        'end_time': datetime.time(hour=14, minute=50, second=0)
    },
    'M11': {
        'time_slot_id': 'M11',
        'day': 'M',
        'start_time': datetime.time(hour=16, minute=50, second=0),
        'end_time': datetime.time(hour=19, minute=50, second=0)
    },
    'T01': {
        'time_slot_id': 'T01',
        'day': 'T',
        'start_time': datetime.time(hour=8, minute=30, second=0),
        'end_time': datetime.time(hour=10, minute=0, second=0)
    },
    'T02': {
        'time_slot_id': 'T02',
        'day': 'T',
        'start_time': datetime.time(hour=10, minute=10, second=0),
        'end_time': datetime.time(hour=11, minute=40, second=0)
    },
    'T03': {
        'time_slot_id': 'T03',
        'day': 'T',
        'start_time': datetime.time(hour=11, minute=50, second=0),
        'end_time': datetime.time(hour=13, minute=20, second=0)
    },
    'T04': {
        'time_slot_id': 'T04',
        'day': 'T',
        'start_time': datetime.time(hour=13, minute=30, second=0),
        'end_time': datetime.time(hour=15, minute=0, second=0)
    },
    'T05': {
        'time_slot_id': 'T05',
        'day': 'T',
        'start_time': datetime.time(hour=15, minute=10, second=0),
        'end_time': datetime.time(hour=16, minute=40, second=0)
    },
    'T06': {
        'time_slot_id': 'T06',
        'day': 'T',
        'start_time': datetime.time(hour=8, minute=00, second=0),
        'end_time': datetime.time(hour=10, minute=0, second=0)
    },
    'T07': {
        'time_slot_id': 'T07',
        'day': 'T',
        'start_time': datetime.time(hour=10, minute=10, second=0),
        'end_time': datetime.time(hour=12, minute=10, second=0)
    },
    'T08': {
        'time_slot_id': 'T08',
        'day': 'T',
        'start_time': datetime.time(hour=13, minute=30, second=0),
        'end_time': datetime.time(hour=15, minute=30, second=0)
    },
    'T09': {
        'time_slot_id': 'T09',
        'day': 'T',
        'start_time': datetime.time(hour=16, minute=50, second=0),
        'end_time': datetime.time(hour=18, minute=50, second=0)
    },
    'T10': {
        'time_slot_id': 'T10',
        'day': 'T',
        'start_time': datetime.time(hour=11, minute=50, second=0),
        'end_time': datetime.time(hour=14, minute=50, second=0)
    },
    'T11': {
        'time_slot_id': 'T11',
        'day': 'T',
        'start_time': datetime.time(hour=16, minute=50, second=0),
        'end_time': datetime.time(hour=19, minute=50, second=0)
    },
    'W01': {
        'time_slot_id': 'W01',
        'day': 'W',
        'start_time': datetime.time(hour=8, minute=30, second=0),
        'end_time': datetime.time(hour=10, minute=0, second=0)
    },
    'W02': {
        'time_slot_id': 'W02',
        'day': 'W',
        'start_time': datetime.time(hour=10, minute=10, second=0),
        'end_time': datetime.time(hour=11, minute=40, second=0)
    },
    'W03': {
        'time_slot_id': 'W03',
        'day': 'W',
        'start_time': datetime.time(hour=11, minute=50, second=0),
        'end_time': datetime.time(hour=13, minute=20, second=0)
    },
    'W04': {
        'time_slot_id': 'W04',
        'day': 'W',
        'start_time': datetime.time(hour=13, minute=30, second=0),
        'end_time': datetime.time(hour=15, minute=0, second=0)
    },
    'W05': {
        'time_slot_id': 'W05',
        'day': 'W',
        'start_time': datetime.time(hour=15, minute=10, second=0),
        'end_time': datetime.time(hour=16, minute=40, second=0)
    },
    'W06': {
        'time_slot_id': 'W06',
        'day': 'W',
        'start_time': datetime.time(hour=8, minute=00, second=0),
        'end_time': datetime.time(hour=10, minute=0, second=0)
    },
    'W07': {
        'time_slot_id': 'W07',
        'day': 'W',
        'start_time': datetime.time(hour=10, minute=10, second=0),
        'end_time': datetime.time(hour=12, minute=10, second=0)
    },
    'W08': {
        'time_slot_id': 'W08',
        'day': 'W',
        'start_time': datetime.time(hour=13, minute=30, second=0),
        'end_time': datetime.time(hour=15, minute=30, second=0)
    },
    'W09': {
        'time_slot_id': 'W09',
        'day': 'W',
        'start_time': datetime.time(hour=16, minute=50, second=0),
        'end_time': datetime.time(hour=18, minute=50, second=0)
    },
    'W10': {
        'time_slot_id': 'W10',
        'day': 'W',
        'start_time': datetime.time(hour=11, minute=50, second=0),
        'end_time': datetime.time(hour=14, minute=50, second=0)
    },
    'W11': {
        'time_slot_id': 'W11',
        'day': 'W',
        'start_time': datetime.time(hour=16, minute=50, second=0),
        'end_time': datetime.time(hour=19, minute=50, second=0)
    },
    'R01': {
        'time_slot_id': 'R01',
        'day': 'R',
        'start_time': datetime.time(hour=8, minute=30, second=0),
        'end_time': datetime.time(hour=10, minute=0, second=0)
    },
    'R02': {
        'time_slot_id': 'R02',
        'day': 'R',
        'start_time': datetime.time(hour=10, minute=10, second=0),
        'end_time': datetime.time(hour=11, minute=40, second=0)
    },
    'R03': {
        'time_slot_id': 'R03',
        'day': 'R',
        'start_time': datetime.time(hour=11, minute=50, second=0),
        'end_time': datetime.time(hour=13, minute=20, second=0)
    },
    'R04': {
        'time_slot_id': 'R04',
        'day': 'R',
        'start_time': datetime.time(hour=13, minute=30, second=0),
        'end_time': datetime.time(hour=15, minute=0, second=0)
    },
    'R05': {
        'time_slot_id': 'R05',
        'day': 'R',
        'start_time': datetime.time(hour=15, minute=10, second=0),
        'end_time': datetime.time(hour=16, minute=40, second=0)
    },
    'R06': {
        'time_slot_id': 'R06',
        'day': 'R',
        'start_time': datetime.time(hour=8, minute=00, second=0),
        'end_time': datetime.time(hour=10, minute=0, second=0)
    },
    'R07': {
        'time_slot_id': 'R07',
        'day': 'R',
        'start_time': datetime.time(hour=10, minute=10, second=0),
        'end_time': datetime.time(hour=12, minute=10, second=0)
    },
    'R08': {
        'time_slot_id': 'R08',
        'day': 'R',
        'start_time': datetime.time(hour=13, minute=30, second=0),
        'end_time': datetime.time(hour=15, minute=30, second=0)
    },
    'R09': {
        'time_slot_id': 'R09',
        'day': 'R',
        'start_time': datetime.time(hour=16, minute=50, second=0),
        'end_time': datetime.time(hour=18, minute=50, second=0)
    },
    'R10': {
        'time_slot_id': 'R10',
        'day': 'R',
        'start_time': datetime.time(hour=11, minute=50, second=0),
        'end_time': datetime.time(hour=14, minute=50, second=0)
    },
    'R11': {
        'time_slot_id': 'R11',
        'day': 'R',
        'start_time': datetime.time(hour=16, minute=50, second=0),
        'end_time': datetime.time(hour=19, minute=50, second=0)
    }
}
