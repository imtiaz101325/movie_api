# Movie API

A small project that scrapes movie data and presents it as an API

## Installation

Install [Docker](https://docs.docker.com/get-docker/):

  - For Mac follow the instructions [here](https://docs.docker.com/docker-for-mac/install/)
  - For Linux follow the instructions [here](https://docs.docker.com/engine/install/)
  - For Windows follow the instructions [here](https://docs.docker.com/docker-for-windows/install/)

## Running project

Build the Dockerfile
  ```
    docker build -t movie_api_container .
  ```

You can now run and interactive shell
  ```
    docker run -it movie_api_container:latest /bin/bash

    (base) root@b9dc6dc4d27c:/# conda activate movie_api
    (movie_api) root@b9dc6dc4d27c:/# scrapy crawl movies
    (movie_api) root@b9dc6dc4d27c:/# FLASK_APP=server/app.py FLASK_ENV=production flask run
  ```

To start scraping data run scrapy
  ```
    docker run -it movie_api_container:latest /opt/conda/bin/conda run -n movie_api scrapy crawl movies
  ```
This might take a while so have some coffee :)

To start the server run flask
  ```
    docker run -it -p 127.0.0.1:5000:5000  movie_api_container:latest /opt/conda/bin/conda run -n movie_api FLASK_APP=server/app.py FLASK_ENV=production flask run

  ```