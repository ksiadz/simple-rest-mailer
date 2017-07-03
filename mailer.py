import sys
import os
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEText import MIMEText

app = Flask(__name__)
api = Api(app)

TO = ""
MSG = ""
FROM = ""

@app.route('/api/', methods=['POST'])
def add_entry():
    request_json     = request.get_json()
    value1           = request_json.get('data')
    print(value1)

    return jsonify(request_json)

@app.route('/test/', methods=['POST'])
def add_test():
    request_json = request.get_json()
    TO = request_json.get('to')
    FROM = request_json.get('sender')
    MSG = request_json.get('msg')
    send(TO, FROM, MSG) 
    return jsonify(TO, FROM, MSG, request_json)

def send(TO, FROM, MSG):
    # Send the email
    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = TO
    msg['Subject'] = 'Order from ' + FROM
    body = MSG
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()



    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login("###", "###")
            s.sendmail("###", TO, text)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise    
    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = TO
    msg['Subject'] = 'Order from ' + FROM
    body = MSG
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
