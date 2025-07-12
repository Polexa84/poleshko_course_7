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

## CI/CD с GitHub Actions и деплой на Ubuntu Server

### 1. Настройка сервера

1.  **Подключитесь к серверу по SSH.**
2.  **Установите необходимые пакеты:**

    ```bash
    sudo apt update
    sudo apt install python3 python3-venv postgresql redis-server nginx gunicorn
    ```

3.  **Создайте пользователя `deployer` (если его нет):**

    ```bash
    sudo adduser deployer
    sudo usermod -aG sudo deployer
    ```

4.  **Настройте PostgreSQL:**

    *   Установите пароль для пользователя `postgres`:

        ```bash
        sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'password';"
        ```

    *   Создайте базу данных `testdb`:

        ```bash
        sudo -u postgres psql -c "CREATE DATABASE testdb;"
        ```

5.  **Создайте директорию для проекта:**

    ```bash
    sudo mkdir /home/deployer/habit_tracker
    sudo chown deployer:deployer /home/deployer/habit_tracker
    ```

6.  **Установите и настройте Gunicorn:**

    *   Создайте файл `/etc/systemd/system/gunicorn.service`:

        ```ini
        [Unit]
        Description=Gunicorn daemon
        After=network.target

        [Service]
        User=deployer
        Group=www-data
        WorkingDirectory=/home/deployer/habit_tracker
        ExecStart=/home/deployer/habit_tracker/venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:8000  # или socket

        [Install]
        WantedBy=multi-user.target
        ```

    *   Включите и запустите Gunicorn:

        ```bash
        sudo systemctl enable gunicorn
        sudo systemctl start gunicorn
        ```

7.  **Установите и настройте Nginx:**

    *   Создайте файл `/etc/nginx/sites-available/habit_tracker`:

        ```nginx
        server {
            listen 80;
            server_name <ваш_домен или IP-адрес>;

            location = /favicon.ico { access_log off; log_not_found off; }
            location /static/ {
                root /home/deployer/habit_tracker;
            }

            location / {
                proxy_pass http://127.0.0.1:8000;  # или путь к сокету, если вы используете сокеты
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
            }
        }
        ```

    *   Создайте символическую ссылку и перезапустите Nginx:

        ```bash
        sudo ln -s /etc/nginx/sites-available/habit_tracker /etc/nginx/sites-enabled/
        sudo nginx -t
        sudo systemctl restart nginx
        ```

8. **Настройка переменных окружения на сервере (Важно!)**

   * Установите `python-dotenv` в виртуальном окружении на сервере:
   ```bash
   pip install python-dotenv
   
**Примечания:**

*   Замените `<URL_вашего_репозитория>` на фактический URL вашего репозитория.
*   Замените `<имя_папки_проекта>` на имя папки вашего проекта.
*   Убедитесь, что Redis работает на порту по умолчанию (6379) или укажите другой порт в настройках.
*   Проверьте логи Celery и Django development server на наличие ошибок.
