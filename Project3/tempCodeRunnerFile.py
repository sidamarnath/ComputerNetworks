from socket import *

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

mailserver = "mail.egr.msu.edu"
mailport = 25

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, mailport))

recv = clientSocket.recv(1024).decode()
print(recv)

if recv[:3] != '220':
    print('220 reply not received from server.')

helo_msg = 'HELO Alice\r\n'
clientSocket.send(helo_msg.encode())

recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('1 250 reply not received from server.')

msg_frm = 'MAIL FROM: <amarnat4@egr.msu.edu>\r\n'
clientSocket.send(msg_frm.encode())

recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '250':
    print('2 250 reply not received from server')

rcptto = "RCPT TO: <amarnat4@egr.msu.edu>\r\n"
clientSocket.send(rcptto.encode())

recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
    print('3 250 reply not received from server.')

data = "DATA \r\n"
clientSocket.send(data.encode())
# clientSocket.send(endmsg.encode())

recv4 = clientSocket.recv(1024).decode()
print(recv4)
# if recv1[:3] != '250':
#     print('250 reply not received from server.')

clientSocket.send(msg.encode())
clientSocket.send(endmsg.encode())

# recv1 = clientSocket.recv(1024).decode()
# print(recv1)
# if recv1[:3] != '250':
#     print('250 reply not received from server.')

quit = "QUIT \r\n"
clientSocket.send(quit.encode())

recv6 = clientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '250':
    print('221 reply not received from server.')