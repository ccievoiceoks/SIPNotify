#!/usr/local/bin/python3
import mailbox

pxs = mailbox.mbox('pxs')
pxs.lock()
for msg in pxs:
   SUBJECT = msg['Subject']
   print(SUBJECT)
   if SUBJECT in 'Message notification':
       BODY = msg.get_payload()
       Splitted = BODY.splitlines()
       for line in Splitted:
          words = line.split()
          print(words)
       Phones = Splitted[1]
       Messages = Splitted[2]
       print('------------')
       print(Phones)
       a,b,c,d = Phones.split()
       ciscophone = str(Phones[1])
       fmuphone = str(Phones[3])
       voicecount = str(Messages[2])
       print('The Cisco Phone number is {} and is associated with the fmu device {} , there is {} Voice Messages'.format(b,d,voicecount))
  
#pxs.clear(16)
amount = pxs.keys()
for i in amount:
   pxs.remove(i)
pxs.flush()
pxs.close()
