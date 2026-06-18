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

При запуске через Docker фронтенд уже доступен на порту 5500 (nginx).

Открыть: http://localhost:5500/front/auth.html

Для локального запуска без Docker (порт 5500 должен быть свободен):

python3 -m http.server 5500

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

Перед нагрузочным тестированием убедитесь, что сервер запущен и в БД зарегистрирован пользователь "test@test.com" с паролем "12345678". Зарегистрировать можно командой:

curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "12345678"}'

## Демонстрация работы сервиса

### Шаг 1 — Запустить проект

docker compose up --build

Подождать пока все 3 контейнера поднимутся (db, app, front).

# Регистрация
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@test.com", "password": "12345678"}'

# Логин — скопировать access_token из ответа
curl -X POST http://localhost:8000/auth/jwt/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@test.com&password=12345678"

# Вставить токен
TOKEN="вставить_токен_сюда"

# Создать задачу
curl -X POST http://localhost:8000/tasks/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Купить молоко", "description": "2 литра", "status": "new", "priority": 3}'

# Получить список задач
curl http://localhost:8000/tasks/ \
  -H "Authorization: Bearer $TOKEN"

# Проверить изменения в БД
docker compose exec db psql -U ${DB_USER} -d ${DB_NAME} -c "SELECT id, title, status, priority FROM tasks;"

### Альтернатива — через браузер (Swagger UI)

Открыть http://127.0.0.1:8000/docs — все эндпоинты доступны прямо в браузере без curl.

## Docker Swarm

Docker Swarm запускает контейнеры в кластере и автоматически перезапускает их при падении.

### Собрать образ приложения

docker build -t todo-fastapi:latest .

### Загрузить переменные окружения и запустить стек

export $(cat .env | xargs)
docker stack deploy -c docker-stack.yml todo


### Проверить статус сервисов

docker stack services todo
docker service ps todo_app
docker service ps todo_db

### Проверить автоперезапуск

# Узнать ID контейнера приложения
docker ps | grep todo_app

# Принудительно остановить контейнер
docker rm -f <container_id>

# Swarm автоматически поднимет новый — проверить
docker service ps todo_app

### Проверить сохранение данных при пересоздании БД

# Остановить сервис БД
docker service scale todo_db=0

# Поднять обратно данные сохранятся через volume
docker service scale todo_db=1

### Остановить стек

docker stack rm todo
docker swarm leave --force

## API


POST "/auth/register" для регистрация
POST "/auth/jwt/login для вход, получение токена
GET "/tasks/" для получения списка задач
POST "/tasks/" создать одну задачу
GET "/tasks/search?q=текст" Поиск по заголовку и описанию
GET "/tasks/top?limit=3" Топ задач по приоритету
GET "/tasks/{id}" Получить задачу
PUT "/tasks/{id}" Обновить задачу
DELETE "/tasks/{id}" Удалить задачу
