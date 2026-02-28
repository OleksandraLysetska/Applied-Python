# Побудова списку років + позиція у рядку + позиція у файлі

import re
import datetime
from typing import Final

P_NAME: Final = r'\b[А-ЯЇҐЄІ][А-ЯЇҐЄІа-яїґіє]*\b'
P_STUD: Final = r'[А-ЯЇҐЄІ|A-Z]{2}\d{8}'
P_PHONE: Final = r'\+380\s\(\d{2}\)\s\d{3}\s\d{4}'
P_BIRTH_DATE: Final = r'\d{2}\.\d{2}\.\d{4}'


def extract_from_line(line: str, students: dict):
    x = line.strip('\n').split()
    data = ' '.join(x)  # переконуємось, що між словами точно один пропуск
    names = re.findall(P_NAME, data)
    success = len(names) == 3
    if not success:
        raise ValueError(f'Неправильний формат імені у рядку:\n{line}\n')

    stud = re.findall(P_STUD, data)
    success = success and len(stud) == 1
    if not success:
        raise ValueError(f'Неправильний формат номера у рядку:\n{line}\n')

    bdate = re.findall(P_BIRTH_DATE, data)
    success = success and len(bdate) == 1
    if not success:
        raise ValueError(f'Неправильний формат дати народження у рядку:\n{line}\n')

    phone = re.findall(P_PHONE, data)
    success = success and len(phone) == 1

    if not success:
        raise ValueError(f'Неправильний формат телефону у рядку:\n{line}\n')

    birthdate = datetime.datetime.strptime(bdate[0], '%d.%m.%Y')

    students[stud[0]] = (names, birthdate, phone[0])


def extract_from_file(filename):
    students = {}
    with open(filename, 'r', encoding='UTF-8') as f:
        data = f.readlines()
        for line in data:
            extract_from_line(line, students)
        return students


if __name__ == '__main__':
    file = r"Stud.txt"
    students = extract_from_file(file)
    for k, v in students.items():
        print(k, v, sep=': ')