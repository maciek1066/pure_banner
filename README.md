# Pure banner app

Test Pure Banner app using Docker to containerize a Django application and run automated tests. The setup allows you to run the Django app on your `localhost` or execute tests automatically within Docker containers.

## Prerequisites

Make sure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)


## Getting Started

### 1. Build Docker Image

Before running the application or tests, you need to build the Docker image. Run the following command from the root directory of the project (where `Dockerfile` and `docker-compose.yml` are located):

```bash
docker-compose build
```

### 1. Running Automated Tests
To run the Django application and access it on localhost, execute the following command:

```bash
docker-compose up django-app
```

This will run all tests defined in your Django project, and the output will be displayed in the terminal.

### 4. Stopping and Cleaning Up
```bash
docker-compose down
```
This will stop all running containers and remove them.

#### Environment Variables
DJANGO_SETTINGS_MODULE: Set to pure_banner.settings by default to use the correct Django settings file.
PYTHONPATH: Ensures Python can find the modules correctly in the /app directory within the Docker container.

