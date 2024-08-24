from socket import *
import sys
import ssl

if len(sys.argv) <= 0:
    print("Usage : ' python ProxyServer.py server_ip' \n [server_ip : It is the IP address of Proxy Server]")
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
tcpServerPort = 6565   
tcpSerSock.bind(('127.0.0.1', tcpServerPort))
tcpSerSock.listen(1)
# Fill in end.

while 1:
    # Strat receiving data from the client
    print("Ready to serve")
    tcpCliSock, addr = tcpSerSock.accept()
    print("Received a connection from:", addr)
    message = tcpCliSock.recv(1024).decode()  # Fill in start.          # Fill in end.
    if message.split()[1] == None:
        continue
    if message.split()[1] == '/www.google.com':
        continue
    if message.split()[1] == '/favicon.ico':
        continue
    print(message)
    # Extract the filename from the given message
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)

    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type:text/html\r\n")
        # Fill in start.
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())
        tcpCliSock.send("\r\n".encode())
        tcpCliSock.close()
        f.close()
        # Fill in end.
        print("Read from cache")

    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            cc = socket(AF_INET, SOCK_STREAM)  # Fill in start.    # Fill in end.
            hostn = filename.replace("www.","",1)
            print(hostn)
            try:
                # Connect to the socket to port 443
                cc.connect((hostn, 443))
                print("Socket connected to port 443 of the host")
                context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
                c = context.wrap_socket(cc, server_hostname=hostn)
                # Fill in start.
            
                # Fill in end.
                # Create a temporary file on this socket and ask port 80
                # for the file requested by the client

                #fileobj = c.makefile("r", 0)
                #fileobj.write("GET "+"http://" + filename + "HTTP/1.0\n\n")

                # Read the response into buffer
                # Fill in start.
                buffer = "GET" + " /" + "HTTP/1.1\r\n\r\n"
                cc.send(buffer.encode())
                recv = cc.recv(15000000)
                # Fill in end.
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and
                # the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                # Fill in start.
                tmpFile.write(recv)
                print("Successfully saved")
                tcpCliSock.send(recv)
                # Fill in end.
            except:
                print("Illegal request")
        
        else:
            # HTTP response message for file not found
            # Fill in start.
            fileError = "HTTP/1.1 404 Not Found"
            c.send(fileError.encode())
            c.close()
            # Fill in end.
    
    # Close the client and the server sockets
    tcpCliSock.close()

# Fill in start.
tcpSerSock.close()
# Fill in end.
