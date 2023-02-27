from advising_portal.models import Student, Semester, Section, Grade

# regex = (?<=Section\.objects\.get\(section_id_id\=\'[A-Z0-9]{7}\')\)

grade_reports1 = [
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 4,
        'section_id': 'CSE1031',
        'grade': Grade.objects.get(grade='A-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 4,
        'section_id': 'ENG1011',
        'grade': Grade.objects.get(grade='A')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 4,
        'section_id': 'MAT1011',
        'grade': Grade.objects.get(grade='C+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 5,
        'section_id': 'CSE1061',
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 5,
        'section_id': 'ENG1021',
        'grade': Grade.objects.get(grade='A-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 5,
        'section_id': 'MAT1021',
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 6,
        'section_id': 'CSE1101',
        'grade': Grade.objects.get(grade='B+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 6,
        'section_id': 'MAT1041',
        'grade': Grade.objects.get(grade='D+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 6,
        'section_id': 'CHE1091',
        'grade': Grade.objects.get(grade='C+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 7,
        'section_id': 'CSE2091',
        'grade': Grade.objects.get(grade='A-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 7,
        'section_id': 'GEN2261',
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 7,
        'section_id': 'ECO1011',
        'grade': Grade.objects.get(grade='A-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 8,
        'section_id': 'CSE2511',
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 8,
        'section_id': 'STA1021',
        'grade': Grade.objects.get(grade='B-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 8,
        'section_id': 'PHY1091',
        'grade': Grade.objects.get(grade='C-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 9,
        'section_id': 'CSE2071',
        'grade': Grade.objects.get(grade='B+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 9,
        'section_id': 'BUS2311',
        'grade': Grade.objects.get(grade='A')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 9,
        'section_id': 'MAT2051',
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 10,
        'section_id': 'CSE2461',
        'grade': Grade.objects.get(grade='A-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 10,
        'section_id': 'CSE3251',
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 10,
        'section_id': 'PHY2091',
        'grade': Grade.objects.get(grade='B+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 11,
        'section_id': 'CSE2001',
        'grade': Grade.objects.get(grade='B+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 11,
        'section_id': 'CSE3021',
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 11,
        'section_id': 'CSE3451',
        'grade': Grade.objects.get(grade='B-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-025'),
        'semester_id': 11,
        'section_id': 'CSE3601',
        'grade': Grade.objects.get(grade='C')
    }
]

updated_grade_report1 = []


for grade_report in grade_reports1:
    formatted_data = {
        'student': grade_report['student'],
        'semester_id': grade_report['semester_id'],
        'section_id': str(grade_report['semester_id']) + grade_report['section_id'],
        'grade': grade_report['grade']
    }
    updated_grade_report1.append(formatted_data)


grade_reports2 = [
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 4,
        'section_id': 'CSE1031',
        'grade': Grade.objects.get(grade='C-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 4,
        'section_id': 'ENG1011',
        'grade': Grade.objects.get(grade='A')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 4,
        'section_id': 'MAT1011',
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 5,
        'section_id': 'CSE1061',
        'grade': Grade.objects.get(grade='C+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 5,
        'section_id': 'ENG1021',
        'grade': Grade.objects.get(grade='B+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 5,
        'section_id': 'MAT1021',
        'grade': Grade.objects.get(grade='D+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 6,
        'section_id': 'CSE1101',
        'grade': Grade.objects.get(grade='A-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 6,
        'section_id': 'MAT1041',
        'grade': Grade.objects.get(grade='R')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 6,
        'section_id': 'CHE1091',
        'grade': Grade.objects.get(grade='B-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 7,
        'section_id': 'CSE2091',
        'grade': Grade.objects.get(grade='C')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 7,
        'section_id': 'GEN2261',
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 7,
        'section_id': 'ECO1011',
        'grade': Grade.objects.get(grade='B+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 8,
        'section_id': 'CSE2511',
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 8,
        'section_id': 'STA1021',
        'grade': Grade.objects.get(grade='B-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 8,
        'section_id': 'PHY1091',
        'grade': Grade.objects.get(grade='C+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 9,
        'section_id': 'CSE2071',
        'grade': Grade.objects.get(grade='A')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 9,
        'section_id': 'BUS2311',
        'grade': Grade.objects.get(grade='A')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 9,
        'section_id': 'MAT2051',
        'grade': Grade.objects.get(grade='A-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 9,
        'section_id': 'MAT1041',
        'grade': Grade.objects.get(grade='C')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 10,
        'section_id': 'CSE2461',
        'grade': Grade.objects.get(grade='A')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 10,
        'section_id': 'CSE3251',
        'grade': Grade.objects.get(grade='B-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 10,
        'section_id': 'PHY2091',
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 11,
        'section_id': 'CSE2001',
        'grade': Grade.objects.get(grade='B+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 11,
        'section_id': 'CSE3021',
        'grade': Grade.objects.get(grade='A')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 11,
        'section_id': 'CSE3451',
        'grade': Grade.objects.get(grade='B+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester_id': 11,
        'section_id': 'CSE3601',
        'grade': Grade.objects.get(grade='B-')
    }
]

updated_grade_report2 = []

for grade_report in grade_reports2:
    formatted_data = {
        'student': grade_report['student'],
        'semester_id': grade_report['semester_id'],
        'section_id': str(grade_report['semester_id']) + grade_report['section_id'],
        'grade': grade_report['grade']
    }
    updated_grade_report2.append(formatted_data)
