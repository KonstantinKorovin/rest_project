FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Добавляем путь к бинарникам, которые ставит pip/poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry
RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /app/

# Настраиваем poetry: не создавать venv и ставить зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Отдельно ставим gunicorn через pip, чтобы он точно был доступен в системе
RUN pip install --no-cache-dir gunicorn

COPY . /app/

EXPOSE 8000

# Запускаем через полный путь к gunicorn на случай проблем с PATH
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
