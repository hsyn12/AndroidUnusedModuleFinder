"""
package_collector.py

This script is used to find usage of specific package in all the modules that are used in the android project.

"""
from ModuleFinder import _exit
from UnusedModuleFinder import get_declared_modules
from UnusedModuleFinder import get_selected_directory
from os import listdir
from os import path

modules: list[str] = []
search_package: str = ''
excluded_directory = ['res', 'build']


def find_module_directory(module_dir: str) -> str:
    module_parts = module_dir.replace(':', '', 1).split(':')
    m_len = len(module_parts)
    if m_len == 1:
        return f"{get_selected_directory()}/{module_parts[0]}"
    if m_len == 2:
        return f'{get_selected_directory()}/{module_parts[0]}/{module_parts[1]}'
    if m_len == 3:
        return f'{get_selected_directory()}/{module_parts[0]}/{module_parts[1]}/{module_parts[2]}'
    if m_len == 4:
        return f'{get_selected_directory()}/{module_parts[0]}/{module_parts[1]}/{module_parts[2]}/{module_parts[3]}'
    if m_len == 5:
        return f'{get_selected_directory()}/{module_parts[0]}/{module_parts[1]}/{module_parts[2]}/{module_parts[3]}/{module_parts[4]}'
    _exit(f'Max length of module is 5 but {m_len} found')


def find_files(directory: str) -> list[str]:
    all_files = []
    for file in listdir(directory):
        if path.isdir(f'{directory}/{file}') and file not in excluded_directory:
            all_files.extend(find_files(f'{directory}/{file}'))
        else:
            if file.endswith('.kt') or file.endswith('.java'):
                all_files.append(f'{directory}/{file}')
    return all_files


def find_usage(search_files: list[str]) -> list[str]:
    global search_package
    used_in = []
    for file in search_files:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                if search_package in line:
                    used_in.append(file)
                    break
    return used_in


if __name__ == '__main__':
    modules = get_declared_modules()
    if not modules:
        _exit('No modules found in settings.gradle')
    print('[Example, com.tr.xyz.time]')
    search_package = input('Enter package name to search : ')

    if not search_package or search_package.isspace():
        _exit('No search package')
    print(f'{len(modules)} modules found in settings.gradle')
    usage_dict: dict[str, list[str]] = dict()

    for module in modules:
        m_directory = find_module_directory(module)
        files = find_files(m_directory)
        usage = find_usage(files)
        if usage:
            usage_dict[module] = usage

    if usage_dict:
        print(f'{len(usage_dict)} modules use [{search_package}]')
        for m, u in usage_dict.items():
            print(f'{m}')
            for f in u:
                print(f'\t{f}')
    else:
        print(f'No any module uses [{search_package}]')
    _exit('Done')
