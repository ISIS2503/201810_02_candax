import simplejson as json
import datetime
import time
import requests
import paho.mqtt.client as mqtt

IP = "172.24.41.153"
puerto = 8083
token = "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJUQkVNMEl6TmpjMk0wRXpSa1ZFTVVFeU5EVkVNRU5DTUVSQ056TTRSVFl5TXprNU5qQTFRUSJ9.eyJodHRwOi8vbXluYW1lc3BhY2Uvcm9sZXMiOlsiQWRtaW4iXSwiZW1haWwiOiJwb2xsaXRvX3N0ZWZhNDRAaG90bWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOi8vaXNpczI1MDMtc2ppbWVuZXoxNi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWFkYzI1MzA0MWFhY2QxZGFhODk4YmE1IiwiYXVkIjoiVWlYY3NlSGF1SU5kUWVlTDFFbWVuV2NkZWFMWEtxWnIiLCJpYXQiOjE1MjYwNTM1NTIsImV4cCI6MTUyNjA4OTU1Mn0.AkuKAGOUByxM7vwSfAcaTZZRhfcAI7N89yZhzseWozM4BlXejX1vq1AjV_p9tHLSfUoE_AaF5-GSEoUAcwC6e7u2IGXmlbq9WeRaJzqFqvdzg-eRHSVeA8dHvKsBdIFO7cjfueVwhAsY8xTA5GQBg1dBw_njBOFgL6rmZtMe2zb4S1adzLB8yRXLdJexWco4vr17AUVUvlVbxxW3_9i-2mWL6tj7PjFCx-w_qWK5h7xCmVqWhpcjhepS9pfj3uWNVPd-Uusu_1q4QZxasZjW6aqyuC8Zuc2jEW9GzdugdYGkuXUdYW7UCJ94PrDn7cu37mlCmuTKbv5vtGKPueoN3w"

# Creates the client
client = mqtt.Client("C199")
# Connects to the mosquitto server on port 8083
print("Conectando a " + IP + " en el puerto " + str(puerto) + "...")
# Configuración para la seguridad del mosquitto
client.username_pw_set("microcontrolador", "Isis2503")
client.connect(IP, port=puerto)
print("Conectado.")
# Subscribes the client to all the topics defined on node-red flow
client.subscribe("alarm.high.res1.house1")
client.subscribe("alarm.low.res1.house1")
client.subscribe("alarm.medium.res1.house1")

urlAlarms = "http://172.24.42.68:8000/alarms"


# Definition of on_message
def on_message(client, data, message):
    mess = str(message.payload.decode("utf-8"))
    headers = {'Authorization': token, 'Content-type': 'application/json'}
    r = json.dumps(json.loads(mess))
    rsp = requests.post(urlAlarms, json=r, headers=headers)
    print(rsp.status_code)
    pastebin_url = rsp.text
    print("The response text is:%s" % pastebin_url
