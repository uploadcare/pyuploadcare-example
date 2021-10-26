# Pyuploadcare Example app

This example project demonstrates the pyuploadcare capabilities.
The project is based on Python 3.9 and Django 3.2.8.

* [Installation](#installation)
  * [Using docker](#using-docker)
  * [Without docker](#without-docker)
* [Usage](#usage)
  * [Configuration](#configuration)
* [Useful links](#useful-links)

## Installation

### Using Docker

To install the example application you need to [install Docker Compose package](https://docs.docker.com/compose/install/).
When Docker Compose is installed, clone this repository and build a Docker image by using the `build` directive:

```console
$ git clone git@github.com:uploadcare/pyuploadcare-example.git
$ docker-compose build
```

This command will build an image for the application.

When the image is ready — up the containers with the following command.

```console
$ docker-compose up -d
```

Then, apply migrations:

```console
$ docker-compose run --rm uploadcare ./manage.py migrate
```

Now, the application must be available in your web-browser, on `http://localhost:8000`

### Without docker

First of all, clone this repository:

```console
$ git clone git@github.com:uploadcare/pyuploadcare-example.git
```

Make sure Python and Poetry are installed on your system. Fire command prompt and run command:

```console
$ python -V
Python 3.9.6
$ poetry --version
Poetry version 1.1.9
```

If Python or Poetry are not installed, check out following links with instructions, how to install those:
* [Install python](https://www.python.org/downloads/)
* [Install Poetry](https://python-poetry.org/docs/#installation)

Then install dependencies:

```console
$ poetry install
```

After dependencies are installed, apply database migrations:

```console
$ poetry run python app/manage.py migrate
```

Now, you can run the server:

```console
$ poetry run python app/manage.py runserver
```

and see the application available in your web-browser, on `http://localhost:8000`

## Usage

### Configuration

To start using tha application you need to set your API keys (public key and secret key).
These keys can be set as ENV variables using the `export` directive:

```console
$ export UPLOADCARE_PUBLIC_KEY=demopublickey
$ export UPLOADCARE_SECRET_KEY=demoprivatekey
```

## Useful links
* [Uploadcare documentation](https://uploadcare.com/docs/?utm_source=github&utm_medium=referral&utm_campaign=pyuploadcare)  
* [Upload API reference](https://uploadcare.com/api-refs/upload-api/?utm_source=github&utm_medium=referral&utm_campaign=pyuploadcare)  
* [REST API reference](https://uploadcare.com/api-refs/rest-api/?utm_source=github&utm_medium=referral&utm_campaign=pyuploadcare)  
* [Contributing guide](https://github.com/uploadcare/.github/blob/master/CONTRIBUTING.md)  
* [Security policy](https://github.com/uploadcare/pyuploadcare/security/policy)  
* [Support](https://github.com/uploadcare/.github/blob/master/SUPPORT.md)
* [A Python library for Uploadcare service](https://github.com/uploadcare/pyuploadcare)
