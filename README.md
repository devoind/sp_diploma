#ДИПЛОМНАЯ РАБОТА ПО КУРСУ "ПРОФЕССИЯ PYTHON РАЗРАБОТЧИК"
***
***

###Ресурс: http://skypro-evedrov.ga

>*Введение<br/>
Представьте, что вы работаете в Google, в направлении разработки календаря – calendar.google.com.
Ваше приложение "Календарь" предоставляет возможности для работы со встречами, но некоторые конкуренты добавляют
функционал работы с задачами/целями. Поэтому продуктовый менеджер провел анализ и интервью с пользователями и принял
решение создать новый продукт, который позволит работать с целями и отслеживать прогресс по ним.
Продукт как всегда нужно запустить в сжатые сроки, поэтому приняли решение начать параллельно разработку
и проектирование интерфейсов.*


###Предварительные требования к будущему приложению:
1. Вход/регистрация/аутентификация через вк; 
2. Создание целей:

    выбор временного интервала цели с отображением кол-ва дней до завершения цели; 

    выбор категории цели (личные, работа, развитие, спорт и т. п.) с возможностью добавлять/удалять/обновлять категории; 

    выбор приоритета цели (статичный список minor, major, critical и т. п.); 

    выбор статуса выполнения цели (в работе, выполнен, просрочен, в архиве);
3. Изменение целей:

    изменение описания цели;

    изменение статуса; 

    дать возможность менять приоритет и категорию у цели;
4. Удаление цели:

    при удалении цель меняет статус на «в архиве»;
5. Поиск по названию цели;
6. Фильтрация по статусу, категории, приоритету, году; 
7. Выгрузка целей в CSV/JSON;
8. Заметки к целям;
9. Все перечисленный функции должны быть реализованы в мобильном приложении.<br/><br/>
###Ход выполнения работы.
1. ***Работа с БД + Django-admin***<br/>
- создание приложения: установка Django (Django==4.0.1) командой  pip install Django==4.0.1;<br/>
- создание проекта командой: django-admin startproject todolist;<br/>
- добавление файла .gitignore в репозиторий;<br/>
- настройка зависимостей. Создание виртуального окружения. Добавление созданного виртуального окружения в проект.
Активировать виртуальное окружение. Добавление файла requirements.txt (для хранения зависимостей для использования
в проекте) в корень проекта. Установка зависимостей командой: pip install -r requirements.txt;<br/>
- настройка файла конфигурации (файл конфигурации нужен для того, чтобы настраивать работу приложения под разные
окружения (локальное и production) https://github.com/joke2k/django-environ;<br/>
- создание файла .env, в котором следует хранить настройки по умолчанию;<br/>
- настройка файла settings.py;<br/>
- создание первого приложения командой:** python manage.py startapp core;<br/>
- создание кастомной модели пользователя.** В файле core/models.py добавить модель пользователя, которая
наследуется от AbstractUser;<br/>
- настроить подключение к базе данных;<br/>
- установить Postgres;<br/>
- создать миграцию для приложения core командой:** python manage.py makemigrations;<br/> 
- применить все миграции: python manage.py migrate.<br/><br/>

2. ***Deploy***
- создаем Docker-образ (бэкенд "слушает" на порту 8000);<br/>
- для запуска всех сервисов используем Docker Compose (закладывается 3 образа: front, api and postgres);<br/>
- создаем виртуальную машину в "Яндекс.Облако";<br/>
- подключение к виртуальной машине осуществляется по SSH;
- для проверки добавлен пользователь deploy (для обеспечения безопасности целесообразно добавить в группу docker);<br/>
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
- редактирование работы с комментариями.<br/>
- 
python manage.py makemigrations goals --name create_new_objects --empty

6. ***Телеграм-бот***



<br/><br/>***Исполнитель дипломной работы:***<br/>
***Ведров Е.А.***
