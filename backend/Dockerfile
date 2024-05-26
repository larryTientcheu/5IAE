FROM ubuntu:latest

WORKDIR /app

EXPOSE 5000
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .

RUN apt-get update -y && apt-get install -y libpq-dev python-dev
RUN apt-get install -y python3 pip

RUN pip install -r requirements.txt

COPY . /app

CMD [ "python", "program.py" ]