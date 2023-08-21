import asyncio
import os
import re
import sys
import time

import aiofiles
import colorama


async def process_lines(lines, search_request):
    results = []
    for string_count, line in enumerate(lines, start=1):
        line = line.strip()
        result = re.search(search_request, line)
        if result:
            extracted_data = result.group(1)
            print(f'[{colorama.Fore.LIGHTYELLOW_EX}{string_count}{colorama.Style.RESET_ALL}] {extracted_data}')
            results.append(extracted_data)
    return results


async def process_file(file_path, search_request):
    success_count = 0
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
        lines = await file.readlines()

    extracted_data_list = await process_lines(lines, search_request)

    async with aiofiles.open('result.txt', 'w', encoding='utf-8') as result_file:
        for extracted_data in extracted_data_list:
            await result_file.write(extracted_data + '\n')
            success_count += 1

    return success_count, len(lines)


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

    loop = asyncio.get_event_loop()
    success_count, string_count = loop.run_until_complete(process_file(file_path, search_request))
    loop.close()

    time_end = time.time()

    print("\nВремя выполнения: ", time_end - time_start)
    print("Найдено строк: " + str(success_count) + '/' + str(string_count))
    input('Нажмите Enter для выхода...')
    sys.exit(0)
