#coding=utf-8

from select import select
import socket
import sys

from impacket import ImpactDecoder

DEFAULT_PROTOCOLS = ('icmp', 'tcp', 'udp')

if len(sys.argv) == 1:
    toListen = DEFAULT_PROTOCOLS
    print "Using default set of protocols. A list of protocols can be supplied from the command line, eg.: %s <proto1> [proto2] ..." % \
          sys.argv[0]
else:
    toListen = sys.argv[1:]

# Open one socket for each specified protocol.
# A special option is set on the socket so that IP headers are included with
# the returned data.
sockets = []
for protocol in toListen:
    try:
        protocol_num = socket.getprotobyname(protocol)
    except socket.error:
        print "Ignoring unknown protocol:", protocol
        toListen.remove(protocol)
        continue
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, protocol_num)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    sockets.append(s)
    print(protocol)

if 0 == len(toListen):
    print "There are no protocols available."
    sys.exit(0)

print "Listening on protocols:", toListen

# Instantiate an IP packets decoder.
# As all the packets include their IP header, that decoder only is enough.
decoder = ImpactDecoder.IPDecoder()

while len(sockets) > 0:
    # Wait for an incoming packet on any socket.
    ready = select(sockets, [], [])[0]
    for s in ready:
        packet = s.recvfrom(4096)[0]
        if 0 == len(packet):
            # Socket remotely closed. Discard it.
            sockets.remove(s)
            s.close()
        else:
            # Packet received. Decode and display it.
            packet = decoder.decode(packet)
            print packet