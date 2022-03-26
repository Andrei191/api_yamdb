# Проект YaMDb

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «изобразительное искусство» или «Ювелирка»).

## Как запустить проект: 

**Клонировать репозиторий и перейти в него в командной строке:**

cd api_yamdb 

**Cоздать виртуальное окружение:**

python -m venv venv (Windows)
python3 -m venv venv (Linux)

**Активировать виртуальное окружение:**

source venv/Scripts/activate (Windows)
source venv/bin/activate  (Linux)

**Установить зависимости из файла requirements.txt:**

python3 -m pip install --upgrade pip 
pip install -r requirements.txt 

**Выполнить миграции:**

python3 manage.py migrate 

**Запустить проект:**

python3 manage.py runserver

## API для проекта YaMDb

Просле запуска проекта, по адресу http://127.0.0.1:8000/redoc/ будет доступна документация для API YaMDb. Там есть и примеры запросов к API.

## импорт данных из CSV-фалов в БД

### Windows

**Скачать программу sqlite3**

https://www.sqlite.org/download.htm

**Создать <file_sh>**

#!/bin/bash

echo -e ".separator \",\"\n.mode csv\n.import  --skip 1 <file_csv> <db_table_name>" | ./sqlite3.exe db.sqlite3

**Запустить <file_sh>**

chmod a+x ./<file_sh> (при импорте первой таблицы)
./<file_sh> (последующие запуски импортов таблиц)

### Linux

**Установить программу sqlite3**

pip install pysqlite3

**Cоздать <file_sh>**

#!/bin/bash

echo -e ".separator \",\"\n.mode csv\n.import  --skip 1 <file_csv> <db_table_name>" | ./sqlite3 db.sqlite3

**Запустить <file_sh>**

chmod a+x ./<file_sh> (при импорте первой таблицы)
./<file_sh> (последующие запуски импортов таблиц)
