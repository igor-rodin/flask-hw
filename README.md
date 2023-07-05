# Домашние задания по Flask

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
