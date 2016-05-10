'''
Created on 19-Oct-2014

@author: mayank
'''

'''
Importing required libraries
'''
import socket
import time
import sys
import random
from os import curdir, sep, linesep
class GBNClient:

    def __init__(self, host = 'localhost', sendport = 9090, readport = 10001):
        self.current_seqn = 0 #current sequence number be sent
        self.num_active      = 0 # number of spaces filled in the sender window
        self.LAST_SENT_SEQN  = -1 #Last sent sequence to the server
        self.sws = 7 #Sender Sindow Size
        self.window=[None] * self.sws #list which will contain window
        self.last_acked_seqn = self.LAST_SENT_SEQN #last acknowdgement recived
        #Starts the socket to listen to server
        self.server_address = (host, readport)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0.5)#Set Timeout as 0.5sec
        self.sock.bind((host,sendport))
        self.window=[None] * 100
        self.flag = 0
        self.logf = 0

    #Function to make Chunks of Data
    def split(self, data, n):
        while data:
            yield data[:n]
            data = data[n:]

    #Condition to check If there is space available in Sender Window
    def canAddToWindow(self):
        return self.num_active < self.sws

    #Making a Datagram Packet for Sending
    def makeDatagram(self,seqno,packetdata):
        packetsize=len(packetdata)
        return str(seqno)+'||||'+str(packetsize)+'||||'+str(packetdata)

    #Function to send Packets
    def sendDatagram(self,packet):
        #print 'Send Packet No.', self.seqno(p)
        #self.logf.write(str(time.time())+" [c] "+str(self.seqno(p))+" Send"+'/n')
        #self.sock.sendto(p,self.server_address)
        i= random.randint(0,30)
        if(i>10):
            print 'Send Packet No.', self.seqno(packet)
            self.logf.write(str(time.time())+" [c] "+str(self.seqno(packet))+" Send"+'\n')
            self.sock.sendto(packet,self.server_address)
        else:
            print'Dropped Packet No.', self.seqno(packet)
            self.logf.write(str(time.time())+" [c] "+str(self.seqno(packet))+" Dropped \n")
        
    #Function to add packets to the window
    def addToWindow(self,byte):
        self.window[self.num_active] = byte
        self.LAST_SENT_SEQN=self.current_seqn
        self.current_seqn = (self.current_seqn + 1)
        self.num_active= self.num_active+1
        self.sendDatagram(byte)

    #Funtion to extract Packet No. from the datagram
    def seqno(self,datagram):
        return int(datagram.split('||||')[0])

    #Function to get the receiver window size
    def rwnd(self,datagram):
        return int(datagram.split('||||')[1])

    #Function to pop packets from Sender Window
    def removeFromWindow(self,datagram):
        index=0
        self.window.pop(index)
        self.window.append(None)
        self.num_active=self.num_active-1;
        self.last_acked_seqn = self.seqno(datagram)#last ack sequence for logging

    #Function to check Acknowledgements
    def acceptAcks(self):
        try:
            datagram,address=self.sock.recvfrom(4096)
        except socket.timeout:
            print 'Connection timed out'
            self.logf.write(str(time.time())+" [c] "+str(self.last_acked_seqn+1)+" Timeout\n")
            return False
        print 'Received Ack No.', self.seqno(datagram)
        if self.seqno(datagram)==self.last_acked_seqn+1:   
            self.sws=self.rwnd(datagram)            
            self.removeFromWindow(datagram)
            return True
        elif self.seqno(datagram)<self.last_acked_seqn+1:
            return False
        #Handling Cumulative ACKs
        elif self.seqno(datagram)>self.last_acked_seqn+1:
            self.sws=self.rwnd(datagram)
            self.counter = self.last_acked_seqn
            while(self.counter<self.seqno(datagram)):
                self.removeFromWindow(datagram)
                self.counter += 1
            return True
        
    #Function to Resend complete window  
    def resendWindow(self):
    	current=0
    	while(current<self.num_active):
            self.logf.write(str(time.time())+" [c] "+str(self.seqno(self.window[current]))+" Retransmit\n")
            print 'Retransmit Packet No.', self.seqno(self.window[current])
            self.sock.sendto(self.window[current],self.server_address)
            current += 1

    #Function to send End of File message
    def sendEOF(self):
        self.sock.sendto('|!@#$%^&',self.server_address)

    #Function to manage flow of Data Packets    
    def sendMessage(self, datalist, listlength):
        currentPacket = 0
        while(currentPacket < listlength or self.last_acked_seqn != listlength - 1):
            while(self.canAddToWindow()==True and currentPacket < listlength):
                datagram = self.makeDatagram(currentPacket, datalist[currentPacket])
                self.addToWindow(datagram)
                currentPacket += 1
            if (self.acceptAcks()==False):
                self.resendWindow()
        self.sendEOF()

        
def validation():
    sys.stdout = sys.stderr
    print 'Type the following command in terminal'
    print 'GBNclient.py [filename.extension]'
    sys.exit(2)

#Main Function
if __name__ == '__main__':
    config = {}
    execfile("ws.conf", config)
    datasize = config["datasize"]

    
    if len(sys.argv) != 2:
        validation()
    else:
        fsend = str(sys.argv[1])
        print fsend
    try:
        f = open(fsend, "rb")
        data = f.read()
        sender = GBNClient()
        #sampleData = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q']
        m = list(sender.split(data, datasize))
        fName = 'clientLog.txt'
        sender.logf = open(curdir + sep + fName, 'w+')
        sender.sendMessage(m, len(m))
        sender.logf.close()
        f.close()
    except IOError:
        print 'File Unavailable'
