from PIL import *
from config import *
from datetime import datetime
from time import sleep
from config import get_config
from poster import Poster
from servel_api import get_servel_data, data_changed
from gen_image import *

import time
import logging

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

if __name__ == "__main__":
    logging.info('Loading config...')
    config = get_config()
    logging.info('Config loaded')
    sleep_time = config["servel"].get("intervalo", 15)
    poster = Poster(config)
    while True:
        start_time = datetime.now()
        logging.info("Woke up")
        try:
            data = get_servel_data(config["servel"])
            if data_changed(data) or config["servel"]["force_gen"]:
                logging.info("Data has changed! generating image...")
                img = generate_image(data)
                logging.info("Posting generated image...")
                poster.post(img, data)
                logging.info("Done!")
            else:
                logging.info("Data has not changed since last time we got it")
        except Exception as e:
            logging.error(f"error executing loop: {e}")
        end_time = datetime.now()
        delta = (end_time - start_time).seconds
        if delta < sleep_time:
            logging.info(f"Sleeping {sleep_time - delta} seconds")
            time.sleep(sleep_time - delta)
        else:
            logging.info("No time to sleep, restarting routine")
        