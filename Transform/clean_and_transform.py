from pyspark.sql import SparkSession
import sys
import os
# add internal packages
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'config'))
from mysql_config import MYSQL_DATABASE_CONFIG, MYSQL_SERVER_CONFIG
from mongo_config import MONGO_DATABASE_CONFIG, MONGO_SERVER_CONFIG
# Do this to set default encoding to 'utf-8'
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

if __name__ == '__main__':
  # Create spark session
  spark_mysql = (SparkSession
    .builder
    .appName('CleanMysqlData')
    .getOrCreate())
  
  # MYSQL connection in spark
  games_basic_details_df = (spark_mysql.read.format('jdbc')
    .option('url', 'jdbc:mysql://{hostname}:{port}/{database}'.format(database = MYSQL_DATABASE_CONFIG['DATABASE_NAME'], hostname = MYSQL_SERVER_CONFIG['host'], port = MYSQL_SERVER_CONFIG['port']))
    .option('driver', 'com.mysql.jdbc.Driver')
    .option('dbtable', MYSQL_DATABASE_CONFIG['TABLE_NAME'])
    .option('user', MYSQL_SERVER_CONFIG['user'])
    .option('password', MYSQL_SERVER_CONFIG['password'])
    .load())

  print(games_basic_details_df.columns)

  games_basic_details_df.show(n = 5, truncate = False)

  spark_mysql.stop()

  spark_mongo = (SparkSession
    .builder
    .appName('CleanMongoData')
    .getOrCreate())

  # MONGODB connection in spark
  games_attributes_details_df = (spark_mongo.read.format('mongo')
    .option('uri', 'mongodb://{username}:{password}@{hostname}:{port}/'.format(username = MONGO_SERVER_CONFIG['username'], password = MONGO_SERVER_CONFIG['password'], hostname = MONGO_SERVER_CONFIG['host'], port = MONGO_SERVER_CONFIG['port']))
    .option('database', MONGO_DATABASE_CONFIG['DATABASE_NAME'])
    .option('collection', MONGO_DATABASE_CONFIG['COLLECTION_NAME'])
    .load())

  games_attributes_details_df.show(n = 5, truncate = False)

  # Stop session
  spark_mongo.stop()
