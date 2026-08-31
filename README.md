FASTAPI PRACTIC
🚀 Обзор проекта
Этот проект представляет собой бэкенд-сервис для управления задачами, построенный на фреймворке FastAPI. Он разработан с использованием паттерна Unit of Work для эффективного взаимодействия с базой данных (PostgreSQL), а также обеспечивает чистую архитектуру с отделением логики по слоям (роутеры, сервисы, репозитории, схемы).

Ключевые особенности:

FastAPI: Высокопроизводительный фреймворк для создания API.
SQLAlchemy Core/ORM: Асинхронная работа с базой данных PostgreSQL.
Pydantic: Валидация данных и сериализация/десериализация.
Unit of Work: Управление транзакциями базы данных.
Аутентификация/Авторизация: JWT-токены.
DI (Dependency Injection): Чистая архитектура и тестируемость.
🛠️ Технологии
Python: 3.10+
FastAPI: Основной фреймворк.
Uvicorn: ASGI-сервер для запуска приложения.
SQLAlchemy: ORM для работы с PostgreSQL.
Alembic: Инструмент для миграций базы данных.
Pydantic: Валидация данных.
Psycopg2-binary: Драйвер PostgreSQL.
PyJWT: Для работы с JWT-токенами.
Passlib: Для хеширования паролей.
Python-Multipart: Для работы с формами.
python-decouple: Для работы с переменными окружения.
📦 Установка и запуск
Следуй этим шагам, чтобы развернуть проект локально.

1. Клонирование репозитория
git clone <URL_ТВОЕГО_РЕПОЗИТОРИЯ>
cd fast_api_practic
2. Создание и активация виртуального окружения
Рекомендуется использовать виртуальное окружение, чтобы изолировать зависимости проекта.
python -m venv venv
# Для Windows
.\venv\Scripts\activate
# Для macOS/Linux
source venv/bin/activate
3. Установка зависимостей
pip install -r requirements.txt
4. Настройка переменных окружения
Создай файл .env в корневой директории проекта и заполни его необходимыми переменными.
Пример .env:
DATABASE_URL="postgresql+asyncpg://user:password@host:port/database_name"
SECRET_KEY="your-super-secret-jwt-key"
ALGORITHM="HS256" # Алгоритм для JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30 # Время жизни access токена в минутах
REFRESH_TOKEN_EXPIRE_DAYS=7 # Время жизни refresh токена в днях
5. Применение миграций базы данных
После настройки DATABASE_URL, создай базу данных и примени миграции:
alembic upgrade head
6. Запуск приложения
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload.


📄 Документация API (Swagger UI / ReDoc)
После запуска приложения, вы можете получить доступ к интерактивной документации API по следующим адресам:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
Здесь вы найдете все доступные эндпоинты, их параметры, примеры запросов и ответов.

🔑 Аутентификация и Авторизация (Базовый поток)
Регистрация пользователя:
POST /api/v1/users/register
Создайте нового пользователя, отправив username, email и password.
Получение токенов:
POST /api/v1/users/token
Авторизуйтесь, отправив username и password. В ответ получите access_token и refresh_token.
Доступ к защищенным эндпоинтам:
Для доступа к защищенным ручкам, в заголовке запроса Authorization передайте Bearer <access_token>.
Пример: Authorization: Bearer eyJhbGciOiJIUzI1Ni...
Обновление токенов:
POST /api/v1/users/refresh_token
Используйте refresh_token для получения новой пары access_token и refresh_token, когда access_token истек. Передайте refresh_token в заголовке Authorization: Bearer <refresh_token>.
📡 Основные ручки (Эндпоинты)
Ниже представлен список основных групп эндпоинтов. Детальное описание параметров и ответов доступно в Swagger UI/ReDoc.

Пользователи (/api/v1/users)
POST /register: Регистрация нового пользователя.
POST /token: Получение access и refresh токенов.
POST /refresh_token: Обновление access и refresh токенов.
GET /me: Получение информации о текущем авторизованном пользователе (требует JWT-токен).
GET /: Получение списка всех пользователей (только для админов).
GET /{user_id}: Получение пользователя по ID.
PUT /{user_id}: Обновление пользователя по ID.
DELETE /{user_id}: Удаление пользователя по ID.

Доски (/api/v1/boards)
POST /: Создание новой доски.
GET /: Получение списка всех досок.
GET /{board_id}: Получение доски по ID.
PUT /{board_id}: Обновление доски по ID.
DELETE /{board_id}: Удаление доски по ID.

Колонки (/api/v1/columns)
POST /: Создание новой колонки (требует board_id).
GET /: Получение списка всех колонок.
GET /{column_id}: Получение колонки по ID.
PUT /{column_id}: Обновление колонки по ID.
DELETE /{column_id}: Удаление колонки по ID.

Задачи (/api/v1/tasks)
POST /: Создание новой задачи (требует board_id и column_id).
GET /: Получение списка всех задач.
GET /{task_id}: Получение задачи по ID.
PUT /{task_id}: Обновление задачи по ID.
DELETE /{task_id}: Удаление задачи по ID.

Группы (/api/v1/groups)
POST /: Создание новой группы.
GET /: Получение списка всех групп.
GET /{group_id}: Получение группы по ID.
PUT /{group_id}: Обновление группы по ID.
DELETE /{group_id}: Удаление группы по ID.

Спринты (/api/v1/sprints)
POST /: Создание нового спринта (требует board_id).
GET /: Получение списка всех спринтов.
GET /{sprint_id}: Получение спринта по ID.
PUT /{sprint_id}: Обновление спринта по ID.
DELETE /{sprint_id}: Удаление спринта по ID.