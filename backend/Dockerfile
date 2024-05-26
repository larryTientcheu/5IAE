FROM python:3.11-slim

WORKDIR /app
EXPOSE 5005

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y && \
    apt-get install -y libpq-dev build-essential

# Install pip requirements
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
CMD ["python", "program.py"]