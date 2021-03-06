import paho.mqtt.client as mqtt
from urllib.parse import urlparse


class clientMQTT:
    instance = None

    def __init__(self, client_name, mqtt_url):
        url = urlparse(mqtt_url)
        self.client = mqtt.Client(client_name)
        self.client.username_pw_set("microcontrolador", "Isis2503")
        self.client.connect(url.hostname, port=url.port)
        self.topic = 'yale.uniandes.ml337.key'

    def publish_message(self, message):
        print('voy a publicar el mensaje' + str(message))
        print(self.topic)
        self.client.publish(self.topic, message)
