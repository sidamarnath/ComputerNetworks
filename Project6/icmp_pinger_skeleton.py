from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8



# In this function we make the checksum of our packet 
def icmp_checksum(str_):
    str_ = bytearray(str_)
    csum = 0
    countTo = (len(str_) // 2) * 2

    for count in range(0, countTo, 2):
        thisVal = str_[count+1] * 256 + str_[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff

    if countTo < len(str_):
        csum = csum + str_[-1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer



def recvPingPacket(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)


			# Fill in start
			# 	one or multiple lines of your code     
			#   You can use "struct.unpack" function with 
			#   parameter "bbHHh" to decode the ICMP header
        icmpHeader = recPacket[20:28]
        icmpType, code, mychecksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
			# Fill in end	

    
        if icmpType != 8 and packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent

        timeLeft = timeLeft - howLongInSelect
        
        if timeLeft <= 0:
            return "Request timed out."

def sendPingPacket(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
	
    
    
        # Fill in start
        # 	one or multiple lines of your code 
        #   Calculate the checksum on the data and the dummy header.
    myChecksum = icmp_checksum(header + data)
        # Fill in end	
	

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
    #Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	
        # Fill in start
        # 	one or multiple lines of your code 
        #   use the socket to send the ICMP packet
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))
        # Fill in end	


def oneTimePing(destAddr, timeout):         
    icmp = getprotobyname("icmp") 
    #Create Socket here
    mySocket = socket(AF_INET, SOCK_RAW, icmp) 

    myID = os.getpid() & 0xFFFF  #Return the current process i     
    sendPingPacket(mySocket, destAddr, myID) 
    delay = recvPingPacket(mySocket, myID, timeout, destAddr)          
    mySocket.close()         
    return delay  


# def ping(host, timeout=1):
#     dest = gethostbyname(host)
#     print ("Pinging " + dest + " using Python:")
#     print ("")
#     #Send ping requests to a server separated by approximately one second
#     loop = 0
#     while loop < 10:
#         delay = oneTimePing(dest, timeout)
#         print("delay: "+format(delay*1000, ".3f")+" (ms)")
#         time.sleep(1)# one second
#         loop += 1
#     return delay


def ping(host, timeout=1):
    # perform multiple pings and calculate statistics
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")

    loop = 0
    total_delay = 0
    min_delay = float('inf')
    max_delay = 0
    lost_packets = 0

    while loop < 10:
        delay = oneTimePing(dest, timeout)
        if isinstance(delay, str):  # packet lost
            print(delay)
            lost_packets += 1
        else:
            print("delay: " + format(delay * 1000, ".3f") + " (ms)")
            total_delay += delay
            if delay < min_delay:
                min_delay = delay
            if delay > max_delay:
                max_delay = delay
        time.sleep(1)  # one second
        loop += 1

    if loop > lost_packets:  # packets received
        avg_delay = total_delay / (loop - lost_packets)
        packet_loss_rate = lost_packets / loop * 100
        print("")
        print("Ping statistics for " + dest + ":")
        print("    Packets: Sent = " + str(loop) + ", Received = " + str(loop - lost_packets) + ", Lost = " + str(
            lost_packets) + " (" + format(packet_loss_rate, ".1f") + "% loss)")
        print("Approximate round trip times in milli-seconds:")
        print("    Minimum = " + format(min_delay * 1000, ".3f") + "ms, Maximum = " + format(max_delay * 1000, ".3f") + "ms, Average = " + format(avg_delay * 1000, ".3f") + "ms")
    else:  # all packets lost
        print("")
        print("Ping statistics for " + dest + ":")
        print("    Packets: Sent = " + str(loop) + ", Received = 0, Lost = " + str(loop) + " (100% loss)")
        print("Approximate round trip times in milli-seconds:")
        print("    Minimum = N/A, Maximum = N/A, Average = N/A")


ping("127.0.0.1")
print("------------------------")
ping("google.com")
print("------------------------")
ping("ox.ac.uk")
print("------------------------")
ping("www.tsinghua.edu.cn")
print("------------------------")
ping("8.8.8.8")
print("------------------------")
ping("www.up.ac.za")