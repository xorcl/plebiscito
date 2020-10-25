import twitter
import telegram
from datetime import datetime
from img_constants import READABLE_DATE
import logging


class Poster:

    def __init__(self, config):
        self.config = config
        self.telegram = telegram.Bot(config["telegram"]["token"])
        self.twitter = twitter.Api(consumer_key=config["twitter"]["api_key"],
                  consumer_secret=config["twitter"]["api_secret"],
                  access_token_key=config["twitter"]["access_token_key"],
                  access_token_secret=config["twitter"]["access_token_secret"])

    def _twitter_post(self, img, data):
        logging.info("posting in twitter...")
        try: 
            msg = self.twitter.PostUpdate(self._gen_text(data), media=img)
            logging.info(f"posted in twitter successfully! status_id= {msg.id}")
        except Exception as e:
            logging.error(f"cannot post in twitter: {e}")

    def _telegram_post(self, img, data):
        try:
            with open(img, 'rb') as f:
                msg = self.telegram.send_photo(chat_id=self.config["telegram"]["channel"], caption=self._gen_text(data), photo=f)
            logging.info(f"posted in telegram successfully! status_id= {msg.id}")
        except Exception as e:
            logging.error(f"cannot post in telegram: {e}")
            
    def _gen_text(self, data):
        fecha1 = datetime.strptime(data["constitucion"]["fecha"], READABLE_DATE)
        fecha2 = datetime.strptime(data["organo"]["fecha"], READABLE_DATE)
        return f"Resultados actualizados al {max(fecha1, fecha2).strftime(READABLE_DATE)}. Más información en http://servelelecciones.cl. #servel #plebiscito2020 #chile"
    

    def post(self, img, data):
        if self.config["twitter"]["enabled"]:
            self._twitter_post(img, data)
        if self.config["telegram"]["enabled"]:
            self._telegram_post(img, data)
    