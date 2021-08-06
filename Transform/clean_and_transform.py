from pyspark.sql import SparkSession
import sys
# Do this to set default encoding to 'utf-8'
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

if __name__ == '__main__':
  # Create spark session
  spark = (SparkSession
    .builder
    .appName('CleanAndTransformGamesData')
    .getOrCreate())
  

  games_basic_details_df = (spark.read.format('jdbc')
    .option('url', 'jdbc:mysql://mysql:3306/video_games_analysis')
    .option('driver', 'com.mysql.jdbc.Driver')
    .option('dbtable', 'games')
    .option('user', 'spark-user')
    .option('password', 'spark123')
    .load())

  print(games_basic_details_df.columns)

  games_basic_details_df.show(n = 50, truncate = False)

  # Stop session
  spark.stop()
