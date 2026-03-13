import os
import datetime
import sys
import tarfile

SIZE = 1024 * 500  # розмір файлу, який опрацьовуємо за 1 раз


def copyfile(filename, fromdir, todir):
    """Функція, що копіює один файл з одного каталогу до іншого  """

    from_full_path = os.path.join(fromdir, filename)
    to_full_path = os.path.join(todir, filename)

    with open(from_full_path, 'rb') as fromfile, open(to_full_path,'wb') as tofile:
        if os.path.getsize(filename) <=SIZE:
            temp = fromfile.read()
            tofile.write(temp)
        else:
            while True:
                temp = fromfile.read(SIZE)
                if not temp: break
                tofile.write(temp)


def copydir(fromdir, toparent):
    """Функція, що рекурсивно копіює каталог 
    разом з усіма його підкаталогами в інший каталог"""

    fromdir = os.path.normpath(fromdir)  # видалити подвійні слеші
    toparent = os.path.normpath(toparent)

    last_dir = os.path.split(fromdir)[-1]
    curdir = os.path.join(toparent, last_dir)
    print(curdir)

    # створюємо підкаталог
    os.mkdir(curdir)

    lst = os.listdir(fromdir)
    for name in lst:
        full_name = os.path.join(fromdir, name)
        if os.path.isfile(full_name):
            try:
                copyfile(name,fromdir,curdir)
            except Exception as e:
                print(f'Пропущено файл {name}.\n', e)
        else:
            copydir(full_name, curdir)


def removedir(dir):
    """Функція, що видаляє з каталогу dir увесь вміст і вкінці видаляє сам каталог dir"""

    dir = os.path.normpath(dir)  #видаляє подвійні слеші
    lst = os.listdir(dir)

    for name in lst:
        fullname = os.path.join(dir, name)
        if os.path.isfile(fullname):
            try:
                os.remove(fullname)
            except Exception as e:
                print('Пропуск видалення файлу', name, e, sep='\n')
        else:
            removedir(fullname)
        os.rmdir(dir)  # вкінці видаляємо порожній каталог


def archivesubdirs(dir):
    """Функція для архівації всіх підкаталогів каталогу dir"""

    dir = os.path.normpath(dir) # видалити подвійні слеші, якщо є
    lst = os.listdir(dir)

    for name in lst:
        full_name = os.path.join(dir, name)

        if os.path.isdir(full_name):
            try:
                tf = tarfile.open(full_name+'.tar.gz', 'w:gz')
                tf.add(full_name)
                tf.close()
                removedir(full_name)
            except Exception as e:
                print('Помилка архівації',  name, e, sep='\n')


def getbackupname(backupdir):
    """Функція, що повертає ім’я нового каталогу, у який будуть збережені дані. 
    Це ім’я формується у вигляді рядка з поточної дати та часу."""
    
    dt = datetime.datetime.now()
    dirname = dt.strftime('%Y%m%d_%H%M%S')
    return os.path.join(backupdir, dirname)



def backupdirectories(directories, backupdir):
    """Функція, що зберігає файли із зазначених каталогів у каталозі backup і архівує їхні попередні версії"""

    archivesubdirs(backupdir)  # архівуємо попереді версії

    toparent = getbackupname(backupdir)
    os.mkdir(toparent)

    for dir in directories:
        try:
            copydir(dir, toparent)
        except Exception as e:
            print(f'Пропущено директорію {dir}.\n', e)



if __name__ == '__main__':
    if len(sys.argv) < 3: # введено замало параметрів
        backupdir = input('Введіть backup-каталог').strip(' \'"')
        user_input = input("Введіть імена каталогів для бекапу через кому:\n")
        directories = [d.strip(' \'"') for d in user_input.split(",") if d.strip()]
    
    else:
        backupdir = sys.argv[1]
        directories = sys.argv[2:]
    backupdirectories(directories, backupdir)



