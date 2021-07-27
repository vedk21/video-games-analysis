import sys
import os
import mysql.connector
from mysql.connector import errorcode
# add internal packages
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'config'))
from mysql_config import MYSQL_CONFIG

def connect_to_server():
  try:
    mysql_connection = mysql.connector.connect(**MYSQL_CONFIG)
    print('Started Connection')
    db_cursor = mysql_connection.cursor()
    db_cursor.execute('SHOW DATABASES')

    for db in db_cursor:
      print(db)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
  else:
    print('Closed Connection')
    mysql_connection.close()

if __name__ == '__main__':
  connect_to_server()
