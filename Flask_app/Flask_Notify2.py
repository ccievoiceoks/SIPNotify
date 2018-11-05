""" This module will help to enhance the MWI Notification
for Cisco Third-Party on vNAG."""
from flask import Flask, request
import json
import datetime
import uuid
import re
import socket
import sys

app = Flask(__name__)
app.config['DEBUG'] = True


def SIP_Connect(sip_notify):
    """ This function will establish a socket(SIP) to the vNAG

    :param sip_notify bytes: SIP NOTIFY Message to send to vNAG
    :return: Returns normally the SIP acknowledge from the vNAG
    :rtype: bytes

    :Example:
    NOTIFY sip:{fmudevice}@80.201.237.33:5071 SIP/2.0
    Via:SIP/2.0/UDP {cucmserver}:5060
    To: <sip:{ciscodevice}@81.201.237.33>
    From: <sip:{ciscodevice}@{cucmserver}>;tag={tag}
    Date: {jour}
    Call-Id: 1349882@{cucmserver}
    CSeq: 101 NOTIFY
    Max-Forward: 70
    User-Agent: LMBUTS
    Contact: <sip:{ciscodevice}@{cucmserver}:5060>
    Event: message-summary
    Subscription-State: active
    Content-Type: application/simple-message-summary
    Content-Length: 23

    Messages-Waiting: yes
    Voice-Message: {message}/0\n\n'''.format(**args)
    print(sip_notify_msg)
    """

    try:
       s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
       # If no source address or source port is provided, the socket module
       # assigns this automatically.
       s.bind(('0.0.0.0', 5060))
       s.settimeout(10)
       s.connect(('80.201.237.33', 5071))
       s.sendall(sip_notify)
       sys.stdout.write('\nRequest sent to vNAG\n')
       sys.stdout.write(sip_notify.decode() + '\n')
       response = s.recv(65535)
       sys.stdout.write('Response from vNAG\n')
       sys.stdout.write(response.decode() + '\n')
       return response.decode()
    except socket.timeout:
       # Socket timed out.  This could mean that no response was received
       # from the far end for a sent SIP packet, or that a TCP connection
       # was not established within the timeout limit.
       sys.stdout.write('No response received within 10 seconds\n')
    finally:
       try:
           # Regardless of what happened, try to gracefully close down the
           # socket.
           s.shutdown(1)
           s.close()
       except UnboundLocalError:
           # Socket has not been assigned.
           pass

@app.route('/', methods=['POST','GET'])
def hello():
    print('This script is the SIP Notify MWI for FMU Third Party Devices')
    return 'This script is the SIP Notify MWI for FMU Third Party Devices'

@app.route('/FMU',methods=['POST','GET'])
def FMU():
    input = request.get_data()
    data = input.decode('utf8')
    print('FMU Mail Notification is received, the script will handle it in some seconds')
    splitted = data.split('\n')
    voicelines = splitted[17]
    messagedesc = splitted[18]
    ciscophone,fmuphone = voicelines.split(' ')[1:4:2]
    amountvm = messagedesc.split(':')[1]
    # print('\n The Cisco phone extension is {} and is associated with FMU extension {}, there are {} Voice messages'.format(ciscophone,fmuphone,amountvm))
    fmuphone = fmuphone[1:]
    cucmserver = '192.168.192.21'
    today = datetime.datetime.today()
    jour = '{:%a, %d %b %Y %H:%M:%S} GMT'.format(today)
    tag = uuid.uuid1()
    args = {'fmudevice': fmuphone,'cucmserver': cucmserver,'ciscodevice': ciscophone,'jour': jour,'tag': tag, 'message': amountvm}
    
    sip_notify_msg = '''\
NOTIFY sip:{fmudevice}@80.201.237.33:5071 SIP/2.0
Via:SIP/2.0/UDP {cucmserver}:5060
To: <sip:{ciscodevice}@81.201.237.33>
From: <sip:{ciscodevice}@{cucmserver}>;tag={tag}
Date: {jour}
Call-Id: 1349882@{cucmserver}
CSeq: 101 NOTIFY
Max-Forward: 70
User-Agent: LMBUTS
Contact: <sip:{ciscodevice}@{cucmserver}:5060>
Event: message-summary
Subscription-State: active
Content-Type: application/simple-message-summary
Content-Length: 23

Messages-Waiting: yes
Voice-Message: {message}/0\n\n'''.format(**args)
    # print(sip_notify_msg)

    sip_notify = sip_notify_msg.encode()
    VNAG = SIP_Connect(sip_notify)
    #print(VNAG)

    return '200'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
