# Movie API

A small project that scrapes movie data and presents it as an API

## Installation

Installing [Anaconda](https://www.anaconda.com/):

  1. Get the latest version of Anaconda from the [Distribution Page](https://www.anaconda.com/distribution/)
  ```
    https://www.anaconda.com/distribution/
  ```

  2. Download the bash script
  ```
    cd /tmp
    curl -O https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
  ```

  3. Run the script
  ```
    sudo chmod +x ./Anaconda3-2020.02-Linux-x86_64.sh
    ./Anaconda3-2020.02-Linux-x86_64.sh
  ```

Duplicate environment using `conda` and `environment.yml`

  ```
    conda env create -n env-name -f environment.yml
  ```

Next activate the Anaconda environment
  ```
    conda activate env-name
  ```

## Running project

To start scraping data run scrapy
  ```
    scrapy crawl movies
  ```
This might take a while so have some coffee :)

To start the server run flask
  ```
    FLASK_APP=server/app.py FLASK_ENV=production flask run
  ```