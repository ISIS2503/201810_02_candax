import paho.mqtt.client as mqtt
import time, requests, json


IP = "172.24.41.153"
puerto = 8083

mess = ''
num = 0
numberTolerance = 5
frecuency = 5
ms = time.time()*1000
# Creates the client
client = mqtt.Client("ClienteYALE")
# Connects to the mosquitto server on port 8083
print("Conectando a " + IP + " en el puerto " + str(puerto) + "...")
# Configuración para la seguridad del mosquitto
client.username_pw_set("microcontrolador", "Isis2503")
client.connect(IP, port=puerto)
print("Conectado.")
# Subscribes the client to lock topic flow
client.subscribe("hub2.healthcheck")

count = 1000000000

def enviar_correo(message):
    # print("To: usuario1@candax.com")
    # print("message topic: " + message.topic)
    # print("message received: " + str(message.payload.decode("utf-8")))
    # print(" ")

    correo = {
        'From': 'info@candax.com',
        'To': 's.jimenez16@uniandes.edu.co',
        'Data': '¡' + message + ' fuera de linea!',
        'Subject': '¡Alarma!'
    }
    url = 'http://localhost:8089/mail'
    response = requests.post(url, json=correo)
    print(response)


def enviar_rest(message):
    url = 'http://localhost:8000/alarms'
    token = "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJUQkVNMEl6TmpjMk0wRXpSa1ZFTVVFeU5EVkVNRU5DTUVSQ056TTRSVFl5TXprNU5qQTFRUSJ9.eyJodHRwOi8vbXluYW1lc3BhY2Uvcm9sZXMiOlsiQWRtaW4iXSwiZW1haWwiOiJwb2xsaXRvX3N0ZWZhNDRAaG90bWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOi8vaXNpczI1MDMtc2ppbWVuZXoxNi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWFkYzI1MzA0MWFhY2QxZGFhODk4YmE1IiwiYXVkIjoiVWlYY3NlSGF1SU5kUWVlTDFFbWVuV2NkZWFMWEtxWnIiLCJpYXQiOjE1MjYwNTM1NTIsImV4cCI6MTUyNjA4OTU1Mn0.AkuKAGOUByxM7vwSfAcaTZZRhfcAI7N89yZhzseWozM4BlXejX1vq1AjV_p9tHLSfUoE_AaF5-GSEoUAcwC6e7u2IGXmlbq9WeRaJzqFqvdzg-eRHSVeA8dHvKsBdIFO7cjfueVwhAsY8xTA5GQBg1dBw_njBOFgL6rmZtMe2zb4S1adzLB8yRXLdJexWco4vr17AUVUvlVbxxW3_9i-2mWL6tj7PjFCx-w_qWK5h7xCmVqWhpcjhepS9pfj3uWNVPd-Uusu_1q4QZxasZjW6aqyuC8Zuc2jEW9GzdugdYGkuXUdYW7UCJ94PrDn7cu37mlCmuTKbv5vtGKPueoN3w"
    headers = {'Authorization': token, 'Content-type': 'application/json'}
    m = {"key": "A"+count,"data": message, "owner":"O001","lock": "L1","hub": "HUB1", "house": "H001", "res_unit": "RU0", "type":"medium"}
    r = json.dumps(json.loads(mess))
    response = requests.post(url, json=r, headers=headers)
    print(response)
    count = count + 1

def on_message(client, data, message):
    global mess
    mess = str(message.payload.decode("utf-8"))
    if (mess != 'OK'):
        m = 'Cerradura'
        enviar_correo(m)
        enviar_rest(m)


client.on_message = on_message

while True:
    client.loop_start()
    time.sleep(frecuency)
    client.loop_stop()
    if(mess == ''):
        num = num + 1
        print('Er' + str(num))
    else:
        mess = ''
        print('NO ERROR')

    currentTime = time.time()*1000
    if (currentTime-ms) > 300000:
        num = 0
        ms = currentTime

    if (num >= numberTolerance):
        print('MAS DE ' + str(numberTolerance) + ' ERRORES')
        a = 'Hub'
        enviar_correo(a)
        enviar_rest(a)
        num = 0
