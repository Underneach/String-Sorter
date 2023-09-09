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
            raw_file_paths = input(f'\n{colorama.Fore.LIGHTBLUE_EX}Пути с пробелами должны быть в кавычках ""{colorama.Style.RESET_ALL}\nВведите путь к файлам или папке через пробел: ').split(' ')

            for file_path in raw_file_paths:

                file_path = file_path.strip('"').strip("'").strip()  # Костыль для удаления кавычек в начале и конце строки и пробелов в начале и конце строки

                if file_path:  # Если путь не пустой

                    if not os.path.exists(file_path):
                        print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Путь {file_path} не существует')
                        continue

                    if os.path.isfile(file_path):
                        file_path_list.append(file_path)
                        continue
                    elif os.path.isdir(file_path):
                        file_path_list.append(os.path.join(file_path, file) for file in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, file)))
                        continue
                    else:
                        print(f'[{colorama.Fore.LIGHTGREEN_EX}-{colorama.Style.RESET_ALL}] Путь {file_path} не является файлом или папкой.')
                        continue

            if len(file_path_list) > 0:
                break

    if not file_path_list:
        print("Нет файлов для обработки.")
        sys.exit(1)

    while True:
        raw_search_requests = input('\nВведите запросы через пробел: ').split(' ')
        if raw_search_requests:
            search_requests = [request.strip(' ').strip() for request in raw_search_requests]
            break

    file_size = sum(os.path.getsize(file) for file in file_path_list) / 1048576

    os.system('cls')
    Print_Logo(app_version)
    return file_path_list, search_requests, int(file_size)
