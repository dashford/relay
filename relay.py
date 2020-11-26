import logging
import os
import sys
import time

import yaml
from blinker import signal
from dotenv import load_dotenv, find_dotenv

from src.mqtt.factory import Factory as MQTTFactory
from src.processors.mqtt.mqtt import MQTT as MQTTProcessor
from src.subscribers.factory import Factory as SubscriberFactory
from src.values.credentials import Credentials


def _initialise_logging():
    log_format = '%(levelname)s | %(name)s | %(asctime)s | %(message)s'
    logging.basicConfig(stream=sys.stdout, format=log_format, level=logging.DEBUG)
    return logging.getLogger('relay')


def _load_env():
    load_dotenv(find_dotenv())


def _load_configuration():
    with open('config/config.yaml') as file:
        return yaml.load(file)


if __name__ == '__main__':
    _load_env()
    configuration = _load_configuration()
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

    # limitation in that only one callback can be attached to a topic

    processors = []
    signals = []

    for config in configuration['subscribers']:
        subscriber = SubscriberFactory.create_subscriber(type=config['type'], logger=logger)
        mqtt_client.subscribe(topic=config['topic'])
        mqtt_client.message_callback_add(subscription=config['topic'], callback=subscriber.callback)
        for processor in config['processors']:
            if processor['type'] == 'MQTT':
                process = MQTTProcessor(
                    logger=logger,
                    mqtt_client=mqtt_client,
                    publish_topic=processor['publish_topic'])
                processors.append(process)

                broadcast = signal(processor['attribute'])
                broadcast.connect(process.notify, sender=subscriber)

                signals.append(broadcast)

    try:
        mqtt_client.loop_start()
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
    finally:
        logger.info('client shutdown')
