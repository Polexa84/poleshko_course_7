FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install django-celery-beat  # Явная установка

# Копируем код проекта
COPY . .

# Создаем пользователя django (для безопасности)
RUN adduser --disabled-password django
USER django

# Команда запуска (будет переопределена в docker-compose.yml)
CMD ["echo", "This is a base image.  Please specify a command in docker-compose.yml"]