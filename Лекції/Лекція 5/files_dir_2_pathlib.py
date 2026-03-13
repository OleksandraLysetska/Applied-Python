from pathlib import Path
import datetime
import sys

SIZE = 1024 * 500  # розмір файлу, який обробляємо за один раз


def copyfile(filename, fromdir, todir):
    """Копіює один файл з одного каталогу до іншого"""
    from_path = Path(fromdir) / filename
    to_path = Path(todir) / filename

    with from_path.open('rb') as f_from, to_path.open('wb') as f_to:
        if from_path.stat().st_size <= SIZE:
            f_to.write(f_from.read())
        else:
            while True:
                chunk = f_from.read(SIZE)
                if not chunk:
                    break
                f_to.write(chunk)


def copydir(fromdir, toparent):
    """Рекурсивно копіює каталог разом із підкаталогами"""
    from_path = Path(fromdir).resolve()
    toparent = Path(toparent).resolve()

    curdir = toparent / from_path.name
    print(f"Копіюємо каталог: {curdir}")

    curdir.mkdir(parents=True, exist_ok=True)

    for item in from_path.iterdir():
        try:
            if item.is_file():
                copyfile(item.name, from_path, curdir)
            else:
                copydir(item, curdir)
        except Exception as e:
            print(f"Пропущено: {item}\n", e)


def getbackupname(backupdir):
    """Повертає ім’я нового каталогу для бекапу (рядок з дати і часу)"""
    dt = datetime.datetime.now()
    dirname = dt.strftime('%Y%m%d_%H%M%S')
    return Path(backupdir) / dirname


def backupdirectories(directories=None, backupdir=None):
    """Зберігає файли з вказаних каталогів у каталозі backup"""
    if backupdir is None:
        backupdir = input('Введіть backup-каталог').strip(' \'"')
    if directories is None or len(directories) == 0:
        user_input = input("Введіть імена каталогів для бекапу через кому:\n")
        directories = [d.strip(' \'"') for d in user_input.split(",") if d.strip()]

    toparent = getbackupname(backupdir)
    toparent.mkdir(parents=True, exist_ok=True)

    for dir_path in directories:
        try:
            copydir(dir_path, toparent)
        except Exception as e:
            print(f"Пропущено директорію {dir_path}\n", e)

    print(f"\nБекап завершено. Файли збережено у: {toparent}")


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        backup_dir_arg = sys.argv[1]
        directories_arg = sys.argv[2:]
    else:
        backup_dir_arg = None
        directories_arg = None

    backupdirectories(directories_arg, backup_dir_arg)