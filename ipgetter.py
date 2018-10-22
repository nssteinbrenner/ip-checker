#!/usr/bin/env python

import smtplib

from fabric import Connection
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

with open('config', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if 'username:' in line:
            targetline = line.strip().split(' ')
            username = targetline[1]
        if 'password:' in line:
            targetline = line.strip().split(' ')
            password = targetline[1]
        if 'emailpass:' in line:
            targetline = line.strip().split(' ')
            emailpass = targetline[1]
        if 'hostname:' in line:
            targetline = line.strip().split(' ')
            hostname = targetline[1]
        if 'to:' in line:
            targetline = line.strip().split(' ')
            toaddr = targetline[1:]
        if 'from:' in line:
            targetline = line.strip().split(' ')
            fromaddr = targetline[1]
        if 'port:' in line:
            targetline = line.strip().split(' ')
            portnum = targetline[1]

targetstart = '	inet '


def notifyMe(toaddr, fromaddr, password, pubip):
    msg = f'Your new public IP is: {pubip}'
    subj = 'Your public IP has changed'
    message = MIMEMultipart()
    message['From'] = fromaddr
    message['To'] = toaddr
    message['Subject'] = subj
    message.attach(MIMEText(msg, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, password)
    text = message.as_string()
    server.sendmail(fromaddr, toaddr, text)


def startCon(hostname, username, port, password):
    c = Connection(host=hostname, user=username, port=portnum,
                   connect_kwargs={'password': password})
    result = c.run('ifconfig re0', hide='stdout').stdout.split('\n')
    c.close()
    return result


def getPub(result):
    for line in result:
        if targetstart in line:
            text = line.split(' ')
            pubip = text[1]
            return pubip
    return pubip


def checkPub(pubip):
    with open('pub_ip', 'r+') as f:
        current = f.readline().strip()
        if current != pubip:
            f.seek(0)
            f.write(pubip)
            f.truncate()
            for i in toaddr:
                notifyMe(i, fromaddr, emailpass, pubip)


result = startCon(hostname, username, portnum, password)
pubip = getPub(result)
checkPub(pubip)
