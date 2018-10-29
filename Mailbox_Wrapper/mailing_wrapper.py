#!/usr/local/bin/python3
import mailbox

pxs = mailbox.mbox('/var/mail/proximus')
pxs.lock()
for msg in pxs:
   print(msg['Subject'])
   print(msg.get_payload())

#pxs.clear(16)
amount = pxs.keys()
for i in amount:
   pxs.remove(i)
pxs.flush()
pxs.close()
