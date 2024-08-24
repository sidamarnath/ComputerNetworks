import ssl
from socket import *
import base64
import smtplib

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "mail.egr.msu.edu"
mailport = 587

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, mailport))

recv = clientSocket.recv(1024).decode()
print(recv)

if recv[:3] != '220':
    print('220 reply not received from server.')

# Send STARTTLS command to server and print server response
command = "STARTTLS\r\n"
clientSocket.send(command.encode())
tls_rev = clientSocket.recv(1024).decode()
print("START TLS: ", tls_rev)
if tls_rev[:3] != "220":
    print ("220 reply not received from server.")


# log in
scs = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)

heloCommand = 'HELO Alice\r\n'
scs.send(heloCommand.encode())
recv1 = scs.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('1 250 reply not received from server.')

scs.send('AUTH LOGIN \r\n'.encode())
recv8 = scs.recv(1024).decode()
print(recv8)


egrID = input("Enter your EGR ID: ")
password = input("Enter password: ")


user_enc = base64.b64encode(egrID.encode())
p_enc = base64.b64encode(password.encode())


scs.send(user_enc + '\r\n'.encode())
scs.send(p_enc + '\r\n'.encode())

recv9 = scs.recv(1024).decode()
print(recv9)


msg_frm = 'MAIL FROM: <{}@egr.msu.edu>\r\n'.format(egrID)
scs.send(msg_frm.encode())

recv2 = scs.recv(1024).decode()
print(recv2)
if recv2[:3] != '220':
    print('2 220 reply not received from server')


rcptto = input("Enter email recipient: ")
rcptto_2 = "RCPT TO: <{}>\r\n".format(rcptto)
# reciepient_enc = base64.b64encode(rcptto.encode()).decode() + '\r\n'
# scs.send(reciepient_enc.encode())
scs.send(rcptto_2.encode())

recv3 = scs.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
    print('3 250 reply not received from server.')


dataCommand = "DATA \r\n"
scs.send(dataCommand.encode())
# clientSocket.send(endmsg.encode())

recv4 = scs.recv(1024).decode()
print(recv4)

scs.send(msg.encode())
scs.send(endmsg.encode())

quitCommand = "QUIT \r\n"
scs.send(quitCommand.encode())

recv6 = scs.recv(1024).decode()
print(recv6)
if recv6[:3] != '250':
    print('221 reply not received from server.')

#clientSocket.close()



