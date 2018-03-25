import requests

#!/usr/local/bin/python3
import paho.mqtt.client as mqtt
import time

IP = "172.24.41.153"
puerto = 8083

#Creates the client
client = mqtt.Client("C3")

#Connects to the mosquitto server on port 8083
print("Conectando a " + IP + " en el puerto "+ str(puerto) + "...")
client.connect(IP, port = puerto)
print("Conectado.")
#Subscribes the client to all the topics defined on node-red flow
client.subscribe("alarm/high/*")


#Definition of on_message
def on_message(client, data, message):
    print("entra on message")
    print("message received: " + str(message.payload.decode("utf-8")))
    print("message topic: " + message.topic)
    print("message qos: " + str(message.qos))
    correo = {
        'to': str(message.qos),
        'data': data,
        'subject': '¡Alarma!'
    }
    url = 'http://172.24.41.151:8089/mail'
    data = '{"From": ' + 'none' + ', "To": ' + correo['to'] + ', "Data": ' + data['data'] + ', "Subject": ' + correo['subject'] + '}'
    response = requests.post(url, data)


#The client starts reading the message from the topics
client.on_message = on_message

#Start the loop of the client
client.loop_start()
time.sleep(1000)
client.loop_stop()

