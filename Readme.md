# Flight booking Chatbot

This is a flight booking chatbot done by:

* Tientcheu Ngaleu Larry Jordan
* Kameni Kameni Olivier
* Ej-Jaidi Aymane

## Project Structure

This project consists of two parts:

* A backend and a Frontend.

### Setting up the Backend

#### Set up the Database

With Postgres running, create a `chatbot` database: (*make sure you have psql installed*)

```bash
createbd chatbot
```

#### Key Pip Dependencies

* [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

* [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

* [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

* [tensorflow](slkdqjsdk)

#### **To run the backend from the root of the project**

* Create a new environment and install all the necessary packages in the requirements.txt file.

 ```bash
python -m pip install -r backend/requirements.txt
 ```

* setup the flask environment with;

 ```bash
set FLASK_APP=program.py
call flask db init
call flask db migrate
call flask db upgrade
 ```

**Note:** If migrations fails, please delete the old migrations files.

* To run the backend, run

 ```bash
python backend/program.py
 ```

### Setting up the Frontend

#### **To run the frontent from the root of the project**

* Create a new environment and install all the necessary packages in the requirements.txt file.

 ```bash
python -m pip install -r frontend/requirements.txt
 ```

* Run the frontend app with

 ```bash
python frontend/app.py
 ```

### Run the contenerized application

* In case you just want to run the whole application to use, you can use the conterized version by running the docker_compose file.

 ```bash
docker compose up
 ```
