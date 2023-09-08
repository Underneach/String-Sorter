import os
import sys

from modules.print_logo import Print_Logo


def User_Input(app_version: str) -> (list, int):
    Print_Logo(app_version)

    file_path_list = []
    file_size = 0
    file_path = ''

    if len(sys.argv) > 1:
        file_path_list = sys.argv[1:]
    else:
        while not os.path.exists(file_path):
            file_path = input('Введите путь к файлу или папке: ')
            if os.path.isfile(file_path):
                file_path_list = [file_path]
                break
            if os.path.isdir(file_path):
                file_path_list = [os.path.join(file_path, file) for file in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, file))]
                break

    if not file_path_list:
        print("Нет файлов для обработки.")
        sys.exit(1)

    while True:
        raw_search_requests = input('Введите запросы через пробел: ').split(' ')
        if raw_search_requests:
            search_requests = [request.strip(' ').strip() for request in raw_search_requests]
            break

    file_size = sum(os.path.getsize(file) for file in file_path_list) / 1048576

    os.system('cls')
    Print_Logo(app_version)
    return file_path_list, search_requests, int(file_size)
