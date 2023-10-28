import os
import sys

import colorama

from modules.print_logo import Print_Logo


def User_Input(app_version: str) -> (list, int):
    Print_Logo(app_version)

    file_path_list = []
    file_size = 0
    raw_file_paths = ''
    file_path_list = ['@urlcloud FREE.txt']
    search_requests = ['google', 'twitter']
    '''
    if len(sys.argv) > 1:
        file_path_list = sys.argv[1:]

    else:
        while True:
            raw_file_paths = input(f'\n{colorama.Fore.LIGHTBLUE_EX}Пути с пробелами должны быть в кавычках ""{colorama.Style.RESET_ALL}\nВведите путь к файлам или папке через пробел: ')

            if not raw_file_paths:
                print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Пути не введены.')
                continue

            def recursive_zalupa(path):
                if os.path.exists(path):
                    if os.path.isfile(path):
                        file_path_list.append(path)
                    elif os.path.isdir(path):
                        for file in os.listdir(path):
                            file_path = os.path.join(path, file)
                            recursive_zalupa(file_path)
                    else:
                        print(f'[{colorama.Fore.LIGHTGREEN_EX}-{colorama.Style.RESET_ALL}] Путь {path} не является файлом или папкой.')
                else:
                    print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Путь {colorama.Fore.LIGHTBLUE_EX}{path}{colorama.Style.RESET_ALL} не существует')

            file_paths = [path.strip() for path in raw_file_paths.split('"') if path.strip()]
            file_path_list = []

            for path in file_paths:
                recursive_zalupa(path)

            if len(file_path_list) > 0:
                break
            else:
                print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Не найдено ни одного файла или папки')

    if not file_path_list:
        print("Нет файлов для обработки.")
        input('Нажмите Enter для выхода...')
        sys.exit(1)

    while True:
        raw_search_requests = input('\nВведите запросы через пробел: ')

        if raw_search_requests:
            search_requests = [request.strip(' ').strip() for request in raw_search_requests.split(' ')]
            break
    '''
    file_size = sum(os.path.getsize(file) for file in file_path_list) / 1048576

    file_path_list = list(set(file_path_list))
    search_requests = list(set(search_requests))

    os.system('cls')
    Print_Logo(app_version)
    return file_path_list, search_requests, int(file_size)
