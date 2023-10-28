import re
from concurrent.futures import ThreadPoolExecutor

import colorama


def Write_result(self, file_path: str) -> None:
    def Process_file(self, request: str) -> None:

        try:
            request = re.sub(r'[\\/|:*?"<>]', '_', request.strip())
            file_path = f'{self.app_dir}\\{request}.txt'
            orig_size = len(self.results[request]['extracted_data'])
            sorted_data = list(set(self.results[request]['extracted_data']))
            new_size = len(sorted_data)
            dubles_count = orig_size - new_size

            print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{request}{colorama.Style.RESET_ALL} : {colorama.Fore.LIGHTBLUE_EX}{len(sorted_data)}{colorama.Style.RESET_ALL} строк : {colorama.Fore.LIGHTBLUE_EX}{dubles_count}{colorama.Style.RESET_ALL} дубликатов')

            if len(sorted_data) > 0:
                with open(file=f'{self.app_dir}\\{request}.txt', mode='a', encoding=self.encoding, buffering=4096) as file:
                    file.write('\n'.join(sorted_data) + '\n')

        except Exception as e:
            print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{request}.txt{colorama.Style.RESET_ALL} : Ошибка : {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')

    print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Удаление дубликатов и запись в файлы {colorama.Fore.LIGHTBLUE_EX}{len(self.results)}{colorama.Style.RESET_ALL} запросов')

    try:

        with ThreadPoolExecutor(max_workers=len(self.search_requests)) as executor:
            for request in self.search_requests:
                executor.submit(Process_file, self, request)

            executor.shutdown(wait=True, cancel_futures=False)

    except Exception as e:
        print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Ошибка записи результата: {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')

    self.jobs_list.clear()  # Очищаем список задач
    for request in self.search_requests:
        self.results[request]['extracted_data'].clear()  # Очищаем словарь результатов

    print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{file_path}{colorama.Style.RESET_ALL} : Файл отсортирован')
