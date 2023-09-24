import os
import sys

import colorama

from modules.print_logo import Print_Logo


def User_Input(app_version: str) -> (list, int):
    Print_Logo(app_version)

    file_path_list = []
    file_size = 0
    raw_file_paths = ''

    if len(sys.argv) > 1:
        file_path_list = sys.argv[1:]

    else:
        while True:
            # Получаем ввод пользователя и разделяем его на пути с пробелами
            raw_file_paths = input(f'\n{colorama.Fore.LIGHTBLUE_EX}Пути с пробелами должны быть в кавычках ""{colorama.Style.RESET_ALL}\nВведите путь к файлам или папке через пробел: ')

            if not raw_file_paths:
                print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Пути не введены.')
                continue

            raw_file_paths = [path.strip() for path in raw_file_paths.split('"') if path.strip()]

            for raw_path in raw_file_paths:
                if os.path.exists(raw_path):
                    if os.path.isfile(raw_path):
                        file_path_list.append(raw_path)
                    elif os.path.isdir(raw_path):
                        # Добавляем все файлы в указанной директории в список file_path_list
                        file_path_list.extend(os.path.join(raw_path, file) for file in os.listdir(raw_path) if os.path.isfile(os.path.join(raw_path, file)))
                    else:
                        print(f'[{colorama.Fore.LIGHTGREEN_EX}-{colorama.Style.RESET_ALL}] Путь {raw_path} не является файлом или папкой.')
                else:
                    print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Путь {colorama.Fore.LIGHTBLUE_EX}{raw_path}{colorama.Style.RESET_ALL} не существует')

            if len(file_path_list) > 0:
                break
            else:
                if len(raw_file_paths) > 1:
                    print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Не найдено ни одного файла.')

    if not file_path_list:
        print("Нет файлов для обработки.")
        input('Нажмите Enter для выхода...')
        sys.exit(1)

    while True:
        raw_search_requests = input('\nВведите запросы через пробел: ')

        if raw_search_requests:
            search_requests = [request.strip(' ').strip() for request in raw_search_requests.split(' ')]
            break

    file_size = sum(os.path.getsize(file) for file in file_path_list) / 1048576

    file_path_list = list(set(file_path_list))
    search_requests = list(set(search_requests))

    os.system('cls')
    Print_Logo(app_version)
    return file_path_list, search_requests, int(file_size)
