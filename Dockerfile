FROM docker.io/bitnami/spark:3
MAINTAINER Vedant Kakade <vedantkakade.cp@gmail.com>

# Set user to root user
USER root

# Install required packages
RUN apt-get update \
&& apt-get install -y vim \
&& rm -rf /var/lib/apt/lists/*

# Install required python packages
RUN pip install pymongo mysql-connector-python fastparquet requests

WORKDIR /home

COPY config /home/config
COPY Prepare /home/prepare
COPY Transform /home/transform
RUN mkdir /home/data

COPY docker/spark/jars/mysql-connector-java-8.0.26.jar /opt/bitnami/spark/jars/

# Reset user to 1001 spark execution user
USER 1001
