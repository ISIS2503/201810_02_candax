import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/notificador', methods=['POST'])
def create_correo():

    if not request.json or not 'from' in request.json or not 'to' in request.json or not 'data' in request.json or not 'subject' in request.json:
        print("error :(")
        return 400
    correo = {
        'from': request.json['from'],
        'to': request.json['to'],
        'data': request.json['data'],
        'subject': request.json['subject']
    }

    url = 'http://172.24.41.151:8089/mail'
    data = '{"From": ' + request.json['from'] + ', "To": ' + request.json['to'] + ', "Data": ' + request.json['data'] + ', "Subject": ' + request.json['subject'] + '}'
    response = requests.post(url, data)
    return jsonify({'correo': correo}), 200


@app.route('/mail', methods=['GET'])
def rest1():
    return requests.get('http://172.24.41.151:8089/mail')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081, threaded=True)