FROM continuumio/anaconda3
ADD environment.yml /temp/environment.yml
RUN conda env create -n movie_api -f /temp/environment.yml
RUN conda init bash
COPY . /