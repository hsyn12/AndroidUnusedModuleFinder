import os
from tkinter import filedialog
from os import listdir
from os import path
import re
from SelectedDirectory import SelectedDirectory

if os.name == 'nt':
    import msvcrt

_search_module = ''
last_selected_directory: SelectedDirectory = SelectedDirectory()
str_build_gradle: str = 'build.gradle'
str_build_gradle_kts: str = 'build.gradle.kts'


def set_search_module(module: str) -> None:
    global _search_module
    _search_module = module


def info() -> None:
    print('-' * 62)
    print('-l : library module [search prefix of exactly what is entered]')
    print('-p : project module [search prefix of project library]')
    print('For example, "time -p" : search with ":time"')
    print('This is same as "time", -p arg is default')
    print('-' * 62)


def _exit(msg: str) -> None:
    print(msg)
    print('Enter any key to exit')
    if os.name == 'nt':
        msvcrt.getch()
    else:
        input()
    exit()


def select_directory(default_directory: str = None) -> str:
    return filedialog.askdirectory(initialdir=default_directory, title='Select Module Root Directory')


# noinspection PyBroadException
def _find_module(file_path: str) -> list[str]:
    modules = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if re.search(rf'{_search_module}[^:]', line):
                    modules.append(file_path)
    except FileNotFoundError as e:
        print("Not found :", e.filename)
    except:
        pass
    return modules


def find_module(root_directory: str) -> list[str]:
    modules = []
    for file in listdir(root_directory):
        folder = f'{root_directory}/{file}'
        if path.isdir(folder):
            modules.extend(find_module(folder))
        else:
            if file == str_build_gradle or file == str_build_gradle_kts:
                modules.extend(_find_module(folder))
    return modules


if __name__ == '__main__':
    print('Select Module Root Directory')
    # if not last_selected_directory.value:
    last_selected_directory.value = select_directory()
    if not last_selected_directory.value:
        _exit("No directory selected")

    print('Directory :', last_selected_directory.value)
    info()

    _search_module = input("Enter module name to search : ")

    if not _search_module or _search_module.isspace():
        _exit("No search module")
    if not re.search(r'-.\b', _search_module):
        if not _search_module.startswith(':'):
            _search_module = ':' + _search_module
    else:
        args: list[str] = re.findall(r'-.\b', _search_module)
        print(args)
        if len(args) == 1:
            _search_module = _search_module.replace(args[0], '', 1).strip()
            if args[0].endswith('p'):
                if not _search_module.startswith(':'):
                    _search_module = ':' + _search_module
        else:
            _exit('Search Module should contain one argument')

    dc = 70
    print(f'Searching : "{_search_module}"')
    modules: list[str] = find_module(last_selected_directory.value)
    if modules:
        print('-' * dc)
        print(*modules, sep='\n')
        print('-' * dc)
    print(f'Found {len(modules)} modules')
    _exit("Done")
