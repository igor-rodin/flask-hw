# Домашние задания по Flask

## Урок 5. Знакомство с FastAPI

Папка урока -  ```lesson_5```

```lesson_5/users``` -  Список дел (Задача 6)

```lesson_5/tasks``` -  Список дел (Задача 7)

1. Установка

   ```bash
      pip instal -r requirements
   ```

2. Запуск сервера

   ```bash
      python lesson_5/main.py
   ```

Список пользователей -  по ```url```: <http://127.0.0.1:8000>

## Урок 4. Введение в многозадачность

Папка урока -  ```lesson_4```

Программа для скачивания ресурсов с сзаданных URL адресла ```url_load```.

Вывод справки ```urls_load.py -h```

```bash

   usage: urls_load.py [-h] [-l | -f] [-t TARGET_DIR] [-r {T,I}] [-m {MT,MP,ASYNC}] source [source ...]

   Скачивает содержимое с заданных URL ресурсов

   positional arguments:
   source                Список URL адресов для скачивания.

   options:
   -h, --help            show this help message and exit
   -l, --list            Источнок URL адресов для скачивания - список, передается в аргументах командной строки
   -f, --file            Источнок URL адресов для скачивания - текстовый файл с содержимым со списком URL. Используется по умолчанию.
   -t TARGET_DIR, --target-dir TARGET_DIR
                           Директория для скачивания. По умолчанию используется текущая
   -r {T,I}, --resource-type {T,I}
                           Тип ресурса для скачивниая. ('T' - плейн текст, 'I' - изображеиния). По умолчанию - 'T'
   -m {MT,MP,ASYNC}, --mode {MT,MP,ASYNC}
                           Режим скачивания. ( 'MT' - многопоточный, 'MP' - многопросессорный, 'ASYNC' - асинхронный). По умолчанию
                           используется 'ASYNC'
```

Примеры использовния:

   ```img_urls.txt``` - список ресурсов с картинками

   ```bash
      python lesson_4/urls_load.py 'lesson_4/data/img_urls.txt' -t='img' --resource-type=I -m=MP
      python lesson_4/urls_load.py -l 'https://www.google.ru/' 'https://dev.to/listings'  --target-dir='tmp'
   ```

## Урок 3. Дополнительные возможности Flask

Шаблоны к уроку находятся в папке ```app/templates/lesson-3```

Файлы урока в папке ```app/lesson_3```

1. Установка

   ```bash
      pip instal -r requirements
   ```

2. Создание базы данных и заполнение таблиц со студентами

   ```bash
      flask init-db
      flask fill-students-db
   ```

   Таблицы со студентами и пользователями сайта находятся в одной базе данных ```students.db```

   Список студентов по умолчанию загружается командой ```flask fill-students-db``` из файла ```app/lesson_3/data/students.json```.
   Расположение файла определяется параметром ```app.config['STUDENTS_FILE']```

3. Запуск сервера

   ```bash
      flask run [--debug]
   ```

Задания к уроку -  по ```url```: <http://127.0.0.1:5000/lesson-3/>
