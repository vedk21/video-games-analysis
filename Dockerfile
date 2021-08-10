FROM docker.io/bitnami/spark:2.4.6
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
COPY docker/spark/jars/mongo-spark-connector_2.11-2.4.2.jar /opt/bitnami/spark/jars/
COPY docker/spark/jars/mongodb-driver-3.8.1.jar /opt/bitnami/spark/jars/
COPY docker/spark/jars/mongodb-driver-core-3.8.1.jar /opt/bitnami/spark/jars/
COPY docker/spark/jars/bson-3.8.1.jar /opt/bitnami/spark/jars/

# Reset user to 1001 spark execution user
USER 1001
