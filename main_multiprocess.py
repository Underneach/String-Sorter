import sys
import re
import os
import colorama
import time
from multiprocessing import Pool


def process_line(line, search_request):
    result = re.search(search_request, line)
    if result:
        extracted_data = result.group(1)
        return extracted_data
    return None


def main(file_path, search_request):
    string_count = 0
    result_data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with Pool() as pool:
        result_data = pool.starmap(process_line, [(line.strip(), search_request) for line in lines])

    with open('result.txt', 'w', encoding='utf-8') as result_file:
        for i, data in enumerate(result_data):
            if data:
                string_count += 1
                print(f'[{colorama.Fore.LIGHTYELLOW_EX}{string_count}{colorama.Style.RESET_ALL}] {data}')
                result_file.write(data + '\n')

    return string_count, len(lines)


if __name__ == '__main__':
    colorama.init(autoreset=True)

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input('Введите путь к файлу: ')
        while not os.path.exists(file_path):
            file_path = input('Введите путь к файлу: ')

    while True:
        search_request = re.compile(r'[\s\S]{4,5}://[\s\S]*' + input('Введите строку для поиска: ') + r'[\s\S]*/:([\s\S]+:[\s\S]+)')
        if search_request:
            break

    time_start = time.time()

    success_count, string_count = main(file_path, search_request)

    time_end = time.time()

    print("\nВремя выполнения: ", time_end - time_start)
    print("Найдено строк: " + str(success_count) + '/' + str(string_count))
    input('Нажмите Enter для выхода...')
    sys.exit(0)
