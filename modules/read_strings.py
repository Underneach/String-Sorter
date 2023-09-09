import sys
import colorama


def Read_Strings(self, file_path: str) -> (list, int):
    print(f'[{colorama.Fore.LIGHTYELLOW_EX}*{colorama.Style.RESET_ALL}] Чтение строк')

    try:
        with open(file_path, 'r', encoding='utf-8', buffering=8192) as file:
            lines = file.readlines()
    except Exception as err:
        print(f'[{colorama.Fore.LIGHTRED_EX}-{colorama.Style.RESET_ALL}] Ошибка чтения файла: {colorama.Fore.LIGHTRED_EX}{err}')
        input('Нажмите Enter для выхода...')
        sys.exit(1)

    string_count = len(lines)
    print(f'[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Style.RESET_ALL}] Найдено строк : {colorama.Fore.LIGHTBLUE_EX}{string_count}')

    return lines, string_count
