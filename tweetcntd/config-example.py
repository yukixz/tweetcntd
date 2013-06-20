from tweetcntd.tweetcntd import *

''' tweetcntd
 Config your tweetcntd.
'''
HOST = 'http://127.0.0.1:8000'
AUTH_KEY = '0x0'
TWEET_MIN = 8
TIMEZONE = 8
POST_TIME = '23:30'	# Hour:Minte. Local time

''' Databse
 Setting of Database.
'''
DATABASE_HOST = 'localhost'
DATABASE_PORT = 3306
DATABASE_DATABASE = '__YourDatabaseName__'
DATABASE_TABLE = '__YourDatabaseTable__'
DATABASE_ISINNODB = True
DATABASE_USERNAME = '__YourDatabaseUsername__'
DATABASE_PASSWORD = '__YourDatabasePassword__'

''' Log
 Support relative path.
  e.g. `foo/bar/` equal to `/path/to/tweetcntd/foo/bar/`
'''
LOG_DIRECTORY = 'log'

''' Admin Tools
 Don't forget to change ADMIN_KEY if want to use Admin Tools.
'''
ADMIN_ENABLED = False
ADMIN_KEY = 'YourAdminKey'
