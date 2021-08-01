#!/bin/bash

: ${HADOOP_PREFIX:=/usr/local/hadoop}

$HADOOP_PREFIX/etc/hadoop/hadoop-env.sh

rm /tmp/*.pid

# installing libraries if any - (resource urls added comma separated to the ACP system variable)
cd $HADOOP_PREFIX/share/hadoop/common ; for cp in ${ACP//,/ }; do  echo == $cp; curl -LO $cp ; done; cd -

# altering the core-site configuration
sed s/HOSTNAME/$HOSTNAME/ /usr/local/hadoop/etc/hadoop/core-site.xml.template > /usr/local/hadoop/etc/hadoop/core-site.xml

# setting spark defaults
#echo spark.yarn.jars hdfs:///spark/spark-assembly-1.6.0-hadoop2.6.0.jar > $SPARK_HOME/conf/spark-defaults.conf
echo export SPARK_DIST_CLASSPATH=$(hadoop classpath) > $SPARK_HOME/conf/spark-env.sh
echo alias python3=python3.7 > ~/.bashrc
source ~/.bashrc

# configure Vim editor
echo 'set pastetoggle=<F2>' > ~/.vimrc
cp $SPARK_HOME/conf/metrics.properties.template $SPARK_HOME/conf/metrics.properties

/etc/init.d/ssh start
$HADOOP_PREFIX/sbin/start-dfs.sh
$HADOOP_PREFIX/sbin/start-yarn.sh
$HADOOP_PREFIX/sbin/mr-jobhistory-daemon.sh start historyserver

# configure hive
#echo export HADOOP_HOME=/usr/local/hadoop > $HIVE_HOME/bin/hive-config.sh
#hdfs dfsadmin -safemode leave
#hdfs dfs -mkdir -p /user/hive/warehouse
#hdfs dfs -chmod g+w /user/hive/warehouse
#cd $HIVE_HOME/bin
#schematool -dbType derby -initSchema

CMD=${1:-"exit 0"}
if [[ "$CMD" == "-d" ]];
then
	service sshd stop
	/usr/sbin/sshd -D -d
else
	/bin/bash -c "$*"
fi

