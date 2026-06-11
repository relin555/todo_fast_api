# FastAPI TODO

######################################################################################
# ОБЯЗАТЕЛЬНО ПРОЧИТАЙТЕ ИНСТРУКЦИИ ПЕРЕД ЗАПУСКОМ                                   #
# И ПЕРЕД КАЖДЫМ ЗАПУСКАМ BASH команды проверь что стоит окружение venv а не ".venv" #
# ОСОБЕННО ПЕРЕД ОТКРЫТИЕМ НОВОГО ТЕРМИНАЛА                                          #    
# АКТИВАЦИЯ ПРАВИЛЬНОГО venv: source venv/bin/activate                               #
######################################################################################


## Требования

- Docker и Docker Compose — для запуска через Docker
- Python 3.12+ и PostgreSQL — для локального запуска

## Настройка окружения

Создайте файл ".env" в корне проекта:

DB_USER=your_user
DB_PASS=your_password
DB_HOST=db
DB_PORT=5432
DB_NAME=your_database
SECRET=your_random_secret_key

"DB_HOST=db"  имя сервиса PostgreSQL в Docker Compose. Для локального запуска без Docker замените на "localhost".

"SECRET" используется для подписи JWT токенов. Сгенерировать можно командой:
    python3 -c "import secrets; print(secrets.token_hex(32))"

## Запуск через Docker

docker compose up --build

Swagger UI: http://127.0.0.1:8000/docs

Таблицы в базе данных создаются автоматически при первом запуске.

Остановить:

docker compose down

Остановить и удалить данные БД:
docker compose down -v

## Локальный запуск без Docker

Измените в ".env" значение "DB_HOST=localhost", затем:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

## Запуск фронтенда

python3 -m http.server 5500


Открыть: http://localhost:5500/front/auth.html

## что бы запустить тесты введите команды:

source venv/bin/activate
python3 -m pytest


отчет о покрытии :

coverage run -m pytest tests
coverage report

## Нагрузочное тестирование

source venv/bin/activate
locust

Открыть: http://127.0.0.1:8089

Перед нагрузочным тестированием убедитесь, что сервер запущен и в БД есть пользователь "test@test.com" с паролем "12345678" в бд я его уже зарегестрировал.

## API


POST "/auth/register" для регистрация
POST "/auth/jwt/login для вход, получение токена
GET "/tasks/" для создания списка задач
POST "/tasks/" создать одну задачу
GET "/tasks/search?q=текст" Поиск по заголовку и описанию
GET "/tasks/top?limit=3" Топ задач по приоритету
GET "/tasks/{id}" Получить задачу
PUT "/tasks/{id}" Обновить задачу
DELETE "/tasks/{id}" Удалить задачу
