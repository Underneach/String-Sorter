# String-Sorter
Сортер url:log:pass строк из файла

    Поиск по регулярному выражению
    Запись найденных строк в файл result.txt
    Возомжность запуск сортировки файла перетягиванием на скрипт


## Все тесты проводились на одном пк ( 6 ядер / 12 потоков / 16 Гб RAM) с одним файлом в 13266511 строк

### Sync (main.py) - Дефолт цикл For
![image](https://github.com/Underneach/String-Sorter/assets/137613889/c449dd73-bfad-4d7e-907d-35c0bbf39dbf)

### Async (main_async.py) - Асинхронный сортинг
![image](https://github.com/Underneach/String-Sorter/assets/137613889/a11b78ef-9763-4402-a653-d1bb8145188b)

### Multiprocessing - Распределение сортинга по всем ядрам процессора (Рекомендуется)
![image](https://github.com/Underneach/String-Sorter/assets/137613889/f4a17206-6fcd-4632-8b1c-a31726aa6314)
