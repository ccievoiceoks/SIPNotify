import re
import socket
import sys
import mailing2
#sip_notify = sys.argv[1]
#sip_notify = sip_notify.encode()
sip_notify = mailing2.sip_notify
print(sip_notify)
try:
   s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
   # If no source address or source port is provided, the socket module
   # assigns this automatically.
   s.bind(('0.0.0.0', 5060))
   s.settimeout(10)
   s.connect(('80.201.237.33', 5071))
   s.send(sip_notify)
   sys.stdout.write('\nRequest sent to vNAG\n')
   sys.stdout.write(sip_notify.decode() + '\n')
   response = s.recv(65535)
   sys.stdout.write('Response from vNAG\n')
   sys.stdout.write(response.decode() + '\n')
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
