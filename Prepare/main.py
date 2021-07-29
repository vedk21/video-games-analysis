import sys
import os
import requests
# add internal packages
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'config'))
from api_config import API_CONFIG
from mysql_config import MYSQL_DATABASE_CONFIG
from mysql_client import add_games_data_into_mysql
from mongo_config import MONGO_DATABASE_CONFIG
from mongo_client import add_games_data_into_mongodb

def getGamesData(URL, params):
  games_list = []
  for i in range(25):
    # update page number
    params['page'] = i + 1
    # Create GET request
    try:
      response = requests.get(URL, params = params)
      if response.status_code == 200:
        games_list.extend(response.json()['results'])
    except requests.exceptions.RequestException as e:
      print('Error in API, ', URL, params, e)
  
  return games_list

def prepareGamesData(games_list):
  games_basic_details = []
  games_attributes_details = []
  games_tags_details = []
  for game in games_list:
    if not game['tba']:
      games_basic_details.append(prepareSQLData(game))
      games_tags_details.append(prepareNOSQLData(game))
      games_attributes_details.append(prepareParquetData(game))

  return {
    'sql': games_basic_details,
    'no_sql': games_tags_details,
    'parquet': games_attributes_details
  }

def prepareSQLData(game):
  return {
    'id': game['id'],
    'name': game['name'],
    'slug': game['slug'],
    'playtime': game['playtime'] if 'playtime' in game else None,
    'released': game['released'] if 'released' in game else None
  }

def prepareNOSQLData(game):
  return {
    'id': game['id'],
    'tags': getTags(game['tags']) if 'tags' in game else []
  }

def prepareParquetData(game):
  return {
    'id': game['id'],
    'platforms': getPlatforms(game['parent_platforms']) if 'parent_platforms' in game else [],
    'store': getStores(game['stores']) if 'stores' in game else [],
    'genres': getGenres(game['genres']) if 'genres' in game else []
  }

def getTags(tags):
  tags_list = []
  if tags:
    for tag in tags:
      tags_list.append({
        'id': tag['id'],
        'slug': tag['slug'],
        'name': tag['name']
      })
  
  return tags_list
      
def getPlatforms(platforms):
  platform_list = []
  if platforms:
    for platform in platforms:
      platform_list.append({
        'id': platform['platform']['id'],
        'slug': platform['platform']['slug'],
        'name': platform['platform']['name']
      })
  
  return platform_list

def getStores(stores):
  store_list = []
  if stores:
    for store in stores:
      store_list.append({
        'id': store['store']['id'],
        'slug': store['store']['slug'],
        'name': store['store']['name']
      })
  
  return store_list

def getGenres(genres):
  genre_list = []
  if genres:
    for genre in genres:
      genre_list.append({
        'id': genre['id'],
        'slug': genre['slug'],
        'name': genre['name']
      })
  
  return genre_list

if __name__ == '__main__':
  params = {
    'key': API_CONFIG['API_KEY'],
    'page': 1,
    'page_size': 40, # max size aacepted by API
    'dates': '2015-01-01,2015-01-31',
    'ordering': '-rating' # '-' means descending order
  }

  games_data = getGamesData(API_CONFIG['API_BASE_URL'], params)

  formated_game_data = prepareGamesData(games_data)

  # add mysql data
  print(len(formated_game_data['sql']))
  print(len(formated_game_data['no_sql']))
  print(len(formated_game_data['parquet']))
  add_games_data_into_mysql(MYSQL_DATABASE_CONFIG['DATABASE_NAME'], MYSQL_DATABASE_CONFIG['TABLE_NAME'], formated_game_data['sql'])
  # add mongodb data
  add_games_data_into_mongodb(MONGO_DATABASE_CONFIG['DATABASE_NAME'], MONGO_DATABASE_CONFIG['COLLECTION_NAME'], formated_game_data['no_sql'])
