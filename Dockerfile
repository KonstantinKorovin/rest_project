FROM python:3.12-slim

# Настройки Python (не создавать .pyc, не буферизовать вывод)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем системные зависимости и Poetry
RUN apt-get update && apt-get install -y curl build-essential && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock /app/

# Отключаем создание venv и ставим зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем остальной код
COPY . /app/

# Запуск через Gunicorn
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
