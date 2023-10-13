import os
import re
import sys
import time
import asyncio
from multiprocessing import Pool, freeze_support

import tqdm
import psutil
import colorama
import aiofiles

from modules.user_input import User_Input
print(sys.version)

class Sorter:
    def __init__(self, file_path_list, search_requests):
        self.file_path_list = file_path_list
        self.app_dir = os.getcwd()
        self.processor_count = min(max(psutil.cpu_count(logical=True) - 1, 1), 61) if psutil.cpu_count(logical=True) is not None else 4  # Количество ядер - 1
        self.free_memory = psutil.virtual_memory().total - psutil.virtual_memory().used  # Свободная память
        self.memory_count = (self.free_memory * 0.75 / 8) if self.free_memory is not None or 0 else 2097152  # 75% свободной памяти, переводим в байты
        self.search_requests = search_requests
        self.checked_lines = 0
        self.jobs_list = []
        self.results = {}
        for request in search_requests:
            self.results[request] = {'compile_request': re.compile(request + '.*:(.+:.+)'), 'extracted_data': []}

    async def process_file(self, request):
        try:

            sorted_data = list(set(self.results[request]['extracted_data']))
            print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{request}{colorama.Style.RESET_ALL} : {colorama.Fore.LIGHTBLUE_EX}{len(sorted_data)}{colorama.Style.RESET_ALL} строк')
            if len(sorted_data) > 0:
                async with aiofiles.open(f'{self.app_dir}\\{request}.txt', 'a', encoding='utf-8', buffering=4096) as file:
                    await file.write('\n'.join(sorted_data) + '\n')

        except Exception as e:
            print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{request}.txt{colorama.Style.RESET_ALL} : Ошибка: {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')

    def process_lines(self, lines, pool, progress_bar, file_path):
        try:

            self.jobs_list.append(pool.map(self.process_line, [line for line in lines]))
            check_lines = len(lines)
            progress_bar.update(check_lines)
            self.checked_lines += check_lines

        except Exception as e:
            print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{file_path}{colorama.Style.RESET_ALL} : Ошибка пула процессоров: {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')

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
        print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Доступные ресурсы : {colorama.Fore.LIGHTBLUE_EX}{self.processor_count}{colorama.Style.RESET_ALL} ядер : {colorama.Fore.LIGHTBLUE_EX}{round(self.free_memory / 1048576)}{colorama.Style.RESET_ALL} МБ памяти\n')
        print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Запуск сортера')

        for file_path in self.file_path_list:

            file_size = os.path.getsize(file_path)
            chunk_size = min(max(round(self.memory_count / 80), 100000), round(file_size / 80))
            string_count = round(file_size / 80)  # 80 байт на строку

            print(f'\n[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Сортировка файла {colorama.Fore.LIGHTBLUE_EX}{file_path}{colorama.Style.RESET_ALL} : {colorama.Fore.LIGHTBLUE_EX}{round(file_size / 1048576)}{colorama.Style.RESET_ALL} МБ : ~{colorama.Fore.LIGHTBLUE_EX}{string_count} строк')
            print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Чтение файла по {colorama.Fore.LIGHTBLUE_EX}{chunk_size}{colorama.Style.RESET_ALL} строк или {colorama.Fore.LIGHTBLUE_EX}{round(chunk_size * 80 / 1048576)}{colorama.Style.RESET_ALL}{colorama.Style.RESET_ALL} МБ')

            with open(file_path, 'r', encoding='utf-8', buffering=4096) as file, Pool(processes=self.processor_count) as pool, tqdm.tqdm(total=string_count, unit=' Strings', desc=f'[*] Обработка файла', colour='blue', dynamic_ncols=True, smoothing=True, bar_format='{desc} | {bar} |{percentage:3.0f}% | {n_fmt}/{total_fmt} | {rate_fmt}') as progress_bar:
                while True:

                    try:
                        lines = [next(file) for _ in range(chunk_size)]
                    except StopIteration:
                        break

                    self.process_lines(lines, pool, progress_bar, file_path)

            for job in self.jobs_list:

                try:

                    for request, extracted_data in job:
                        if request and extracted_data is not None:
                            self.results[request]['extracted_data'].append(extracted_data)  # Получаем результаты работы процессов

                except Exception as e:
                    print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Ошибка получения данных: {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')

            print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Удаление дубликатов и запись в файлы {colorama.Fore.LIGHTBLUE_EX}{len(self.results)}{colorama.Style.RESET_ALL} запросов')

            try:
                asyncio.get_event_loop().run_until_complete(asyncio.gather(*[self.process_file(request) for request in self.results]))  # асинхронный процесс записи в файлы
            except Exception as e:
                print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{file_path}{colorama.Style.RESET_ALL} : Ошибка: {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')
                input('Нажмите Enter для выхода...')
                sys.exit(-1)

            self.jobs_list.clear()  # Очищаем список задач
            for request in self.search_requests:
                self.results[request]['extracted_data'].clear()  # Очищаем словарь результатов

            print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{file_path}{colorama.Style.RESET_ALL} : {colorama.Fore.LIGHTBLUE_EX}Файл отсортирован{colorama.Style.RESET_ALL}')

        print(f'\n[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Всего отсортировано строк : {colorama.Fore.LIGHTBLUE_EX}{self.checked_lines}{colorama.Style.RESET_ALL}')


if __name__ == '__main__':
    freeze_support()
    app_version = '1.4.0'
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
