import requests

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
  RAWG_GAMING_PLATFORM_URL = 'https://api.rawg.io/api/games'
  # API Key
  API_KEY = '912d6827a6cf4170861f11df0a82f501'
  # query params
  params = {
    'key': API_KEY,
    'page': 1,
    'page_size': 40, # max size aacepted by API
    'dates': '2015-01-01,2015-01-31',
    'ordering': '-rating' # '-' means descending order
  }

  games_data = getGamesData(RAWG_GAMING_PLATFORM_URL, params)
  # Prepare data
  print(prepareGamesData(games_data))
