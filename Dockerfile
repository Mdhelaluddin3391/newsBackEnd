FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1️⃣ copy ONLY requirements.txt first (layer caching ke liye)
COPY requirements.txt .

# 2️⃣ install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 3️⃣ copy rest of project
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
