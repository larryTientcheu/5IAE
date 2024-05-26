# Flight booking Chatbot

This is a flight booking chatbot done by:

* Tientcheu Ngaleu Larry Jordan
* Kameni Kameni Olivier
* Ej-Jaidi Aymane

## Project Structure

```bash
.
├── Comprehensive Documentation.docx
├── PFE_23-24_5e.docx
├── PFE_23-24_5e.pdf
├── Readme.md
├── backend
│   ├── Dockerfile
│   ├── ai_model
│   │   ├── __init__.py
│   │   ├── flight_prices_prediction.ipynb
│   │   ├── helpers
│   │   │   ├── __init__.py
│   │   │   ├── airlines_dataframe
│   │   │   ├── airports_dataframe
│   │   │   └── helpers.py
│   │   ├── model.ipynb
│   │   ├── model_eval.ipynb
│   │   └── tmodels
│   │       ├── label_encoders.pkl
│   │       └── nn_model.pkl
│   ├── config.py
│   ├── models.py
│   ├── program.py
│   ├── requirements.txt
│   └── src
│       └── funcs.py
├── frontend
│   ├── chatbot
│   │   ├── airline_prices.csv
│   │   ├── airlines.csv
│   │   ├── airlines_dataframe
│   │   ├── chatbot.ipynb
│   │   ├── chatbot_training_data.json
│   │   └── flights_dataframe
│   ├── docker-compose.yml
│   ├── dockerfile
│   ├── helpers.py
│   ├── program.py
│   ├── requirements.txt
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │       └── scripts.js
│   └── templates
│       └── index.html
├── ~$mprehensive Documentation.docx
└── ~WRL0336.tmp
```

## HOW TO RUN

### With Docker

#### From DockerHub

1. Pull the image from Dockerhub using ``

2. Run the image using ``

3. Access the chatbot using `http://localhost:5000`

#### Build the docker image

1. Create an environment file called `.env.docker`.

    * The `.env.docker` file should have a key called `DATABASE_URI` . This is the connection string to the database. For example; the .env file could have `DATABASE_URI=postgresql://postgres:grimm@host.docker.internal:5432/chatbot`. This means; Using `postgresql`, connect to a database called `chatbot` on `host.docker.internal:5432`  with user `postgres`  and password `grimm`

2. From the root of the project, run `docker-compose up --build`

3. Access the chatbot using `http://localhost:5000`

### From source

This project consists of two parts:

* A backend and a Frontend.

### Setting up the Backend

#### Prerequisites

1. Create an environment file called `.env`

   * The `.env` file should have a key called `DATABASE_URI` . This is the connection string to the database. For example; the .env file could have `DATABASE_URI=postgresql://postgres:grimm@localhost:5432/chatbot`. This means; Using `postgresql`, connect to a database called `chatbot` on `localhost:5432`  with user `postgres`  and password `grimm`

2. Make sure the folder helpers contains `airlines_dataframe` , and `airports_dataframe`.

3. The folder tmodel should contain the saved encoders and the saved model after training`label_encoders.pkl & nn_model.pkl`

#### Set up the Database

With Postgres running, create a `chatbot` database: (*make sure you have psql installed*)

```bash
createbd chatbot
```

* The database can also be created manually using the `pgAdmin Dashboard`.

#### Key Pip Dependencies

* [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

* [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

* [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

* [tensorflow]()

* scikit-learn

#### **To run the backend from the root of the project**

* Create a new environment and install all the necessary packages in the requirements.txt file.
  
  ```bash
  python -m pip install -r backend/requirements.txt
  ```

**Note:** If migrations fails, please delete the old migrations files.

* To run the backend, run
  
  ```bash
  python backend/program.py
  ```
  
  * The backend runs on

    ```bash
    http://localhost:50005
    ```

### Setting up the Frontend

#### Prerequisites

1. In the folder frontend/chatbot, the datasets `airlines.csv & airline_prices.csv` must be present.

2. After training the chatbot in chatbot.ipynb, a file called flights_dataframe is produced. This is the main data set for the conversational logic of the chatbot.

#### **To run the frontent from the root of the project**

* Create a new environment and install all the necessary packages in the requirements.txt file.
  
  ```bash
  python -m pip install -r frontend/requirements.txt
  ```

* From the root of the project, run the frontend app with
  
  ```bash
  python frontend/app.py
  ```
  
  * The frontend runs on

    ```bash
    http://localhost:5000
    ```
