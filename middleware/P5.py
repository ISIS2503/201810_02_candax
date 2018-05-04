import paho.mqtt.client as mqtt
import time, requests, json


IP = "172.24.41.153"
puerto = 8083

mess = ''
num = 0
numberTolerance = 5
frecuency = 5
ms = time.time()*1000
#Creates the client
client = mqtt.Client("ClienteYALE")
#Connects to the mosquitto server on port 8083
print("Conectando a " + IP + " en el puerto "+ str(puerto) + "...")
client.connect(IP, port = puerto)
print("Conectado.")
#Subscribes the client to lock topic flow
client.subscribe("hub2.healthcheck")

def enviar_correo(message):
    #print("To: usuario1@candax.com")
    #print("message topic: " + message.topic)
    #print("message received: " + str(message.payload.decode("utf-8")))
    #print(" ")

    correo = {
        'From': 'info@candax.com',
        'To': 's.jimenez16@uniandes.edu.co',
        'Data': '¡' + message + ' fuera de linea!',
        'Subject': '¡Alarma!'
    }
    url = 'http://172.24.42.125:8089/mail'
    response = requests.post(url, json=correo)
    print(response)
    

def on_message(client, data, message):
    global mess
    mess = str(message.payload.decode("utf-8"))
    if (mess != 'OK'):
        m = 'Cerradura'
        enviar_correo(m)

client.on_message = on_message

while True:
    client.loop_start()
    time.sleep(frecuency)
    client.loop_stop()
    if(mess==''):
        num = num + 1
        print('Er' + str(num))
    else:
        mess = ''
        print('NO ERROR')

    currentTime= time.time()*1000
    if (currentTime-ms)> 300000:
        num = 0
        ms = currentTime

    if (num >= numberTolerance):
        print('MAS DE ' + str(numberTolerance) + ' ERRORES')
        a = 'Hub'
        enviar_correo(a)
        num = 0
