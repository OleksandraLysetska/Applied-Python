import re
import datetime
from typing import Final

P_NAME: Final = r'(\b[А-ЯЇҐЄІ][А-ЯЇҐЄІа-яїґіє]*)'
P_STUD: Final = r'([А-ЯЇҐЄІ|A-Z]{2}\d{8})'
P_PHONE: Final = r'''(\+380\s\(\d{2}\)\s\d{3}\s\d{4}  |    # +380 ()....
                        380\s\(\d{2}\)\s\d{3}\s\d{4}  |    # 380 ()....
                              \(\d{2}\)\s\d{3}\s\d{4}  |    # ()....
                              )'''
P_BIRTH_DATE: Final = r'''(
    \d{1,2}\.\d{1,2}\.\d{4} |   # dd.mm.yyyy
    \d{1,2}/\d{1,2}/\d{4}  |    # dd/mm/yyyy
    \d{4}-\d{1,2}-\d{1,2}       # yyyy-mm-dd
)'''
PATTERN_STUDENT = r'\s'.join([P_NAME, P_NAME, P_NAME, P_STUD, P_BIRTH_DATE, P_PHONE])


def formatdate(date: str) -> str:
    '''Приймає рядок з датою і повертає відповідний йому формат'''
    dateformat = None
    if '.' in date:
        dateformat = '%d.%m.%Y'
    elif '/' in date:
        dateformat = '%d/%m/%Y'
    elif '-' in date:
        dateformat = '%Y-%m-%d'

    return dateformat


def getdate(date: str) -> str:
    '''Приймає дату, опрацьовує її формат і повертає читабельний рядок'''
    date_format = formatdate(date)
    datetime_format = datetime.datetime.strptime(date, date_format)
    return datetime_format.strftime(formatdate(date))


def extract_from_line(line: str, students: dict, pat: re.Pattern):
    '''Опрацьовує один рядок line згідно шаблону pat 
        і записує дані студента у вигляді кортежу у словник students 
        з ключами у вигляді номерів залікових'''

    x = line.strip('\n').split()
    data = ' '.join(x)  # Переконуємось, що між словами точно один пропуск
    result = pat.search(data)
    if result is None:
        raise ValueError(f'Неправильний формат даних у рядку {line}.')

    st = result.groups()  # кортеж із зчитаними даними
    key = st[3]  # Номер студ. квитка - ключ у словнику
    correct_date = getdate(st[-2])  # Дата

    students[key] = (*st[0:3], correct_date, st[-1])


def extract_from_file(filename):
    '''Функція для зчитування файлу filename та опрацьовування його записів'''
    studs = {}
    stud_pattern = re.compile(PATTERN_STUDENT, flags=re.VERBOSE)
    with open(filename, 'r', encoding='UTF-8') as f:
        data = f.readlines()
        for line in data:
            extract_from_line(line, studs, stud_pattern)

    return studs


if __name__ == '__main__':
    #file = input('Enter file name')
    file = r"data\Stud1.txt"
    students_data = extract_from_file(file)
    for k, v in students_data.items():
        print(k, ' '.join(v), sep=': ')
