import os
import shutil


def copy_paste(folders, files, destination):
    for folder in folders:
        shutil.copytree(folder, destination + folder[folder.rindex('/'):], dirs_exist_ok=True)
    for file in files:
        shutil.copy2(file, destination)


def rename(source, needed_name):
    os.rename(source, needed_name)


def create_folder(folder_name):
    os.mkdir(folder_name)


def cut_paste(folders, files, destination):
    for folder in folders:
        shutil.move(folder, destination + folder[folder.rindex('/'):])
    for file in files:
        shutil.move(file, destination)


def delete(folders, files):
    for folder in folders:
        shutil.rmtree(folder)
    for file in files:
        os.remove(file)
