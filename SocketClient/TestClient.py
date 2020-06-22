import NetworkCommunications as ncms
from SocketClient.Client import Client

client = Client(ncms.ip, ncms.Ports.SOCKET)
while(True):
    print('left?')
    left = float(input())
    print('right?')
    right = float(input())
    client.sendSpeeds(left, right)
