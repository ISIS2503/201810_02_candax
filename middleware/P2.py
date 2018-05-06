#!/usr/local/bin/python3
import paho.mqtt.client as mqtt
import time 

IP = "172.24.41.153"
puerto = 8083

#Creates the client
client = mqtt.Client("C2")
#Connects to the mosquitto server on port 8083
print("Conectando a " + IP + " en el puerto "+ str(puerto) + "...")
client.username_pw_set("microcontrolador", "Isis2503") #Configuración para la seguridad del mosquitto
client.connect(IP, port = puerto)
print("Conectado.")
#Subscribes the client to all the topics defined on node-red flow
client.subscribe("alarm.high.res1.house1")
client.subscribe("alarm.low.res1.house1")
client.subscribe("alarm.medium.res1.house1")


#Definition of on_message
def on_message(client, data, message):
    topic = message.topic.split(".")
    if(topic[1] == "high"):
        print("To: yale@candax.com")
        print("message topic: " + message.topic)
        print("message received: " + str(message.payload.decode("utf-8")))
        print(" ")
        print("To: admin@candax.com")
        print("message topic: " + message.topic)
        print("message received: " + str(message.payload.decode("utf-8")))
        print(" ")
    print("To: usuario1@candax.com")
    print("message topic: " + message.topic)
    print("message received: " + str(message.payload.decode("utf-8")))
    print(" ")

#The client starts reading the message from the topics
client.on_message = on_message

#Start the loop of the client
client.loop_start()
time.sleep(1000)
client.loop_stop()