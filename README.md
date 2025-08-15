Furniture Shop API

Простой REST API для мебельного магазина (Django REST Framework + PostgreSQL + Docker).
Позволяет просматривать каталог мебели и оформлять заказы.

🛠 Технологии

Backend: Django + Django REST Framework

База данных: PostgreSQL

Контейнеризация: Docker, docker-compose

🚀 Быстрый старт
# 1) (опционально) создайте .env из примера
# cp .env.example .env

# 2) Поднять все сервисы (БД, MailHog, веб)
docker compose up -d --build

# 3) Применить миграции
docker compose run --rm web python manage.py migrate

# 4) (опц.) создать суперпользователя для /admin
docker compose run --rm web python manage.py createsuperuser

# 5) (опц.) наполнить демо-данными
docker compose run --rm web python manage.py shell -c "
from shop.models import Furniture;
Furniture.objects.all().delete();
Furniture.objects.bulk_create([
    Furniture(name='Table A', price=100, category='table'),
    Furniture(name='Chair A', price=50, category='chair'),
    Furniture(name='Sofa A',  price=300, category='sofa'),
]);
print(Furniture.objects.count(), 'items created');
"


API будет доступен на: http://localhost:8000/

Админка: http://localhost:8000/admin/

Почтовый веб-интерфейс (MailHog): http://localhost:8025/

🔐 Переменные окружения

Заполняются через .env (в репозитории есть .env.example).

Ключ	Значение по умолчанию	Описание
DJANGO_SECRET_KEY	change-me	Секретный ключ Django
DEBUG	1	Режим отладки (1/0)
ALLOWED_HOSTS	*	Разрешённые хосты
POSTGRES_DB	furniture	Имя БД
POSTGRES_USER	furniture	Пользователь БД
POSTGRES_PASSWORD	furniture	Пароль БД
POSTGRES_HOST	db	Хост БД (из docker-compose)
POSTGRES_PORT	5432	Порт БД
EMAIL_HOST	mailhog	SMTP хост (MailHog)
EMAIL_PORT	1025	SMTP порт
EMAIL_USE_TLS	0	TLS (0/1)
EMAIL_USE_SSL	0	SSL (0/1)
DEFAULT_FROM_EMAIL	no-reply@furniture.local	Отправитель писем
LOG_LEVEL	INFO	Уровень логирования

В репозиторий коммитим .env.example, а .env добавляем в .gitignore.

📌 Эндпоинты API
📋 Список мебели
GET /api/furniture/


Параметры:

category (опционально): table|chair|sofa|bed|other
Пример: /api/furniture/?category=sofa

🔍 Карточка товара
GET /api/furniture/<id>/


Пример: /api/furniture/1/

📦 Список заказов по email
GET /api/orders/?email=<email>


Пример: /api/orders/?email=user@example.com

🛒 Создание заказа
POST /api/orders/
Content-Type: application/json


Тело запроса:

{
  "email": "user@example.com",
  "items": [
    {"furniture": 1, "quantity": 2},
    {"furniture": 3, "quantity": 1}
  ]
}

🧪 Примеры (curl)
# Список мебели
curl http://localhost:8000/api/furniture/

# Фильтрация по категории
curl "http://localhost:8000/api/furniture/?category=sofa"

# Деталь товара
curl http://localhost:8000/api/furniture/1/

# Заказы по email
curl "http://localhost:8000/api/orders/?email=user@example.com"

# Создание заказа
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
        "email": "user@example.com",
        "items": [
          {"furniture": 1, "quantity": 1},
          {"furniture": 3, "quantity": 1}
        ]
      }'

✉️ Проверка писем (MailHog)

Веб-интерфейс: http://localhost:8025

Письма из приложения не уходят “в интернет”, а попадают в MailHog (удобно для разработки).

После создания заказа откройте http://localhost:8025 — письмо с деталями будет во “Входящих”.

📂 Структура проекта
shop/
  models.py         # модели: Furniture, Order, OrderItem (индексы для category/email)
  serializers.py    # сериалайзеры (отдельные для чтения и создания заказа)
  views.py          # Furniture list/detail; Orders (GET по email, POST создание)
  urls.py           # маршруты приложения

config/
  settings.py       # настройки Django, БД, email, логирование
  urls.py           # подключение /api/
  wsgi.py

Dockerfile
docker-compose.yml
README.md
.env.example

🪵 Логирование

Базовое логирование настроено через LOG_LEVEL (по умолчанию INFO). Логи приложений выводятся в консоль контейнера web.

🧹 Полезные команды
# Логи веб-приложения
docker compose logs -f web

