import os
import re
import sys
import time
from multiprocessing import freeze_support

import psutil
import colorama

from modules.user_input import User_Input
from modules.work.write_result import Write_result
from modules.work.sort_lines import Sorting
from modules.work.get_result import Get_result


class Sorter:
    def __init__(self, file_path_list, search_requests):
        self.file_path_list = file_path_list
        self.search_requests = search_requests
        self.invalid_pattern = r'.{201,}|UNKOWN'
        self.app_dir = os.getcwd()
        self.processor_count = min(max(psutil.cpu_count(logical=True) - 1, 1), 61) if psutil.cpu_count(logical=True) is not None else 4  # Количество ядер - 1
        self.checked_lines = 0
        self.invalid_lines = 0
        self.encoding = None
        self.chunk_size = None
        self.jobs_list = []
        self.results = {}
        for request in search_requests:
            self.results[request] = {'compile_request': re.compile(r'.*' + request + r'.*:(.+:.+)'), 'extracted_data': []}

    def main(self) -> None:

        print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Доступные ресурсы : {colorama.Fore.LIGHTBLUE_EX}{self.processor_count}/{self.processor_count + 1}{colorama.Style.RESET_ALL} ядер : {colorama.Fore.LIGHTBLUE_EX}{round((psutil.virtual_memory().total - psutil.virtual_memory().used) / 1048576)}/{round(psutil.virtual_memory().total / 1048576)}{colorama.Style.RESET_ALL} МБ памяти\n')
        print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Запуск сортера...')

        for file_path in self.file_path_list:

            Sorting(self, file_path)

            Get_result(self)

            Write_result(self, file_path)

        print(f'\n\n\n[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Всего отсортировано строк : {colorama.Fore.LIGHTBLUE_EX}{self.checked_lines}{colorama.Style.RESET_ALL}')
        print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Всего невалидных строк : {colorama.Fore.LIGHTBLUE_EX}{self.invalid_lines}{colorama.Style.RESET_ALL}\n\n\n')


if __name__ == '__main__':
    freeze_support()
    app_version = '1.5.0'
    colorama.init(autoreset=True)
    file_path_list, search_requests, file_size = User_Input(app_version)

    print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Всего файлов : {colorama.Fore.LIGHTBLUE_EX}{len(file_path_list)}{colorama.Style.RESET_ALL} объемом {colorama.Fore.LIGHTBLUE_EX}{file_size}{colorama.Style.RESET_ALL} МБ')
    print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Всего запросов : {colorama.Fore.LIGHTBLUE_EX}{len(search_requests)}{colorama.Style.RESET_ALL}')

    time_start = time.time()
    Sorter(file_path_list, search_requests).main()
    time_end = time.time()

    print(f"\nВремя выполнения: {colorama.Fore.LIGHTBLUE_EX}{time_end - time_start}")
    input(f'Нажмите {colorama.Fore.LIGHTBLUE_EX}Enter{colorama.Style.RESET_ALL} для выхода...')
    sys.exit(0)