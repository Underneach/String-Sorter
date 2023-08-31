import os
import re
import sys


def User_Input() -> (str, list):
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "test_strings.txt"  # input('Введите путь к файлу: ')
        while not os.path.exists(file_path):
            file_path = input('Введите путь к файлу: ')

    while True:
        search_request = 'github'  # input('Введите строку для поиска: ')
        if search_request:
            break

    return file_path, search_request
