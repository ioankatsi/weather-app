## General

This is my solution for the [NeuroPublic's backend assignment](https://github.com/ioankatsi/weather-app/blob/dev/np_python_assignment.pdf).

I used [FastAPI](https://fastapi.tiangolo.com/) for implementing the task. As data storage I opted for postgesql.

Mainly the project structure is discussed in the section bellow.
A simplified API documentation can be found on `http://localhost:8000/docs#/`, when the server is running.

## How to run the Project

To run the containerized service,
you can find **Dockerfile** and two docker-compose files [**docker-compose-main.yaml**, **docker-compose-test.yaml**] on the root directory.

- **docker-compose-main.yaml**
  - You can use this file to run the full containerized service.
- **docker-compose-test.yaml**
  - You can use this file to run the tests.

To start the main app, you can do so by:

```bash
docker-compose -f docker-compose-main.yaml up --build
```

To stop the main app, you can do so by:

```bash
docker-compose -f docker-compose-main.yaml down
```

**WARNING**

If postgresql is running as service on your local machine, should be stopped before deploying the containerized app.
You could check by:

```bash
sudo service postgresql status
```

**P.S** I do not use `--detatch` on the docker-compose so to be able to check that everything is working fine through the logging.

##### Making requests

By default I add some fixtures while setting up the DB.

A user is already registered in the DB and you can use this one in order to authenticate. Of course you can create new ones by using /register endpoint.

The credentials in order to authenticate are:

```
email: testuser@example.com
password: testpassword
```

##### Making requests

You can use OpenAPI, provided by FastApi. You can access that on `http://localhost:8000/docs`

As a first steps authorize youself by using Authorization button on the upper left of Swagger's screeen and then you can proceed with the testing.

##### Running tests

For the tests I built another containerized service, so to be alike the web app environment.

To run the tests, you can do so by:

```bash
docker-compose -f docker-compose-test.yml up
```

To exit the containerized service, you can do so by:

```bash
docker-compose -f docker-compose-test.yml down
```

**WARNING**

If postgresql is running as service on your local machine, should be stopped before deploying the containerized app.
You could check by:

```bash
sudo service postgresql status
```

and stop it by:

```bash
sudo service postgresql stop
```

## Project structure

The project consists of these directories :

- alembic (contains db migrations)
- api (contains the API router logic)
- auth (contains basic auth implementation)
- core (contains basic configuration for db)
- db (contains db connection logic)
- models (contains the db models)
- schemas (Data validation & sanity checks)
- services (Contains entpoints logic)
- tests (contains basic testing implementation)
- bin (contains bash scripts)

## Sanity Check & Data Validation

I have implemented basic data validity and sanity checks in our API. This ensures that all input data is thoroughly validated and meets predefined criteria before processing. These checks enhance the reliability and accuracy of the data managed by the API.

## Logging

I implemented a very simple logging mechaninsm mostly to track errors.
Logging is essential on a Production level service / web-app
It provides visibility into how the applications is running on each of the various infrastructure components.
Log data contains information such as out of memory exception or query & DB errors.
This is very helpful information that will help us identify the “why” behind a problem either that a user has brought to our attention or that we have uncovered.

The logs reside in `/logs` folder. You should expect to see stored logs only if an exception/error took place.

## Testing and Coverage

Basic tests have been created for most of the endpoints in order to test their functionality.
I also made a coverage report which can be run as

```
docker-compose -f docker-compose-test.yml up
```

The result will be 77% coverage.

```text
Name                              Stmts   Miss  Cover   Missing
============================== 13 passed in 1.69s ==============================
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
app/core/__init__.py                  0      0   100%
app/core/config.py                    9      9     0%   1-16
app/core/log_conf.py                  7      0   100%
app/db/__init__.py                    0      0   100%
app/db/base.py                        2      0   100%
app/db/session.py                     5      5     0%   1-6
app/main.py                          52     52     0%   3-79
app/models/station.py                29      1    97%   42
app/schemas/metric.py                42      4    90%   35, 58-60
app/schemas/station.py               36      0   100%
app/services/__init__.py              0      0   100%
app/services/station_service.py     107     18    83%   19-20, 27-28, 39-40, 53-54, 62-63, 85-86, 93-94, 101-102, 125, 134
app/tests/__init__.py                 0      0   100%
app/tests/basic_unit_tests.py       110      1    99%   145
---------------------------------------------------------------
TOTAL                               399     90    77%

```

<h3> Clean Up </h3>

In order to remove all the created containers from your PC you can run

```
bash bin/clean_up.sh
```

<h3> Next Steps </h3>

Here are a few examples of future features that I would implement:

<ol>
<li>Implement Proximity Check for New Stations

<p>When creating a new station, it would be prudent to implement a mechanism to check whether another station already exists within a specified radius. This will help to avoid redundant or overlapping station data and ensure that stations are geographically distinct as required.
</li>

<li>Develop Radius-Based Metrics Retrieval

<p>Introduce functionality to retrieve metrics based on a specified geographic radius. This feature would allow users to query metrics for a particular region by providing latitude, longitude, and date range as search parameters. This would facilitate more precise and localized data analysis.
</li>
</ol>

---

---

**P.S** In case that I was not clear or I missed anything, please let me know. I would be more than happy for a further discussion.
