# Побудова списку років + позиція у рядку + позиція у файлі

import re
from typing import Final

path = r"C:\!МОЄ\Прикладна\Прикладне програмування\Лекції\Презентації\Lec 3 prog\KyivRus.txt"

YEAR_PAT_1: Final = r"\d{3,4}"
YEAR_PAT: Final = re.compile(YEAR_PAT_1)  # проекомпільований рядок клас re.Pattern



def years_in_file(file):
    """Отримуання відомостей про роки та номери рядків їх входжень у файлі"""

    years = []  # список знайдених років

    with open(file, 'r') as f:
        text = f.readlines()
        for i, line in enumerate(text, start=1):
            years_in_line(line, i, years)  # обробка одного рядка файлу
    return years

def years_in_line(line, line_number, years):
    """Отримання відомостей про роки у одній стрічці файлу та їх позиції у рядку"""

    all_years = YEAR_PAT.finditer(line)  # послідовність років з класу re.Match
    for year in all_years:
        years.append((int(str(year.group())), line_number, find_position_in_line(year, line)))  
def find_position_in_line(year, line):
    """Пошук позиції року у рядку"""""
    pos = year.span()  # кортеж (початок, кінець) позиції року у рядку
    return pos



years = years_in_file(path)
years.sort()

print('year, line')
for y in years:
    print(y)