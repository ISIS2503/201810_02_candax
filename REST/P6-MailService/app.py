from flask import Flask, request, jsonify

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# json
import json

app = Flask(__name__)


silenced = False


@app.route('/mail', methods=['POST'])
def restSendEmail():

    if request.json:
        mydata = request.json  # will be
        if(not silenced):
            sendMail(mydata)
        else:
            print("Esta silenciado, no enviará correo")
            return jsonify({"silenced":str(silenced)})

    else:
        print("no json received")

    return jsonify(request.json)

@app.route('/silence', methods=['POST'])
def cambiarSilenciado():
    global silenced
    silenced = not silenced
    return jsonify({"silenced":str(silenced)})



@app.route('/mail', methods=['GET'])
def rest1():
    return 'Mensaje llega perfectamente.'


def sendMail(jsonFile):
    info = json.load(open('conf.json'))
    usr = info["mail"]
    password = info["pass"]

    to1 = jsonFile["To"]
    data = jsonFile["Data"]
    subject = jsonFile["Subject"]

    msg = MIMEText(data)
    msg['Subject'] = subject
    msg['From'] = usr
    msg['To'] = to1

    print("Enviando a %s ..." % to1)
    s = smtplib.SMTP('smtp.office365.com', 587)
    s.ehlo()  # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    s.starttls()  # Puts connection to SMTP server in TLS mode
    s.ehlo()
    s.login(usr, password)
    s.sendmail(usr, [to1], msg.as_string())
    print("Email enviado")
    s.quit()
    return


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8089, threaded=True)
