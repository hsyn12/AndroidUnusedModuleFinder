import re

from SelectedDirectory import SelectedDirectory
from ModuleFinder import select_directory
from ModuleFinder import find_module
from ModuleFinder import _exit
from ModuleFinder import set_search_module

settings_gradle: str = 'settings.gradle'
all_modules: dict[str, list[str]] = dict()
selected_directory: str = ''


def get_selected_directory() -> str:
    return selected_directory


def get_declared_modules() -> list[str]:
    global selected_directory
    _modules: list[str] = []
    last_selected_directory: SelectedDirectory = SelectedDirectory()
    selected_directory = select_directory()
    if selected_directory and not selected_directory.isspace():
        last_selected_directory.value = selected_directory
    try:
        with open(f'{selected_directory}/{settings_gradle}', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('include '):
                    _modules.append(re.search(r'\'(.*?)\'', line).group(1))
    except FileNotFoundError as e:
        _exit(f"Not found : {e.filename}. Make sure that you have {settings_gradle} in your module root directory.")
    return _modules


def check() -> None:
    global all_modules
    modules = get_declared_modules()

    if not modules:
        _exit("No modules found in settings.gradle")

    print(f'{len(modules)} modules found in settings.gradle')
    print('Checking...')

    enumerated_modules: enumerate[str] = enumerate(modules, 1)
    _modules_len = len(modules)

    for index, module in enumerated_modules:
        set_search_module(module)
        print(f'{index:3} /{_modules_len:3} - Searching : {module}')
        used_in = find_module(f'{selected_directory}')
        if used_in:
            dl = all_modules.get(module)
            if not dl:
                all_modules[module] = used_in
            else:
                dl.extend(used_in)
        else:
            all_modules[module] = []

    print('-' * 62)
    unused_modules = [module for module in all_modules if not all_modules[module]]
    _unused_modules_len = len(unused_modules)
    print(f'{_unused_modules_len} modules unused')
    for index, module in enumerate(unused_modules, 1):
        print(f'{index:3}. {module}')


if __name__ == '__main__':
    check()
