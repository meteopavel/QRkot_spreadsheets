# Проект QRkot_spreadseets  (переработать)
Проект QRKot — это сервис для Благотворительного фонда поддержки котиков.

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.

Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

Для управления пользователями используется библиотека FastAPI Users. Транспорт Bearer и стратегия JWT.

## Основные используемые инструменты
* python 3.9
* fastapi
* fastapi-users
* alembic
* uvicorn
* sqlalchemy
* python-dotenv

## Развёртывание проекта на локальном компьютере
1. Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:meteopavel/cat_charity_fund.git
```
2. Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv venv
linux: source env/bin/activate
windows: source venv/Scripts/activate
```
3. Установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Создать файл переменных окружения .env:
```bash
touch .env
```
5. Наполнить файл переменными по образцу .env.example


## Использование
1. Применить миграции:
```bash
alembic upgrade head
```

2. Запустить проект:
```bash
uvicorn app.main:app
```
Команда запустит сервер uvicorn. После этого ресурс станет доступен по
адресу http://127.0.0.1:8000.

## Примеры некоторых запросов API
### /donation/ — POST-запрос на создание нового пожертвования;
Пример запроса:
```json
{
  "full_amount": 0,
  "comment": "string"
}
```
Ожидаемый ответ:
```json
{
  "full_amount": 0,
  "comment": "string",
  "id": 0,
  "create_date": "2019-08-24T14:15:22Z"
}
```

### /users/me — GET-запрос на получение информации о текущем пользователе.
Ожидаемый ответ:
```json
{
  "id": null,
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

3. Полная документация Swagger доступна по адресу:
http://127.0.0.1:8000/swagger

4. Полная документация ReDoc доступна по адресу:
http://127.0.0.1:8000/redoc


## Автор
[Павел Найденов](https://github.com/meteopavel)