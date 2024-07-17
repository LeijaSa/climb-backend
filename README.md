
### This repository contains a Docker Compose setup for running a backend for Climbing App using Flask and PostgreSQL

### Set up:

#### Clone the repository

### Change the usernames and passwords for your postgres database

#### Build and start the containers: docker-compose up --build.
This command will build the necessary images and start the containers in the background.

Access the backend application: Open your browser and go to http://localhost:5000 to access the Flask web application.
The database is initialized with two tables and their respective columns.

### Notes:

Ensure Docker is installed on your system.
This command will initiate the shutdown process, stopping and removing all containers, networks, and volumes created by docker-compose up: docker-compose down
