ДИПЛОМНАЯ РАБОТА ПО КУРСУ "ПРОФЕССИЯ PYTHON РАЗРАБОТЧИК"
##Skypro: sp_diploma
***
***

Ресурс: http://skypro-evedrov.ga

Cтек технологий
>Python 3.10, Django 4.0.1, Postgres, Docker, Docker Compose

<br/><br/>
>*Введение<br/>
Представьте, что вы работаете в Google, в направлении разработки календаря – calendar.google.com.
Ваше приложение "Календарь" предоставляет возможности для работы со встречами, но некоторые конкуренты добавляют
функционал работы с задачами/целями. Поэтому продуктовый менеджер провел анализ и интервью с пользователями и принял
решение создать новый продукт, который позволит работать с целями и отслеживать прогресс по ним.
Продукт, как всегда, нужно запустить в сжатые сроки, поэтому приняли решение начать параллельно разработку
и проектирование интерфейсов.*


Требования к будущему приложению:
1. Вход/регистрация/аутентификация через вк; 
2. Создание целей:<br/>
выбор временного интервала цели с отображением кол-ва дней до завершения цели;<br/> 
выбор категории цели (личные, работа, развитие, спорт и т. п.) с возможностью добавлять/удалять/обновлять категории;<br/> 
выбор приоритета цели (статичный список minor, major, critical и т. п.); <br/>
выбор статуса выполнения цели (в работе, выполнен, просрочен, в архиве);<br/>
3. Изменение целей:<br/> 
изменение описания цели;<br/>
изменение статуса; <br/>
дать возможность менять приоритет и категорию у цели;
4. Удаление цели:<br/>
при удалении цель меняет статус на «в архиве»;<br/>
5. Поиск по названию цели;<br/>
6. Фильтрация по статусу, категории, приоритету, году;<br/> 
7. Выгрузка целей в CSV/JSON;<br/>
8. Заметки к целям;<br/>
9. Все перечисленный функции должны быть реализованы в мобильном приложении.<br/><br/>

>Перечень команд, которые могут потребоваться в процессе работы:- клонирование репозитория
- создать виртуальное окружение ................ python -m venv venv
- активировать его ......................................... venv/Scripts\activate.bat
- установку зависимостей ............................. pip install -r requirements.txt
- перейти в папку todolist .............................. cd todolist
- cоздайте файл командой ........................... .env
- заполнить файл .env переменными окружения в соответствии с файлом .env.example
- накатить миграции в БД ............................ python manage.py makemigrates
- создать администратора ........................... python manage.py createsuperuser
- запустить сервер ....................................... python manage.py runserver
- перейти в браузере в админ-панель по адресу 127.0.0.1:8000/admin/
- удаление неиспользуемых контейнеров.. sudo -S docker system prune -a -f
- создание своей миграции.......................... python manage.py makemigrations goals --name create_new_objects --empty


Ход выполнения работы.
1. ***Работа с БД + Django-admin***<br/>
- установка Django (Django==4.0.1) командой  _**pip install Django==4.0.1**_;<br/>
- создание проекта - _**django-admin startproject todolist**_;<br/>
- добавление файла .gitignore в репозиторий;<br/>
- установка зависимостей - _**pip install -r requirements.txt**_;<br/>
- настройка файла конфигурации - **https://github.com/joke2k/django-environ;<br/>**
- создание файла .env;<br/>
- настройка файла settings.py;<br/>
- создание первого приложения - _**python manage.py startapp core**_;<br/>
- создание кастомной модели пользователя;<br/>
- создать миграцию - _**python manage.py makemigrations**_;<br/> 
- применить все миграции - _**python manage.py migrate**_.<br/><br/>

2. ***Deploy***
- создаем Docker-образ (бэкенд "слушает" на порту 8000);<br/>
- для запуска всех сервисов используем Docker Compose (закладывается 3 образа: front, api and postgres);<br/>
- создаем виртуальную машину в "Яндекс.Облако";<br/>
- подключение к виртуальной машине осуществляется по SSH;
- при помощи приложения GitHub Actions осуществляется автоматическая сборка Docker Compose и добавление на созданный
репозиторий в Docker Hub и на виртуальную машину;<br/><br/>
3. ***Аутентификация и авторизация***<br/>
- для написания API используется Django REST Framework(DRF);<br/>
- добавлен файл serializers.py в приложение core;<br/>
- для авторизации используется стандартная библиотека django.contrib.auth;<br/>
- осуществлено получение/обновление пользователя, а также смена пароля;<br/>
- добавлена поддержка входа через социальную сеть VK.<br/><br/>
4. ***Вебинтерфейс по работе с целями***<br/>
- создаем приложение python manage.py startapp goals;<br/>
- добавляем функционал категорий;<br/>
- добавляем функционал целей;<br/>
- добавляем функционал комментариев<br/><br/>
5. ***Шеринг доски***
- добавление новых моделей;<br/>
- добавление методов для работы с досками (POST, DELETE, GET, PUT);<br/>
- редактирование работы с категориями;<br/>
- редактирование работы с целями;<br/>
- редактирование работы с комментариями.<br/><br/>

7. ***Телеграм-бот*** - в работе


<br/><br/>***Исполнитель дипломной работы:***<br/>
***Ведров Е.А.***

