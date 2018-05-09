from kafka import KafkaConsumer
from kafka.errors import KafkaError
import simplejson as json
import datetime
import time
import requests

high = "alarm.high.res1.house1"
medium = "alarm.low.res1.house1"
low = "alarm.medium.res1.house1"

consumer = KafkaConsumer(high, low, medium, group_id='my-group',
                         bootstrap_servers=['localhost:8090'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')))

urlAlarms = "http://172.24.41.149:8080/alarms"
print("Conectado")
for message in consumer:
    data = message.value
    n = json.dumps(data)
    o = json.loads(n)
    headers = {'Content-type': 'application/json'}
    rsp = requests.post(urlAlarms, json=o, headers=headers)
    print(rsp.status_code)
    pastebin_url = rsp.text
    print("The response text is:%s" % pastebin_url
