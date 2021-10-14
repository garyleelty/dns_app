from socket import *

portNumber = 53533

info = {}

serversocket = socket(AF_INET, SOCK_DGRAM)

serversocket.bind(('', portNumber))

print("server is ready")
while True:
   message, address = serversocket.recvfrom(2048)
   messages = message.decode()
   print("Get message"+messages)
   if 'VALUE' in messages:
      print('Register')
      # Register
      splits = messages.split('\n')
      hostname = splits[1].split("=")[1]
      value = splits[2].split("=")[1]
      info[hostname] = value
      print("Name:{}VALUE:{}".format(hostname,value))
      serversocket.sendto('Success'.encode(),address)
   else:
      print('Query')
      splits = messages.split("\n")
      name = splits[1].split("=")[1]
      print(name)
      if name in info:
         response = "TYPE=A\nNAME={}\nVALUE={}\nTTL=10".format(name,info[hostname])
         serversocket.sendto(response.encode(),address)