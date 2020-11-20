import logging
import os
import sys
import time

from dotenv import load_dotenv, find_dotenv
from src.mqtt.factory import Factory as MQTTFactory
from src.values.credentials import Credentials


def _initialise_logging():
    log_format = '%(levelname)s | %(name)s | %(asctime)s | %(message)s'
    logging.basicConfig(stream=sys.stdout, format=log_format, level=logging.DEBUG)
    return logging.getLogger('relay')


def _load_env():
    load_dotenv(find_dotenv())


if __name__ == '__main__':
    _load_env()
    logger = _initialise_logging()

    mqtt_client = MQTTFactory.create_client(
        provider=os.getenv('MQTT_PROVIDER'),
        client_id=os.getenv('MQTT_CLIENT_ID'),
        credentials=Credentials(
            username=os.getenv('MQTT_USERNAME'),
            password=os.getenv('MQTT_PASSWORD')
        )
    )
    mqtt_client.connect(host=os.getenv('MQTT_HOST'), port=os.getenv('MQTT_PORT'))

    mqtt_client.loop_start()

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
    finally:
        logger.info('client shutdown')
