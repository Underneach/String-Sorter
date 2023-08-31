import os
import re
import sys
import time
from multiprocessing import Pool, freeze_support

import colorama

from modules.print_logo import Print_Logo
from modules.read_strings import Read_Strings
from modules.user_input import User_Input


class Sorter:
    def __init__(self, file_path, search_requests):
        self.file_path = file_path
        self.search_request = search_request
        self.result_list = []
        self.search_list = []

    def process_line(self, line, compile_request):
        result = re.search(compile_request, line)
        if result:
            extracted_data = result.group(1)
            return extracted_data
        else:
            return None

    def main(self, file_path, search_requests):
        lines, string_count = Read_Strings(self, self.file_path)
        processor_count = min(max(os.cpu_count() - 1, 1), 61) if os.cpu_count() is not None else 4
        compile_request = re.compile(search_request + '.*:(.+:.+)')

        print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Запуск сортера на {colorama.Fore.LIGHTCYAN_EX}{processor_count}{colorama.Style.RESET_ALL} ядрах')

        try:
            with Pool(processes=processor_count) as pool:
                self.result_list = pool.starmap(self.process_line, [(line.strip(), compile_request) for line in lines])
                pool.close()
                pool.join()

        except KeyboardInterrupt:
            pool.terminate()
            print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Принудительная остановка...')
            input('Нажмите Enter для выхода...')
            pool.terminate()
            sys.exit(-1)

        except Exception as e:
            pool.terminate()
            print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Ошибка: {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')
            input('Нажмите Enter для выхода...')
            sys.exit(-1)

        print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Подсчет результатов')
        for result in self.result_list:
            if result is not None:
                self.search_list.append(result)
        self.search_list = list(set(self.search_list))

        print(f"[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Найдено строк по запросу {colorama.Fore.LIGHTCYAN_EX}{self.search_request}{colorama.Style.RESET_ALL} : {colorama.Fore.LIGHTCYAN_EX}{len(self.search_list)}{colorama.Style.RESET_ALL} / {colorama.Fore.LIGHTCYAN_EX}{string_count}")

        with open(f'{self.search_request}.txt', 'w', encoding='utf-8') as result_file:
            for result in self.search_list:
                result_file.write(f'{result}\n')

        print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Результаты записаны в файл {colorama.Fore.LIGHTCYAN_EX}{self.search_request}.txt{colorama.Style.RESET_ALL}')


if __name__ == '__main__':
    freeze_support()
    colorama.init(autoreset=True)
    Print_Logo()
    file_path, search_request = User_Input()

    time_start = time.time()
    Sorter(file_path, search_request).main(file_path, search_request)
    time_end = time.time()

    print(f"\nВремя выполнения: {colorama.Fore.LIGHTCYAN_EX}{time_end - time_start}")
    input('Нажмите Enter для выхода...')
    sys.exit(0)
