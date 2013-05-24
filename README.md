# tweetcntd

## Dependencies
* python3
* - Django
* - mysql-connector-python
* - requests
* MySQL/MariaDB

## How to Deploy
1. MySQL
```
    CREATE DATABASE {{database_name_setted_in_config.py}}
    # Execute SQL_CREATE_TABLE in tweetcntd.models.database.
```

2. Crontab
```bash
    $ crontab -e
```
See `crontab` file.

3. Use 'uwsgi':
```bash
$ uwsgi -x uwsgi.xml -d /path/to/logfile
```
Or run with django:
```bash
$ python3 manager runserver
```

## GAE Version
See this: https://github.com/dazzyd/tweetcntd-gae
