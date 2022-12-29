# > ![version](https://www.linux.org.ru/tango/img/general-logo.png) **`_Skypro: sp_diploma_`**

### _ДИПЛОМНАЯ РАБОТА ПО КУРСУ ``ПРОФЕССИЯ PYTHON РАЗРАБОТЧИК``_
---
---
![version](https://www.quasa.io/storage/photos/%D0%A4%D0%BE%D1%82%D0%BE/00%20%D0%9F%D0%BB%D0%B0%D0%BD%207.png)

## Стек IT-разработки

* ![version](https://img.shields.io/badge/Python-v_3.10-informational/?style=social&logo=Python)
* ![version](https://img.shields.io/badge/Django-v_4.0.1-informational/?style=social&logo=Django)
* ![version](https://img.shields.io/badge/PostgreSQL-v_15_alpine-informational/?style=social&logo=Postgresql)
* ![version](https://img.shields.io/badge/Docker_Desktop-v_4.15.0-informational/?style=social&logo=Docker)

#### Приложение ✨Календарь✨ предоставляет возможности для работы со встречами и имеет следующие функционал:

> 1. Вход/регистрация/аутентификация через вк;
>2. Создание целей:<br/>
    - выбор временного интервала цели с отображением количества дней до завершения цели;<br/>
    - выбор категории цели (личные, работа, развитие, спорт и т. п.) с возможностью добавлять/удалять/обновлять категории;<br/>
    - выбор приоритета цели (статичный список minor, major, critical и т. п.);<br/>
    - выбор статуса выполнения цели (в работе, выполнен, просрочен, в архиве);<br/>
>3. Изменение целей:<br/>
    - изменение описания цели;<br/>
    - изменение статуса;<br/>
    - дать возможность менять приоритет и категорию у цели;<br/>
>4. Поиск по названию цели;
>5. Фильтрация по статусу, категории, приоритету, году;
>6. Заметки к целям;
>7. Аккаунт Telegram привязан к аккаунту приложения. Через Telegram получается просматривать все открытые цели пользователя, создавать цели.
###
#### 🏆 Сайт приложения находится по адресу: [skypro-evedrov.ga](http://skypro-evedrov.ga)
#### 🚀 Для перехода к Telegram_bot, созданный при помощи BotFather, необходимо перейти по ссылке: [Todolisting_bot](https://t.me/Todolisting_bot)
___
###
#### Для корректной работы приложения рекомендуется установить Django версии 4.0.1 командой `pip install Django==4.0.1`
###
#### 👋Файл `docker-compose.yaml` содержит контейнер с базой данных Frontend, Postgres, API и BOT, разворачиваемый при наборе команды в терминале команды - `docker-compose up -d`
#### Файл `docker-compose-ci.yaml` для развёртывания приложения на сервере
#### Также содержится файлы *`.env`* и для хранения переменных окружения
####
#### Активация виртуального окружения: `.\venv\Scripts\Activate`
#### Файл requirements.txt служит для установки зависимостей в приложении через команду `pip install -r requirements.txt`
###
#### 📝 Перечень команд, которые могут потребоваться в процессе работы

|Наименование | Команда |
| ------ | ------ |
| Cоздание приложения | python manage.py startapp <name_application>|
| Удаление томов, контейнеров образов, сетей | sudo -S docker system prune -a -f|
| Создание своей миграции | python manage.py makemigrations goals --name create_new_objects --empty |
| Накатить миграции в БД | python manage.py makemigrates |
| Применить все миграции | python manage.py migrate|
| Создание администратора | python manage.py createsuperuser |
| Запуск сервера  | python manage.py runserver |
###
####
##### 👨‍💻Запуск тестов из терминала PyCharm выполняется в следующем порядке:
- перейти в директорию `todolist` командой `cd .\todolist\`
- запуск непосредственно тестов командой `pytest`
#
## ***Исполнитель дипломной работы:***
### ***Ведров Е.А.***