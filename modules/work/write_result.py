import sys
import asyncio

import colorama
import aiofiles


def Write_result(self, file_path: str) -> None:

    async def Process_file(self, request: str) -> None:

        try:

            file_path = f'{self.app_dir}\\{request}.txt'
            sorted_data = list(set(self.results[request]['extracted_data']))

            print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{request}{colorama.Style.RESET_ALL} : {colorama.Fore.LIGHTBLUE_EX}{len(sorted_data)}{colorama.Style.RESET_ALL} строк')

            if len(sorted_data) > 0:
                async with aiofiles.open(f'{self.app_dir}\\{request}.txt', 'a', encoding=self.encoding, buffering=4096) as file:
                    await file.write('\n'.join(sorted_data) + '\n')

        except Exception as e:
            print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{request}.txt{colorama.Style.RESET_ALL} : Ошибка : {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')


    async def write_files(self) -> None:
        await asyncio.gather(*[Process_file(self, request) for request in self.search_requests])

    print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Удаление дубликатов и запись в файлы {colorama.Fore.LIGHTBLUE_EX}{len(self.results)}{colorama.Style.RESET_ALL} запросов')

    try:
        asyncio.run(write_files(self))
    except Exception as e:
        print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Ошибка записи результата: {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')

    self.jobs_list.clear()  # Очищаем список задач
    for request in self.search_requests:
        self.results[request]['extracted_data'].clear()  # Очищаем словарь результатов

    print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] {colorama.Fore.LIGHTBLUE_EX}{file_path}{colorama.Style.RESET_ALL} : Файл отсортирован')
