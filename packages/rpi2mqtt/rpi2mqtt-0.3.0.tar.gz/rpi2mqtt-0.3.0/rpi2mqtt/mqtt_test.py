# import paho.mqtt.publish as mqtt
# import paho.mqtt.subscribe as mqtt_sub
# from paho.mqtt.client import Client
import paho.mqtt.client as mqtt
from rpi2mqtt.config import config
import traceback
import logging
import sys


# logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
# client = Client('rpi2mqtt')
# subscribed_topics = {}


# def publish(topic, payload, cnt=1):
#     try:
#         logging.debug("Pushlishing to topic {}: | attempt: {} | message: {}".format(topic, cnt, payload))
#         if cnt <= config.mqtt.retries:
#             mqtt.single(topic, payload, 
#                         hostname=config.mqtt.host, 
#                         port=config.mqtt.port,
#                         auth={'username': config.mqtt.username, 'password': config.mqtt.password},
#                         tls={'ca_certs': config.mqtt.ca_cert},
#                         retain=True)
#     except Exception as e:
#         logging.exception("Error publishing message.", e)
#         cnt += 1
#         publish(topic, payload, cnt)




    # client.tls_set(ca_certs=config.mqtt.ca_cert) #, certfile=None, keyfile=None, cert_reqs=cert_required, tls_version=tlsVersion)

    # # if args.insecure:
    # #     self.client.tls_insecure_set(True)

    # if config.mqtt.username or config.mqtt.password:
    #     client.username_pw_set(config.mqtt.username, config.mqtt.password)

    # logging.info("Connecting to " + config.mqtt.host + " port:" + str(config.mqtt.port))
    # client.connect(config.mqtt.host, config.mqtt.port, 60)
    # logging.info("Successfully connected to {} port:{}".format(config.mqtt.host, str(config.mqtt.port)))

    # client.loop_start()

    # client.on_subscribe = on_subscribe
    # client.on_message = on_message


# def on_message(mqttc, obj, msg):
#     logging.info("Recieved: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
#     # print(msg.payload)


# def on_subscribe(mqttc, obj, mid, granted_qos):
#     logging.info("Subscribed to " + str(mid) + " " + str(granted_qos))

def on_message_msgs(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # $SYS/broker/messages/#
    print("MESSAGES: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_message_bytes(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # $SYS/broker/bytes/#
    print("BYTES: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_message(mosq, obj, msg):
    # This callback will be called for messages that we receive that do not
    # match any patterns defined in topic specific callbacks, i.e. in this case
    # those messages that do not have topics $SYS/broker/messages/# nor
    # $SYS/broker/bytes/#
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))





# # working subscription callback over TLS
# mqttc = mqtt.Client()
# mqttc.tls_set(ca_certs=config.mqtt.ca_cert)

# # Add message callbacks that will only trigger on a specific subscription match.
# mqttc.message_callback_add("$SYS/broker/messages/#", on_message_msgs)
# mqttc.message_callback_add("$SYS/broker/bytes/#", on_message_bytes)
# mqttc.on_message = on_message
# # mqttc.connect("mqtt.eclipse.org", 1883, 60)

# mqttc.username_pw_set(config.mqtt.username, config.mqtt.password)
# mqttc.connect(config.mqtt.host, 8883, 60)

# mqttc.subscribe("hello", 0)

# # mqttc.loop_forever()

# mqttc.loop_start()

# while True:
#     pass













# # working subscription callback
# mqttc = mqtt.Client()

# # Add message callbacks that will only trigger on a specific subscription match.
# mqttc.message_callback_add("$SYS/broker/messages/#", on_message_msgs)
# mqttc.message_callback_add("$SYS/broker/bytes/#", on_message_bytes)
# mqttc.on_message = on_message
# # mqttc.connect("mqtt.eclipse.org", 1883, 60)

# mqttc.username_pw_set(config.mqtt.username, config.mqtt.password)
# mqttc.connect('localhost', 1883, 60)

# mqttc.subscribe("hello", 0)

# # mqttc.loop_forever()

# mqttc.loop_start()

# while True:
#     pass






# def subscribe(topic, callback):
#     global client
#     logging.info("Subscribing to topic %s", topic)
#     res = client.subscribe(topic)
#     logging.info('Subscription result = {}'.format(res))
#     # client.message_callback_add(topic, callback)
#     return res

mqttc = mqtt.Client()
mqttc.tls_set(ca_certs=config.mqtt.ca_cert) #, certfile=None, keyfile=None, cert_reqs=cert_required, tls_version=tlsVersion)

# if args.insecure:
#     self.client.tls_insecure_set(True)

if config.mqtt.username or config.mqtt.password:
    mqttc.username_pw_set(config.mqtt.username, config.mqtt.password)

# mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

# logging.info("Connecting to " + config.mqtt.host + " port:" + str(config.mqtt.port))
# mqttc.connect('localhost', 1883, 60)
mqttc.connect(config.mqtt.host, config.mqtt.port, 60)
logging.info("Successfully connected to {} port:{}".format(config.mqtt.host, str(config.mqtt.port)))

# client.loop_start()



mqttc.subscribe("hello", 0)


mqttc.loop_forever()