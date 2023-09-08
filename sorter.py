import os
import re
import sys
import time
from multiprocessing import Pool, freeze_support

import colorama

from modules.read_strings import Read_Strings
from modules.user_input import User_Input


class Sorter:
    def __init__(self, file_path_list, search_requests):
        self.file_path_list = file_path_list
        self.app_dir = os.getcwd()
        self.results = {}
        self.search_requests = search_requests
        for request in search_requests:
            self.results[request] = {'compile_request': re.compile(request + '.*:(.+:.+)'), 'extracted_data': []}

    def process_folder(self, request):
        try:
            sorted_data = list(set(self.results[request]['extracted_data']))
            print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTCYAN_EX}{request}{colorama.Style.RESET_ALL} : {colorama.Fore.LIGHTCYAN_EX}{len(sorted_data)}{colorama.Style.RESET_ALL} строк')
            with open(f'{self.app_dir}\\{request}.txt', 'w', encoding='utf-8', buffering=4096) as file:
                file.write('\n'.join(sorted_data) + '\n')

        except Exception as e:
            print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTCYAN_EX}{request}.txt{colorama.Style.RESET_ALL} : Ошибка: {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')

    def process_line(self, line):
        try:

            for request in self.search_requests:
                result = re.search(self.results[request]['compile_request'], line)
                if result:
                    extracted_data = result.group(1)
                    return request, extracted_data

            return None, None

        except Exception as e:
            print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {line} : Ошибка : {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')

    def main(self):
        processor_count = min(max(os.cpu_count() - 1, 1), 61) if os.cpu_count() is not None else 4
        print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Запуск сортера на {colorama.Fore.LIGHTCYAN_EX}{processor_count}{colorama.Style.RESET_ALL} ядрах')

        for file_path in self.file_path_list:
            print("")
            lines, string_count = Read_Strings(self, file_path)
            print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Обработка строк из файла {colorama.Fore.LIGHTCYAN_EX}{file_path}')

            try:

                with Pool(processes=processor_count) as pool:
                    for request, extracted_data in pool.map(self.process_line, [(line.strip()) for line in lines], chunksize=processor_count * 2500):
                        if request and extracted_data:
                            self.results[request]['extracted_data'].append(extracted_data)

            except Exception as e:
                print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTCYAN_EX}{file_path}{colorama.Style.RESET_ALL} : Ошибка : {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')
                input('Нажмите Enter для выхода...')
                sys.exit(1)

            print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTCYAN_EX}{file_path}{colorama.Style.RESET_ALL} : Удаление дубликатов и запись в файлы {colorama.Fore.LIGHTCYAN_EX}{len(self.results)}{colorama.Style.RESET_ALL} запросов')

            try:

                for request in self.results:
                    self.process_folder(request)

            except Exception as e:
                print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTCYAN_EX}{file_path}{colorama.Style.RESET_ALL} : Ошибка: {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')
                input('Нажмите Enter для выхода...')
                sys.exit(-1)


if __name__ == '__main__':
    freeze_support()
    app_version = '1.3.0'
    colorama.init(autoreset=True)
    file_path_list, search_requests, file_size = User_Input(app_version)

    print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Всего файлов : {colorama.Fore.LIGHTCYAN_EX}{len(file_path_list)}{colorama.Style.RESET_ALL} объемом {colorama.Fore.LIGHTCYAN_EX}{file_size}{colorama.Style.RESET_ALL} МБ')
    print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Всего запросов : {colorama.Fore.LIGHTCYAN_EX}{len(search_requests)}{colorama.Style.RESET_ALL}')

    time_start = time.time()
    Sorter(file_path_list, search_requests).main()
    time_end = time.time()

    print(f"\nВремя выполнения: {colorama.Fore.LIGHTCYAN_EX}{time_end - time_start}")
    input(f'Нажмите {colorama.Fore.LIGHTCYAN_EX}Enter{colorama.Style.RESET_ALL} для выхода...')
    sys.exit(0)
