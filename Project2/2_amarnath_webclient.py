# import socket module

import socket
from socket import *
import sys # In order to terminate the program
clientSocket = socket(AF_INET, SOCK_STREAM)
host = sys.argv[1]
port = int(sys.argv[2])
path = sys.argv[3]

while True:
#Establish the connection
  print ("The server is ready to receive")
  clientSocket.connect((host,port))
  try:
    with open(path, 'rb') as f:
      for msg in f:
        msg = msg.decode('utf-8')



  #Send HTTP header lines into socket
    clientSocket.sendall(("GET /" + path + "HTTP/1.1 200 OK\r\n\r\n").encode())
  #Fill in end

  #Send the content of the requested file to the client
    for i in range(0, len(msg)):
      print(msg[i])

    print(msg)

  #Fill in end

  # Close the connection with this particular client
    clientSocket.close()

  except IOError:
    #Send response message for file not found
    clientSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
    
  clientSocket.close()
  sys.exit()