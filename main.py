import sys
import re
import os
import colorama
import time


def main(file_path, search_request):
    string_count = 0
    success_count = 0
    with open(file_path, 'r', encoding='utf-8') as file, open('result.txt', 'w', encoding='utf-8') as result_file:
        for line in file:
            string_count += 1
            line = line.strip()
            result = re.search(search_request, line)
            if result:
                success_count += 1
                extracted_data = result.group(1)
                print(f'[{colorama.Fore.LIGHTYELLOW_EX}{string_count}{colorama.Style.RESET_ALL}] {extracted_data}')
                result_file.write(extracted_data + '\n')
    return success_count, string_count


if __name__ == '__main__':

    colorama.init(autoreset=True)
    time_start = time.time()

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
