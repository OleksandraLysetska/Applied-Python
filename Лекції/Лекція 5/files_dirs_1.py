import os


def dirsize(path):
    """Функція, що повертає розмір однієї директорії (какталогу)"""
    size = 0
    for root, dirs, files in os.walk(path):
        size += sum(os.path.getsize(os.path.join(root, name)) for name in files)
    return size

def dirslist(directory):
    '''Функція, що повертає список пар (каталог, розмір)'''
    dir_list = os.listdir(directory)
    dirs_sizes = []

    for dir in dir_list:
        path = os.path.join(directory, dir)

        if os.path.isdir(path):
            dirs_sizes.append((path, dirsize(path)))

    dirs_sizes.sort(reverse=True, key=lambda x: x[1])
    return dirs_sizes


if __name__ == '__main__':
    import sys

    # sys.argv - список параметрів, що передаються програмі в інтерпретаторі
    if len(sys.argv) == 1:
        directory: str = input('Input directory  name: ')
    else:
        directory = sys.argv[1]
    dirs_sizes = dirslist(directory)

    for _ in dirs_sizes:
        print(f'directory: {_[0]}, size: {_[1]}')

        