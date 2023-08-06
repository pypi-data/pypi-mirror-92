import logging
import sys
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

import mqtt as mqtt
import time

# logging.getLogger().setLevel(logging.DEBUG)

def main():
    logging.debug('debug message')
    logging.info('info message')
    logging.warning('warning')
    logging.error('error')
    mqtt.setup()

def test_mqtt_subscribe():
    mqtt.setup()

    def callback(client, data, message):
        print(message.payload)

    while True:
        res, id = mqtt.subscribe('hello', callback)
        if res == 0:
            break
        time.sleep(1)

    while True:
        pass
        # mqtt.setup()

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    test_mqtt_subscribe()
