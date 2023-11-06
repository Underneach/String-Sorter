import os
from multiprocessing import Pool

import tqdm
import psutil
import colorama

from modules.work.process_lines import Process_Lines
from modules.work.get_encoding import Get_encoding


def Sorting(self, file_path: str) -> None:
    self.encoding = Get_encoding(file_path) if self.encoding == 'auto' else self.encoding
    file_size = os.path.getsize(file_path)
    chunk_size = min(max(round((psutil.virtual_memory().total - psutil.virtual_memory().used * 0.75 / 8) if psutil.virtual_memory().total - psutil.virtual_memory().used is not None or 0 else 2097152 / 80), 100000), round(file_size / 80))
    string_count = round(file_size / 80)

    print(f'\n[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Сортировка файла {colorama.Fore.LIGHTBLUE_EX}{file_path}{colorama.Style.RESET_ALL} : {colorama.Fore.LIGHTBLUE_EX}{self.encoding}{colorama.Style.RESET_ALL} : {colorama.Fore.LIGHTBLUE_EX}{round(file_size / 1048576)}{colorama.Style.RESET_ALL} МБ : ~{colorama.Fore.LIGHTBLUE_EX}{string_count} строк')
    print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Чтение файла по {colorama.Fore.LIGHTBLUE_EX}{chunk_size}{colorama.Style.RESET_ALL} строк или {colorama.Fore.LIGHTBLUE_EX}{round(chunk_size * 80 / 1048576)}{colorama.Style.RESET_ALL}{colorama.Style.RESET_ALL} МБ')

    with (open(file=file_path, mode='r', encoding=self.encoding, buffering=4096, errors='ignore') as file, Pool(processes=self.processor_count) as pool, tqdm.tqdm(total=string_count, unit=' Strings', desc=f'[*] Обработка файла', colour='blue', dynamic_ncols=True, smoothing=True, bar_format='{desc} | {bar} |{percentage:3.0f}% | {n_fmt}/{total_fmt} | {rate_fmt}') as progress_bar):
        while True:
            try:
                lines = [next(file) for _ in range(chunk_size)]
            except StopIteration:
                break
            except Exception:
                print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Ошибка сортировки : {colorama.Fore.LIGHTRED_EX}{str(e)}{colorama.Style.RESET_ALL}')

            Process_Lines(self, lines, pool, progress_bar, file_path)
