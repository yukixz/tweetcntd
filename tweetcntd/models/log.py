import logging
import os
from datetime import datetime
from tweetcntd import config

def getLogger():
    # path
    dir = config.LOG_DIRECTORY
    if not os.path.exists(dir): os.makedirs(dir)
    utcnow = datetime.utcnow()
    file = utcnow.strftime("%Y-%m-%d.log")
    PATH = os.path.join(dir,file)
    
    # format
    FORMAT = '%(asctime)s %(levelname)s @%(module)s:%(lineno)d - %(message)s'
    
    logging.basicConfig(
        filename=PATH,
        filemode='a',
        format=FORMAT,
        level=logging.INFO
    )
    
    return logging.getLogger()\
log = getLogger()
