#!/usr/local/bin/python3
import paho.mqtt.client as mqtt
import time 

#Creates the client
client = mqtt.Client("C2")

#Connects to the mosquitto server on port 8083
print("Conectando...")
client.connect("172.24.41.153", port = 8083)
print("Conectado.")
#Subscribes the client to all the topics defined on node-red flow
client.subscribe("alarm/high/res1/house1")
client.subscribe("alarm/low/res1/house1")
client.subscribe("alarm/medium/res1/house1")


#Definition of on_message
def on_message(client, data, message):
    print("entra on message")
    print("message received: " + str(message.payload.decode("utf-8")))
    print("message topic: " + message.topic)
    print("message qos: " + str(message.qos))

#The client starts reading the message from the topics
client.on_message = on_message

#Start the loop of the client
client.loop_start()
time.sleep(1000)
client.loop_stop()