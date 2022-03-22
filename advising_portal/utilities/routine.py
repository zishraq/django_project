class TimeSlot():
    class objects:
        @staticmethod
        def get(pk):
            return pk


routine_slot = [
    {
        'routine_id': 'S01T01',
        'time_slot_id': TimeSlot.objects.get(pk='S01')
    },
    {
        'routine_id': 'S01T01',
        'time_slot_id': TimeSlot.objects.get(pk='T01')
    },
    {
        'routine_id': 'S02T02',
        'time_slot_id': TimeSlot.objects.get(pk='S02')
    },
    {
        'routine_id': 'S02T02',
        'time_slot_id': TimeSlot.objects.get(pk='T02')
    },
    {
        'routine_id': 'S03T03',
        'time_slot_id': TimeSlot.objects.get(pk='S03')
    },
    {
        'routine_id': 'S03T03',
        'time_slot_id': TimeSlot.objects.get(pk='T03')
    },
    {
        'routine_id': 'S04T04',
        'time_slot_id': TimeSlot.objects.get(pk='S04')
    },
    {
        'routine_id': 'S04T04',
        'time_slot_id': TimeSlot.objects.get(pk='T04')
    },
    {
        'routine_id': 'S04T04',
        'time_slot_id': TimeSlot.objects.get(pk='S04')
    },
    {
        'routine_id': 'S04T04',
        'time_slot_id': TimeSlot.objects.get(pk='T04')
    },
    {
        'routine_id': 'S05T05',
        'time_slot_id': TimeSlot.objects.get(pk='S05')
    },
    {
        'routine_id': 'S05T05',
        'time_slot_id': TimeSlot.objects.get(pk='T05')
    },
    {
        'routine_id': 'M01W01',
        'time_slot_id': TimeSlot.objects.get(pk='M01')
    },
    {
        'routine_id': 'M01W01',
        'time_slot_id': TimeSlot.objects.get(pk='W01')
    },
    {
        'routine_id': 'M02W02',
        'time_slot_id': TimeSlot.objects.get(pk='M02')
    },
    {
        'routine_id': 'M02W02',
        'time_slot_id': TimeSlot.objects.get(pk='W02')
    },
    {
        'routine_id': 'M03W03',
        'time_slot_id': TimeSlot.objects.get(pk='M03')
    },
    {
        'routine_id': 'M03W03',
        'time_slot_id': TimeSlot.objects.get(pk='W03')
    },
    {
        'routine_id': 'M04W04',
        'time_slot_id': TimeSlot.objects.get(pk='M04')
    },
    {
        'routine_id': 'M04W04',
        'time_slot_id': TimeSlot.objects.get(pk='W04')
    },
    {
        'routine_id': 'M04W04',
        'time_slot_id': TimeSlot.objects.get(pk='M04')
    },
    {
        'routine_id': 'M04W04',
        'time_slot_id': TimeSlot.objects.get(pk='W04')
    },
    {
        'routine_id': 'M05W05',
        'time_slot_id': TimeSlot.objects.get(pk='M05')
    },
    {
        'routine_id': 'M05W05',
        'time_slot_id': TimeSlot.objects.get(pk='W05')
    }
]
