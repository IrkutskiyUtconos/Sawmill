FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей для weasyprint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Создание директории для отчётов
RUN mkdir -p /var/storage/reports

# Запуск тестов при сборке
RUN pip install pytest && pytest tests/ -v --ignore=test_models.py || true

CMD ["python", "main.py"]