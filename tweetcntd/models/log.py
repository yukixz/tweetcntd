import logging
import os
from datetime import datetime
from tweetcntd import config

def init_log():
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
        # level=logging.DEBUG
    )

init_log()
log = logging.getLogger('tweetcntd')

#### Disable logging of requests
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

#### Disable Deprecation Warning
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
