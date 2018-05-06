#!/usr/local/bin/python3
import paho.mqtt.client as mqtt
import time 
import numpy as np
import datetime
#Creates the client
client = mqtt.Client("C3")

print("conectando...")
#Connects to the mosquitto server on port 8083
client.username_pw_set("microcontrolador", "Isis2503") #Configuración para la seguridad del mosquitto
client.connect("172.24.41.153", port = 8083)
print("conectado")
#Subscribes the client to all the topics defined on node-red flow


high = "alarm/high/res1/house1"
medium = "alarm/low/res1/house1"
low = "alarm/medium/res1/house1"

priors = [high,medium,high,low]
al1 = "\",\"lowBattery\": {\"data\":\"Low Battery\", \"hubId\" :1, \"house\" : \"casa1\",\"res_unit\":\"res1\",\"type\":\"high\"}}"
al2 = "\",\"permissionDenied\": {\"data\":\"Number of attempts exceeded\", \"hubId\" :1, \"house\" : \"casa1\",\"res_unit\":\"res1\",\"type\":\"medium\"}}"
al3 = "\",\"suspiciousMotion\": {\"data\":\"Motion detected!\", \"hubId\" :1, \"house\" : \"casa1\",\"res_unit\":\"res1\",\"type\":\"high\"}}"
al4 = "\",\"doorOpen\": {\"data\":\"Door open more than 30s\", \"hubId\" :1, \"house\" : \"casa1\",\"res_unit\":\"res1\",\"type\":\"low\"}}"
alarmas = [al1,al2,al3,al4]
cont = 0

while True:
    print("entra while")
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    payload = "{\"time\":\"" + st + alarmas[cont%4]
    client.publish(priors[cont%4], payload= payload, qos=0, retain=False)
    print(payload)
    cont += 1
    time.sleep(3)
    print("sale de while")
#Definition of on_message
