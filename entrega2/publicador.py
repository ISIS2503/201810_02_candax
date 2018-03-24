#!/usr/local/bin/python3
import paho.mqtt.client as mqtt
import time 
import numpy as np
#Creates the client
client = mqtt.Client("C1")

print("conectando...")
#Connects to the mosquitto server on port 8083
client.connect("172.24.41.153", port = 8083)
print("conectado")
#Subscribes the client to all the topics defined on node-red flow


high = "alarm/high/res1/house1"
medium = "alarm/low/res1/house1"
low = "alarm/medium/res1/house1"

priors = [low,medium,high]

cont = 0

while True:
    print("entra while")
    payload = str(np.random.random()) + priors[cont%3]
    client.publish(priors[cont%3], payload= payload, qos=0, retain=False)
    print(payload)
    cont += 0
    time.sleep(3000)
#Definition of on_message
