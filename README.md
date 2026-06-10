# FastAPI TODO

## Требования

- Docker и Docker Compose — для запуска через Docker
- Python 3.12+ и PostgreSQL — для локального запуска

## Настройка окружения

Создайте файл `.env` в корне проекта:

```
DB_USER=your_user
DB_PASS=your_password
DB_HOST=db
DB_PORT=5432
DB_NAME=your_database
SECRET=your_random_secret_key
```

> `DB_HOST=db` — имя сервиса PostgreSQL в Docker Compose. Для локального запуска без Docker замените на `localhost`.

> `SECRET` — используется для подписи JWT токенов. Сгенерировать можно командой:
> ```bash
> python3 -c "import secrets; print(secrets.token_hex(32))"
> ```

## Запуск через Docker

```bash
docker compose up --build
```

Swagger UI: http://127.0.0.1:8000/docs

Таблицы в базе данных создаются автоматически при первом запуске.

Остановить:
```bash
docker compose down
```

Остановить и удалить данные БД:
```bash
docker compose down -v
```

## Локальный запуск (без Docker)

Измените в `.env` значение `DB_HOST=localhost`, затем:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Запуск фронтенда

```bash
python3 -m http.server 5500
```

Открыть: http://localhost:5500/front/auth.html

## Тесты

```bash
source venv/bin/activate
python3 -m pytest
```

С отчётом о покрытии:

```bash
coverage run -m pytest tests
coverage report
```

## Нагрузочное тестирование

```bash
source venv/bin/activate
locust
```

Открыть: http://127.0.0.1:8089

> Перед нагрузочным тестированием убедитесь, что сервер запущен и в БД есть пользователь `test@test.com` с паролем `12345678`.

## API

| Метод | Путь | Описание |
|-------|------|---------|
| POST | `/auth/register` | Регистрация |
| POST | `/auth/jwt/login` | Вход, получение токена |
| GET | `/tasks/` | Список задач |
| POST | `/tasks/` | Создать задачу |
| GET | `/tasks/search?q=текст` | Поиск по заголовку и описанию |
| GET | `/tasks/top?limit=3` | Топ задач по приоритету |
| GET | `/tasks/{id}` | Получить задачу |
| PUT | `/tasks/{id}` | Обновить задачу |
| DELETE | `/tasks/{id}` | Удалить задачу |
