from advising_portal.models import Student, Semester, Section, Grade


grade_report = [
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=1),
        'section': Section.objects.get(section_id='CSE1031'),
        'grade': Grade.objects.get(grade='A-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=1),
        'section': Section.objects.get(section_id='ENG1011'),
        'grade': Grade.objects.get(grade='A')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=1),
        'section': Section.objects.get(section_id='MAT1011'),
        'grade': Grade.objects.get(grade='C+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=2),
        'section': Section.objects.get(section_id='CSE1061'),
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=2),
        'section': Section.objects.get(section_id='ENG1021'),
        'grade': Grade.objects.get(grade='A-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=2),
        'section': Section.objects.get(section_id='MAT1021'),
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=3),
        'section': Section.objects.get(section_id='CSE1101'),
        'grade': Grade.objects.get(grade='B+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=3),
        'section': Section.objects.get(section_id='MAT1041'),
        'grade': Grade.objects.get(grade='D+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=3),
        'section': Section.objects.get(section_id='CHE1091'),
        'grade': Grade.objects.get(grade='C+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=4),
        'section': Section.objects.get(section_id='CSE2091'),
        'grade': Grade.objects.get(grade='A-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=4),
        'section': Section.objects.get(section_id='GEN2261'),
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=4),
        'section': Section.objects.get(section_id='ECO1011'),
        'grade': Grade.objects.get(grade='A-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=5),
        'section': Section.objects.get(section_id='CSE2511'),
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=5),
        'section': Section.objects.get(section_id='STA1021'),
        'grade': Grade.objects.get(grade='B-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=5),
        'section': Section.objects.get(section_id='PHY1091'),
        'grade': Grade.objects.get(grade='C-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=6),
        'section': Section.objects.get(section_id='CSE2071'),
        'grade': Grade.objects.get(grade='B+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=6),
        'section': Section.objects.get(section_id='BUS2311'),
        'grade': Grade.objects.get(grade='A')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=6),
        'section': Section.objects.get(section_id='MAT2051'),
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=7),
        'section': Section.objects.get(section_id='CSE2461'),
        'grade': Grade.objects.get(grade='A-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=7),
        'section': Section.objects.get(section_id='CSE3251'),
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=7),
        'section': Section.objects.get(section_id='PHY2091'),
        'grade': Grade.objects.get(grade='B+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=8),
        'section': Section.objects.get(section_id='CSE2001'),
        'grade': Grade.objects.get(grade='B+')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=8),
        'section': Section.objects.get(section_id='CSE3021'),
        'grade': Grade.objects.get(grade='B')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=8),
        'section': Section.objects.get(section_id='CSE3451'),
        'grade': Grade.objects.get(grade='B-')
    },
    {
        'student': Student.objects.get(student_id='2019-2-60-022'),
        'semester': Semester.objects.get(semester_id=8),
        'section': Section.objects.get(section_id='CSE3601'),
        'grade': Grade.objects.get(grade='C')
    }
]
