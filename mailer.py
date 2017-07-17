import logging
import sys
import os
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
api = Api(app)

TO = ""
MSG = ""
FROM = ""

@app.route('/api/', methods=['POST'])
def print_request():
    request_json = request.get_json()
    # secret of app to verify from spam bots
    if request_json.get("secret") == "xxx":
        logging.info(request_json)
        logging.info("correct secret key")
        TO = request_json.get('email')
        FROM = 'xxx@gmail.com' 
        MSG = request_json.get('content')
        SUBJECT = request_json.get('subject')
        send(TO, FROM, MSG, SUBJECT) 
    else: 
        logging.warning("wrong secret key")
    return jsonify(request_json)

def send(TO, FROM, MSG, SUBJECT):
    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = TO
    msg['Subject'] = SUBJECT
    body = MSG
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()



    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            # https://myaccount.google.com/apppasswords
            s.login("xxx@gmail.com", "gmailSecretAppKey")
            s.sendmail("xxx@gmail.com", TO, text)
            s.close()
        logging.info("Email sent!")
    except:
        logging.warning("Unable to send the email. Error: ", sys.exc_info()[0])
        raise       

if __name__ == '__main__':
    logging.basicConfig(filename='mailer.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', debug=False)
    
