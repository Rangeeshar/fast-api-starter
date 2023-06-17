# 32Health Assignment

## Pre-requisites

- Docker installed and running.
  - https://docs.docker.com/engine/install/
- Docker compose installed
  - https://dockerlabs.collabnix.com/intermediate/workshop/DockerCompose/How_to_Install_Docker_Compose.html

## Run the service

- After successful installation run the following command.
  - sudo docker-compose build
  - sudo docker-compose up
- The above command will make sure both postgres and our fastapi is up and running.
- After successful run use the following api in browser for healthcheck.
  - http://localhost:8000/health

## Apis

- Attaching postman collection with some sample data to run our service.
  - https://api.postman.com/collections/17712229-c8dc9305-5872-451e-a908-e0e345e26a6f?access_key=PMAT-01H346NK06T665HE98REA0JY3N

## Folder structure explanation

- main - consist of code to start the fastapi framework driver code.
- app - consist of all the required directories for the application.
- app/api - consist of versioned apis like v1 and can be extended to v2, v2..etc.
- app/common - consist of error codes and exceptions.
- app/core - consist of db session generator and db config.
- app/database - consist of multiple database as of now just postgres.
- app/middleware - consist of middleware configs
- app/services - consist of service layer responsible for interacting with db and business logic.

## Misc

- The answer to the assignment problem is in app/services/v1/claim/claim_service.py as a docstring.

## Any issue ?

- Mail me @ rangees28@gmail.com / Whatsapp me @ +919566414541