# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочую директорию в контейнере
WORKDIR /usr/src/app

# Копируем файл зависимостей
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Создаем директорию для кеша и даем права на запись
RUN mkdir -p /usr/src/app/cache && chmod -R 777 /usr/src/app/cache

# Устанавливаем переменную окружения для кеша
ENV TRANSFORMERS_CACHE=/usr/src/app/cache

# Копируем весь код проекта в рабочую директорию
COPY . .

# Указываем команду для запуска бота
CMD ["python", "main.py"]
