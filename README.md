# FastAPI TODO

для запуска перейдите в папку проекта и пропишите:

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload

Открыть Swagger:
http://127.0.0.1:8000/docs

## Настройка PostgreSQL
Необходимо создать PostgreSQL базу данных и указать параметры подключения в .env.
Пример .env:

DB_USER=your_user
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database

## запуск фронта

python3 -m http.server 5500

открыть: 

http://localhost:5500/front/auth.html

## Добавил в проект тесты для проверки работы API, для запуска тестов пропишите:

python3 -m pytest

## Для проверки покрытия тестами кода пропишите:

coverage run -m pytest tests
coverage report

## Для запуска нагрузочного тестирования:

locust
http://127.0.0.1:8089