# ![RealWorld Example App](logo.png)

> ### Django Rest Framework + Postgres codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.


### [Demo](https://demo.realworld.io/)&nbsp;&nbsp;&nbsp;&nbsp;[RealWorld](https://github.com/gothinkster/realworld)


This codebase was created to demonstrate a fully fledged fullstack application built with Django Rest Framework including CRUD operations, authentication, routing, pagination, and more.

We've gone to great lengths to adhere to the Django Rest Framework community styleguides & best practices.

For more information on how to this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.


# Usage

1. Clone the Git repository:

```shell
  git clone https://github.com/Sean-Miningah/realWorld-DjangoRestFramework.git

```
2. Create Virtual Environment
```shell
  cd project_directory
  python3 -m venv venv 
  pip3 install -r requirements.txt
```

make sure you a postgres database configured for connection

3. Run Application
> python manage.py runserver 

## Using Docker and Docker Compose 

Run:
> docker compose up

# API Documentation 

The project provides API documentation using Swagger. To access the API documentation, follow these steps:

Ensure that the project is running by executing the command mentioned in the "Usage" section.

Open a web browser and navigate to the following endpoint:

```bash
/swagger
```
# Contributing
If you would like to contribute to the project, please follow these guidelines:

1. Fork the repository and create a new branch for your feature or bug fix.

2. Make the necessary changes and commit them.

3. Push your changes to your forked repository.

4. Submit a pull request to the main repository, explaining the changes you made and any additional information that might be helpful for review.

