import logging
import os
from config import BASE_DIR

LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "jarvis.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("JARVIS")

def info(msg):
    logger.info(msg)
    
def error(msg):
    logger.error(msg)
    
def debug(msg):
    logger.debug(msg)
