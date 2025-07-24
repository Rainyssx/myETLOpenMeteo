# Используем официальный образ Python
FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Копируем зависимости и исходный код
COPY requirements.txt .
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Команда для запуска ETL-процесса (замените на вашу)
CMD ["python", "main.py"]