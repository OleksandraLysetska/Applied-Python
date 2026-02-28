# Побудова списку років + позиція у рядку + позиція у файлі

import re
from typing import Final

path = r"KyivRus.txt"

YEAR_PAT: Final = r"\d{3,4}"


def years_in_file(file):
    """Отримуання відомостей про роки та номери рядків їх входжень у файлі"""

    years = []  # список знайдених років

    with open(file, 'r') as f:
        text = f.readlines()
        for i, line in enumerate(text, 1):
            years_in_line(line, i, years)  # обробка одного рядка файлу
    return years

def years_in_line(line, line_number, years):
    """Отримання відомостей про роки у одній стрічці файлу"""

    all_years = re.findall(YEAR_PAT, line)  # ітерована послідовність років
    for year in all_years:
        years.append((int(year), line_number))


years = years_in_file(path)
years.sort()

print('year, line')
for y in years:
    print(y)