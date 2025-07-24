FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВСЕ файлы из текущей директории (кроме указанных в .dockerignore)
COPY . .

CMD ["python", "main.py"]  # Убедитесь, что main.py — это ваш главный файл