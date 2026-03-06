import re
import datetime
import pickle  # для збереження колекцій
from typing import Final

P_NAME: Final = r'(\b[А-ЯЇҐЄІ][А-ЯЇҐЄІа-яїґіє]*)'
P_STUD: Final = r'([А-ЯЇҐЄІ|A-Z]{2}\d{8})'
P_PHONE: Final = r'''(\+380\s\(\d{2}\)\s\d{3}\s\d{4}  |    # +380 (098)...
                        380\s\(\d{2}\)\s\d{3}\s\d{4}  |    # 380 (098)...
                           \(?\d{2}\)?\s\d{3}\s\d{4}) |    # (098) ... або 098 ...'''
P_BIRTH_DATE: Final = r'''(
    \d{1,2}\.\d{1,2}\.\d{4} |   # dd.mm.yyyy
    \d{1,2}/\d{1,2}/\d{4}  |    # dd/mm/yyyy
    \d{4}-\d{1,2}-\d{1,2}       # yyyy-mm-dd
)'''
PATTERN_STUDENT = r'\s'.join([P_NAME, P_NAME, P_NAME, P_STUD, P_BIRTH_DATE, P_PHONE])

ERROR_COUNTER = 0


def getphone(phone):
    '''Приймає рядок з телефоном і повертає відповідний йому формат'''

    phone = re.sub(r'\D', '', phone)  # забираємо всі нецифрові символи +, (, )
    if len(phone) < 12:  # цифр разом з кодом 12
        phone = '38' + phone
    phone = f'+{phone[:3]} ({phone[3:5]}) {phone[5:8]} {phone[8:]}'
    return phone


def formatdate(date: str) -> str:
    '''Приймає рядок з датою і повертає відповідний йому формат'''

    dateformat = ''
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
    return datetime_format.strftime('%d.%m.%Y')


def extract_from_line(line: str, students: dict, pat: re.Pattern, file: str):
    '''Опрацьовує один рядок line згідно шаблону pat 
        і записує дані студента у вигляді кортежу у словник students 
        з ключами у вигляді номерів залікових'''

    global ERROR_COUNTER
    x = line.strip('\n').split()
    data = ' '.join(x)  # Переконуємось, що між словами точно один пропуск
    result = pat.search(data)

    try:
        st = result.groups()  # кортеж із зчитаними даними
        key = st[3]  # Номер студ. квитка - ключ у словнику
        correct_date = getdate(st[-2])
        correct_phone = getphone(st[-1])
        students[key] = (*st[0:3], correct_date, correct_phone)

    except ValueError as ve:
        ERROR_COUNTER += 1
        with open('logfile.txt', 'a') as log:
            log.write(f'{ERROR_COUNTER}. Запис: {line} у файлі {file}\nПомилка: {ve}\n\n')

    except TypeError as te:
        ERROR_COUNTER += 1
        with open('logfile.txt', 'a') as log:
            log.write(f'{ERROR_COUNTER}. Запис: {line} у файлі {file}\nПомилка: {te}\n\n')



def extract_from_file(filename):
    '''Функція для зчитування файлу filename та опрацьовування його записів'''

    studs = {}
    stud_pattern = re.compile(PATTERN_STUDENT, flags=re.VERBOSE)

    with open(filename, 'r', encoding='UTF-8') as f:
        data = f.readlines()
        for line in data:
            extract_from_line(line, studs, stud_pattern, filename)
    return studs

def write_to_file(data: dict) -> None:
    '''Функція для записування отриманих записів до файлу'''

    with open('final_file.txt', 'a') as final:
        for k, v in data.items():
            raw = ' '.join(v)
            final.write(f'{k}: {raw}\n')

if __name__ == '__main__':
    #file = input('Enter file name')
    file = r"data\Stud1.txt"
    students_data = extract_from_file(file)
    write_to_file(students_data)  # зберігаємо дані у текстовий файл

    # зберігаємо у pickle-файл
    with open(file+'.dat', 'wb') as h:
        pickle.dump(students_data, h)

    # зчитуємо з pickle-файла
    with open(file+'.dat', 'rb') as h:
        loaded_st_data = pickle.load(h)

        # виводимо у консоль
        for _ in loaded_st_data:
            print(_,': ', students_data[_])


Token = namedtuple('Token', ['type', 'value’]),

