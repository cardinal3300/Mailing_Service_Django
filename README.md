# Mailing_Service_Django

---

## Описание проекта
Проект представляет собой веб-приложение для управления рассылками электронной почты.  
Позволяет создавать и редактировать сообщения, добавлять получателей, создавать рассылки и отправлять их вручную через веб-интерфейс или автоматически.  
В проекте реализована аутентификация пользователей и управление правами доступа.

---

## Структура проекта

```bash
    mailing_service_Django/
    ├─ config/                 # Основные настройки проекта Django
    ├─ mailing/                # Приложение рассылок
    │  ├─ management/
    │  ├─ migrations/
    │  ├─ templates/
    │  ├─ admin.py
    │  ├─ forms.py
    │  ├─ models.py
    │  ├─ services.py
    │  ├─ urls.py
    │  ├─ views.py
    ├─ static/                 # Bootstrap
    ├─ templates/              # Базовый шаблон
    │      ├─ base.html  
    ├─ users/                  # Приложение пользователей
    │    ├─ management/
    │    ├─ migrations/
    │    ├─ templatess/
    │    ├─ admin.py
    │    ├─ models.py
    ├─ .env.semple
    ├─ README.md
    ├─ manage.py               # Выполнение административных задач
    ├─ .flake8
    ├─ requirements.txt
```

---

## Технологии
- Python 3.14
- Django 5.2
- PostgreSQL
- Redis (для кеширования)
- Bootstrap 5 (для фронтенда)
- psycopg2 (для работы с PostgreSQL)

---

## Установка и запуск
1. Клонировать репозиторий SSH:
   ```bash
   git clone git@github.com:cardinal3300/Mailing_Service_Django.git
   
2. Клонировать репозиторий HTTPS:
    ```bash
   git clone https://github.com/cardinal3300/Mailing_Service_Django.git
   
3. Установить зависимости:
    ```bash
   pip install -r requirements.txt
   
4. Выполнить миграции:
    ```bash
    python manage.py migrate


5. Создать суперпользователя:
    ```bash
    python manage.py createsuperuser

6. Запустить сервер разработки:
    ```bash
    python manage.py runserver   
       
---

## Функционал

- Управление получателями (CRUD)

- Управление сообщениями (CRUD)

- Управление рассылками (CRUD)

- Отправка по требованию через веб-интерфейс и Cli 

- Отслеживание попыток рассылки (успешные и с ошибками)

- Аутентификация пользователей и разграничение доступа

- Использование Redis для кеширования

---

## GitFlow

- Основная ветка: main

- Разработки ветка: develop

- Для новых фич создаются ветки feature/<название>

- После завершения работы ветку feature/<название> сливают в develop через Pull Request

---
