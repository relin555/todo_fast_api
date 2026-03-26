# FastAPI TODO

для запуска перейдите в папку проекта и пропишите:

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload

Открыть Swagger:
http://127.0.0.1:8000/docs

запуск фронта

python3 -m http.server 5500

открыть: 

http://localhost:5500/front/auth.html
