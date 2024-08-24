
#import socket module
from socket import *
import sys # In order to terminate the program
serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
serverSocket.bind(('', 6790))
serverSocket.listen(1)


while True:
    #Establish the connection
    print ("The server is ready to receive")
    connectionSocket, addr = serverSocket.accept() #Fill in start

    #Fill in end
    try:
        message = connectionSocket.recv(1024) #Fill in start    #Fill in end
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read() #Fill in start     #Fill in end

        #Send HTTP header lines into socket
        #Fill in start
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        #connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n")
        #Fill in end


        #Send the content of the requested file to the client
        #Fill in start
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
            
            #connectionSocket.send(outputdata[i])
        # connectionSocket.send("This is a test".encode())
        #Fill in end


        # Close the connection with this particular client
        connectionSocket.close()
    
    except IOError:
        #Send response message for file not found
        #Fill in start
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        #Fill in end


        #Close client socket
        #Fill in start
        connectionSocket.close()
        #Fill in end


    serverSocket.close()
    sys.exit()


