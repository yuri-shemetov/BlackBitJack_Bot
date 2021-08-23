import os

def get_files_photos(path):
    files = []
    directory = os.listdir(path)
    directory.sort(reverse=True)
    for file in directory:
        if file.endswith('.jpg'):
            files.append(file)
    return files

def get_files_messages(path):
    files = []
    directory = os.listdir(path)
    directory.sort(reverse=True)
    for file in directory:
        if file.endswith('.txt'):
            files.append(file)
    return files

def remove_old_files(path, files):
    """ Оставляет последние 20 файлов, остальные удаляет """
    max_files = 20
    if len(files) < max_files:
        return
    i = 0
    for f in files:
        i += 1
        if i > max_files:
            os.remove(os.path.join(path, f))
