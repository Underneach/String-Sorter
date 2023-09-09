import os
import re
import sys
import time
import psutil
import asyncio
import aiofiles
from multiprocessing import Pool, freeze_support

import colorama

from modules.read_strings import Read_Strings
from modules.user_input import User_Input


class Sorter:
    def __init__(self, file_path_list, search_requests):
        self.file_path_list = file_path_list
        self.app_dir = os.getcwd()
        self.processor_count = min(max(psutil.cpu_count(logical=True) - 1, 1), 61) if psutil.cpu_count(logical=True) is not None else 4
        self.memory_count = psutil.virtual_memory().total - psutil.virtual_memory().used - (psutil.virtual_memory().total * 0.1)  # Сделать чтение по чанкам
        self.search_requests = search_requests
        self.results = {}
        for request in search_requests:
            self.results[request] = {'compile_request': re.compile(request + '.*:(.+:.+)'), 'extracted_data': []}

    async def process_file(self, request):
        try:

            sorted_data = list(set(self.results[request]['extracted_data']))
            print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{request}{colorama.Style.RESET_ALL} : {colorama.Fore.LIGHTBLUE_EX}{len(sorted_data)}{colorama.Style.RESET_ALL} строк')
            if len(sorted_data) > 0:
                async with aiofiles.open(f'{self.app_dir}\\{request}.txt', 'w', encoding='utf-8', buffering=4096) as file:
                    await file.write('\n'.join(sorted_data) + '\n')

        except Exception as e:
            print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{request}.txt{colorama.Style.RESET_ALL} : Ошибка: {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')

    def process_line(self, line):
        try:

            for request in self.search_requests:
                result = re.search(self.results[request]['compile_request'], line)
                if result:
                    extracted_data = result.group(1)
                    return request, extracted_data

            return None, None

        except Exception as e:
            print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {line} : Ошибка обработки строки: {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')

    def main(self):
        print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Доступные ресурсы : {colorama.Fore.LIGHTBLUE_EX}{self.processor_count}{colorama.Style.RESET_ALL} ядер : {colorama.Fore.LIGHTBLUE_EX}{round(self.memory_count / 1048576)}{colorama.Style.RESET_ALL} МБ памяти\n')
        print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Запуск сортера')

        for file_path in self.file_path_list:

            if os.path.getsize(file_path) * 4 > self.memory_count:  # Костыль ебать
                print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Файл {colorama.Fore.LIGHTBLUE_EX}{file_path}{colorama.Style.RESET_ALL} слишком большой для обработки на данной машине.')
                continue

            print("")
            print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Сортировка файла {colorama.Fore.LIGHTBLUE_EX}{file_path}')
            lines, string_count = Read_Strings(self, file_path)
            print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Обработка строк')

            try:

                with Pool(processes=self.processor_count) as pool:
                    for request, extracted_data in pool.map(self.process_line, [(line.strip()) for line in lines], chunksize=self.processor_count * 2500):
                        if request and extracted_data:
                            self.results[request]['extracted_data'].append(extracted_data)

            except Exception as e:
                print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{file_path}{colorama.Style.RESET_ALL} : Ошибка пула процессоров: {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')
                input('Нажмите Enter для выхода...')
                sys.exit(1)

            print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Удаление дубликатов и запись в файлы {colorama.Fore.LIGHTBLUE_EX}{len(self.results)}{colorama.Style.RESET_ALL} запросов')

            try:
                asyncio.get_event_loop().run_until_complete(asyncio.gather(*[self.process_file(request) for request in self.results]))
            except Exception as e:
                print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{file_path}{colorama.Style.RESET_ALL} : Ошибка: {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')
                input('Нажмите Enter для выхода...')
                sys.exit(-1)


if __name__ == '__main__':
    freeze_support()
    app_version = '1.3.3'
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
