FROM vedk21/hadoop-2.10.1:2.0.0
MAINTAINER Vedant Kakade <vedantkakade.cp@gmail.com>

#support for Hadoop 2.10.1
RUN curl -s https://apachemirror.wuchna.com/spark/spark-3.1.1/spark-3.1.1-bin-without-hadoop.tgz | tar -xz -C /usr/local/
RUN cd /usr/local && ln -s spark-3.1.1-bin-without-hadoop spark
ENV SPARK_HOME /usr/local/spark
ENV PYSPARK_PYTHON python3.7
RUN mkdir $SPARK_HOME/yarn-remote-client
ADD yarn-remote-client $SPARK_HOME/yarn-remote-client

# Add hive dependent jars to spark
RUN apt-get update && apt-get install -y wget procps vim \
&& wget https://repo1.maven.org/maven2/org/apache/spark/spark-hive-thriftserver_2.12/3.1.1/spark-hive-thriftserver_2.12-3.1.1.jar \
&& wget https://repo1.maven.org/maven2/org/apache/spark/spark-hive_2.12/3.1.1/spark-hive_2.12-3.1.1.jar \
&& mv spark-hive-thriftserver_2.12-3.1.1.jar $SPARK_HOME/jars/ \
&& mv spark-hive_2.12-3.1.1.jar $SPARK_HOME/jars/

RUN $BOOTSTRAP && $HADOOP_PREFIX/bin/hadoop dfsadmin -safemode leave && $HADOOP_PREFIX/bin/hdfs dfs -put $SPARK_HOME-3.1.1-bin-without-hadoop/bin /spark

ENV YARN_CONF_DIR $HADOOP_PREFIX/etc/hadoop
ENV PATH $PATH:$SPARK_HOME/bin:$HADOOP_PREFIX/bin
# update boot script
COPY bootstrap.sh /etc/bootstrap.sh
RUN chown root.root /etc/bootstrap.sh
RUN chmod 700 /etc/bootstrap.sh

# Install python v3
RUN apt-get update \
&& apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libbz2-dev \
&& rm -rf /var/lib/apt/lists/*
RUN curl -O https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz \
&& tar -xf Python-3.7.3.tar.xz \
&& cd Python-3.7.3 \
&& ./configure --enable-optimizations \
&& make -j 8 \
&& make altinstall \
&& rm -rf Python-3.7.3.tar.xz Python-3.7.3

ENTRYPOINT ["/etc/bootstrap.sh"]
