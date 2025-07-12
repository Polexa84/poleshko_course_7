# Курсовая работа №7 (DRF)

Инструкция по развертыванию и запуску проекта.

## Предварительные требования

*   Python 3.6+
*   Redis
*   Telegram (для работы с ботом)

## Инструкция по установке

1.  **Клонирование проекта:**

    ```bash
    git clone <URL_вашего_репозитория>
    cd <имя_папки_проекта>
    ```

2.  **Создание и активация виртуального окружения:**

    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```

3.  **Установка зависимостей:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Создание базы данных:**

    Настройте подключение к вашей базе данных (например, PostgreSQL, MySQL, SQLite) в файле `.env`.  Убедитесь, что база данных существует.  Если вы используете SQLite, Django создаст файл базы данных автоматически.

5.  **Миграции базы данных:**

    ```bash
    python manage.py migrate
    ```

6.  **Настройка переменных окружения:**

    *   Скопируйте файл `.env.example` в `.env`:

        ```bash
        cp .env.example .env  # Или скопируйте вручную
        ```

    *   Отредактируйте файл `.env` и внесите необходимые настройки, такие как:
        *   `SECRET_KEY`
        *   `DEBUG`
        *   Настройки базы данных (`DATABASE_URL`, `POSTGRES_USER`, `POSTGRES_PASSWORD` и т.д.)
        *   Токен Telegram бота (`TELEGRAM_BOT_TOKEN`)
        *   И другие переменные, необходимые для вашего приложения.

7.  **Создание суперпользователя:**

    ```bash
    python manage.py createsuperuser  # Или python manage.py csu (если определена команда)
    ```

    Введите имя пользователя, email и пароль для суперпользователя.

8.  **Запуск Redis:**

    Убедитесь, что Redis установлен и запущен:

    ```bash
    redis-server
    ```

    Redis используется для Celery и кеширования.

## Запуск проекта

1.  **Запуск Django development server:**

    ```bash
    python manage.py runserver
    ```

    Откройте браузер и перейдите по адресу `http://127.0.0.1:8000/` (или по адресу, указанному в консоли).

2.  **Запуск Celery Beat (планировщик задач):**

    В новом терминале, активируйте виртуальное окружение (шаг 2) и запустите Celery Beat:

    ```bash
    celery -A config beat -l info -S django
    ```

3.  **Запуск Celery Worker:**

    В другом новом терминале, активируйте виртуальное окружение (шаг 2) и запустите Celery Worker:

    ```bash
    celery -A config worker -l INFO
    ```

## Интеграция с Telegram ботом

1.  **Запустите Telegram бота:**

    После запуска Django development server, Celery Beat и Celery Worker, перейдите в Telegram и найдите своего бота.

2.  **Отправьте команду `/start` боту:**

    ```
    /start
    ```

    Это активирует бота и зарегистрирует пользователя (в зависимости от логики вашего бота).

## CI/CD с GitHub Actions

### 1. Настройка секретов GitHub

*   В репозитории GitHub перейдите в `Settings` -> `Secrets` -> `Actions` и добавьте следующие секреты:
    *   `SSH_KEY`: Содержимое вашего приватного SSH-ключа (для доступа к серверу).
    *   `SSH_USER`: Имя пользователя для подключения к серверу (например, `deployer`).
    *   `SERVER_IP`: IP-адрес вашего сервера.
    *   `DJANGO_SECRET_KEY`: Секретный ключ Django (тот же, что и в `.env`).
    *   `POSTGRES_PASSWORD`: Пароль от базы данных PostgreSQL на сервере (если отличается от локального).
    *   `DEPLOY_DIR`: `/home/deployer/habit_tracker` (путь к директории деплоя на сервере).

### 2. Файл `.github/workflows/deploy.yml`

```yaml
name: Django CI/CD Pipeline

on:
  push:
    branches:
      - main  # или develop_1

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up SSH key
        uses: webfactory/ssh-agent@v0.8.0
        with:
          ssh-private-key: ${{ secrets.SSH_KEY }}

      - name: Add known host
        run: ssh-keyscan ${{ secrets.SERVER_IP }} >> ~/.ssh/known_hosts

      - name: Deploy to server
        run: |
          export RSYNC_RSH="ssh -o StrictHostKeyChecking=no"
          rsync -avz --delete --exclude '__pycache__' . ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }}:${{ secrets.DEPLOY_DIR }}

          ssh ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} << EOF
            cd ${{ secrets.DEPLOY_DIR }}
            python3 -m venv venv
            source venv/bin/activate
            pip install -r requirements.txt
            python manage.py migrate
            python manage.py collectstatic --noinput
            sudo systemctl restart gunicorn  # или ваш сервис
          EOF

**Примечания:**

*   Замените `<URL_вашего_репозитория>` на фактический URL вашего репозитория.
*   Замените `<имя_папки_проекта>` на имя папки вашего проекта.
*   Убедитесь, что Redis работает на порту по умолчанию (6379) или укажите другой порт в настройках.
*   Проверьте логи Celery и Django development server на наличие ошибок.