# Перезапуск веба (после изменения env)
docker compose up -d --build web

# Остановка всех сервисов
docker compose down

# Полная очистка с томом БД (осторожно!)
docker compose down -v


Быстрый старт
# 1) (опционально) создайте .env из примера
# cp .env.example .env

# 2) Поднять все сервисы (БД, MailHog, веб)
docker compose up -d --build

# 3) Применить миграции
docker compose run --rm web python manage.py migrate

# 4) (опц.) создать суперпользователя для /admin
docker compose run --rm web python manage.py createsuperuser

# 5) (опц.) наполнить демо-данными
docker compose run --rm web python manage.py shell -c "
from shop.models import Furniture;
Furniture.objects.all().delete();
Furniture.objects.bulk_create([
    Furniture(name='Table A', price=100, category='table'),
    Furniture(name='Chair A', price=50, category='chair'),
    Furniture(name='Sofa A',  price=300, category='sofa'),
]);
print(Furniture.objects.count(), 'items created');
"
API будет доступен на: http://localhost:8000/

Админка: http://localhost:8000/admin/

Почтовый веб-интерфейс (MailHog): http://localhost:8025/


Переменные окружения

Заполняются через .env (в репозитории есть .env.example).

Ключ	Значение по умолчанию	Описание
DJANGO_SECRET_KEY	change-me	Секретный ключ Django
DEBUG	1	Режим отладки (1/0)
ALLOWED_HOSTS	*	Разрешённые хосты
POSTGRES_DB	furniture	Имя БД
POSTGRES_USER	furniture	Пользователь БД
POSTGRES_PASSWORD	furniture	Пароль БД
POSTGRES_HOST	db	Хост БД (из docker-compose)
POSTGRES_PORT	5432	Порт БД
EMAIL_HOST	mailhog	SMTP хост (MailHog)
EMAIL_PORT	1025	SMTP порт
EMAIL_USE_TLS	0	TLS (0/1)
EMAIL_USE_SSL	0	SSL (0/1)
DEFAULT_FROM_EMAIL	no-reply@furniture.local	Отправитель писем
LOG_LEVEL	INFO	Уровень логирования

В репозиторий коммитим .env.example, а .env добавляем в .gitignore.

Эндпоинты API
📋 Список мебели
GET /api/furniture/


Параметры:

category (опционально): table|chair|sofa|bed|other
Пример: /api/furniture/?category=sofa

🔍 Карточка товара
GET /api/furniture/<id>/


Пример: /api/furniture/1/

📦 Список заказов по email
GET /api/orders/?email=<email>


Пример: /api/orders/?email=user@example.com

🛒 Создание заказа
POST /api/orders/
Content-Type: application/json


Тело запроса:

{
  "email": "user@example.com",
  "items": [
    {"furniture": 1, "quantity": 2},
    {"furniture": 3, "quantity": 1}
  ]
}

🧪 Примеры (curl)
# Список мебели
curl http://localhost:8000/api/furniture/

# Фильтрация по категории
curl "http://localhost:8000/api/furniture/?category=sofa"

# Деталь товара
curl http://localhost:8000/api/furniture/1/

# Заказы по email
curl "http://localhost:8000/api/orders/?email=user@example.com"

# Создание заказа
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
        "email": "user@example.com",
        "items": [
          {"furniture": 1, "quantity": 1},
          {"furniture": 3, "quantity": 1}
        ]
      }'

✉️ Проверка писем (MailHog)

Веб-интерфейс: http://localhost:8025

Письма из приложения не уходят “в интернет”, а попадают в MailHog (удобно для разработки).

После создания заказа откройте http://localhost:8025 — письмо с деталями будет во “Входящих”.

📂 Структура проекта
shop/
  models.py         # модели: Furniture, Order, OrderItem (индексы для category/email)
  serializers.py    # сериалайзеры (отдельные для чтения и создания заказа)
  views.py          # Furniture list/detail; Orders (GET по email, POST создание)
  urls.py           # маршруты приложения

config/
  settings.py       # настройки Django, БД, email, логирование
  urls.py           # подключение /api/
  wsgi.py

Dockerfile
docker-compose.yml
README.md
.env.example

🪵 Логирование

Базовое логирование настроено через LOG_LEVEL (по умолчанию INFO). Логи приложений выводятся в консоль контейнера web.

🧹 Полезные команды
# Логи веб-приложения
docker compose logs -f web

# Перезапуск веба (после изменения env)
docker compose up -d --build web

# Остановка всех сервисов
docker compose down

# Полная очистка с томом БД (осторожно!)
docker compose down -v