import argparse
import json
import os
import random
import re
from datetime import datetime

import requests


def data_online():
    headers = [
        {
            'Host': 'faportal.ewubd.edu',
            'User-Agent': 'Mozilla/5.0 (X11; Windows x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://portal.ewubd.edu',
            'Connection': 'keep-alive',
            'Referer': 'https://portal.ewubd.edu/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-GPC': '1',
            'TE': 'trailers',
        },
        {
            'authority': 'faportal.ewubd.edu',
            'method': 'GET',
            'path': '/api/FacultyInfo/GetAllFaculty',
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://portal.ewubd.edu',
            'referer': 'https://portal.ewubd.edu/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (X11; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34',
        }
    ]

    headers = random.choice(headers)

    all_sections = []

    semester = requests.get('https://faportal.ewubd.edu/api/Semester/GetSemesterForDropDown', headers=headers)
    semester = semester.json()[1]['SemesterId']

    result = requests.get(
        f'https://faportal.ewubd.edu/api/OfferedCourses/GetAllOfferedCourses?deptid=undefined&semesterid='
        f'{semester}',
        headers=headers
    )

    all_sections.extend(result.json())

    return all_sections


all_section = data_online()

time_slots = []

for section in all_section:
    if section['TimeSlotName'] not in time_slots:
        if section['TimeSlotName'].startswith(('S', 'M', 'T', 'W', 'R')):
            time_slots.append(section['TimeSlotName'])


print(time_slots)
