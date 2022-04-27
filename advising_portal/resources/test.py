# from django.contrib.auth.models import User
# from django.utils import timezone
#
# from advising_portal.models import Department, TimeSlot, Course, Faculty
#
#
# # def generate_routine(routine):
# #     if routine == 'R 08:00 AM - 11:00 AM':
# #
#
#
#
#
# def create_data(data):
#     course_existence_check = Course.objects.filter(
#         course_code=data['CourseCode']
#     ).exists()
#
#     if not course_existence_check:
#         course_data = {}
#         if data['AcademicDepartmentShortName'] == 'CSE':
#             course_data['department'] = Department.objects.get(pk='CSE').pk
#         else:
#             course_data['department'] = Department.objects.get(pk='GEN').pk
#
#         course_data['course_id'] = data['CourseCode']
#         course_data['course_code'] = data['CourseCode']
#         course_data['course_title'] = data['CourseName']
#         course_data['credit'] = 3
#         course_data['created_at'] = timezone.now()
#         course_data['created_by_id'] = User.objects.get(username='admin').pk
#
#         c = Course(**course_data)
#         c.save()
#
#         faculty_existence_check = Faculty.objects.filter(
#             faculty_id=data['ShortName']
#         ).exists()
#
#         if not faculty_existence_check:
#             faculty_data = {
#                 'faculty_id': data['ShortName'],
#                 'initials': data['ShortName']
#             }
#
#             f = Faculty(**faculty_data)
#             f.save()
#
#             section_data = {
#                 'section_id': course_data['course_code'] + str(data['SectionName'])
#                 'section_no': int(data['SectionName']),
#                 'section_capacity': int(data['SeatCapacity']),
#                 'total_students': int(data['SeatTaken']),
#                 'instructor': f
#             }
#
