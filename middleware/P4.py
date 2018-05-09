import paho.mqtt.client as mqtt
import time


IP = "172.24.41.153"
puerto = 8083

mess = ''
num = 0
numberTolerance = 3
frecuency = 5
ms = time.time()*1000
# Creates the client
client = mqtt.Client("ClienteP4")
# Connects to the mosquitto server on port 8083
print("Conectando a " + IP + " en el puerto " + str(puerto) + "...")
# Configuración para la seguridad del mosquitto
client.username_pw_set("microcontrolador", "Isis2503")
client.connect(IP, port=puerto)
print("Conectado.")
# Subscribes the client to lock topic flow
client.subscribe("alarms.res1.house1")


def on_message(client, data, message):
    global mess
    m = str(message.payload.decode("utf-8"))
    if(m == 'OK'):
        mess = str(message.payload.decode("utf-8"))


client.on_message = on_message

while True:
    client.loop_start()
    time.sleep(frecuency)
    client.loop_stop()
    client.publish("hub2.healthcheck", payload='OK', qos=0, retain=False)
    # print('PUBLICOOOO')
    if(mess == ''):
        num = num + 1
        print('Er' + str(num))
    else:
        mess = ''

    currentTime = time.time() * 1000
    if (currentTime-ms) > 30000:
        num = 0
        ms = currentTime

    if (num >= numberTolerance):
        print('MAS DE ' + str(numberTolerance) + ' ERRORES')
        client.publish("hub2.healthcheck",
                       payload='ERROR LOCK2',
                       qos=0,
                       retain=False)
        num = 0
