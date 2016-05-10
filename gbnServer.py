'''
Created on 19-Oct-2014

@author: mayank
'''

'''
Importing required libraries
'''
import socket
import time
import threading
import sys
from os import curdir, sep, linesep
class GBNServer:
   #Constructor to intialize the variables 
    def __init__(self,host='localhost', sport=10001, dport=9090):
        self.last_sent_ackn=-1 #Last acknownlegded sequence number
        self.expected_seqn=0 #Expected packet sequence number
        self.N= 6 # Window size of the server
        self.num_active=0 # Specifies the number of packets in window
        self.writeptr=0 #Write pointer to write packets to file
        self.rwindow=[None] * self.N
        self.filetowrite=open(filetosave,'a')
        #Starts the socket to listen to client
        self.client_address = (host, dport)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host,sport))
        self.counter = 0
        
    '''
    Function to remove the Packet from Window
    '''
    def removeFromWindow(self,byte):
    	index=self.rwindow.index(byte)
    	#print 'index', index
    	self.rwindow[index]=None
    	self.num_active=self.num_active-1
    	
    '''
    Funtion to Return the sequence number of the datagram
    '''
    def seqno(self,datagram):
        return int(datagram.split('||||')[0])	# |||| is used as the delimiter between sequence number and data
    
    '''
    Function to Return the data part of the datagram
    '''
    def data(self,datagram):
        return datagram.split('||||')[2]	
    
    '''
    Function to Check to see if space is available in window to add new packet
    '''
    def canAddToWindow(self):
	    return self.num_active < self.N
	    
    '''
    Function to create a datapacket to be sent
    '''
    def mkDatagram(self,seqno,winsize):
        return str(seqno)+'||||'+str(winsize)# acknowledges with variable window
	
    '''
    Function to Add packets to the window
    '''
    def addToWindow(self,datagram):
    	seqn=self.seqno(datagram)
    	if(self.rwindow[seqn%self.N]==None):
                if(self.seqno(datagram)==self.expected_seqn):
                    print 'Received Packet No.', self.seqno(datagram)
                    self.logf.write(str(time.time())+" [s] "+str(self.seqno(datagram))+" Received\n")
                    self.rwindow[seqn%self.N] = datagram
                    self.num_active=self.num_active+1
                elif(self.seqno(datagram)>self.expected_seqn):
                    print 'Packet Added to window buffer', self.seqno(datagram)
                    self.rwindow[seqn%self.N] = datagram
                    self.num_active=self.num_active+1
        #Discarding Existing packets
    	else:
            print 'Already in window buffer', self.seqno(datagram)
    		
    '''
    Function to send acknowledgement to the client
    '''
    def sendAck(self,datagram, counter):
    	self.last_sent_ackn = self.seqno(datagram)+counter
    	if(counter==0):
            print 'Sending Ack for Packet No.', self.seqno(datagram)
            self.sock.sendto(str(datagram),self.client_address)
            self.logf.write(str(time.time())+" [s] "+str(self.seqno(datagram))+" Ack\n")
        elif(counter>0):
            print 'Sending CumulativeAck for Packet No.', self.seqno(datagram)
            self.sock.sendto(str(datagram),self.client_address)
            self.logf.write(str(time.time())+" [s] "+str(self.seqno(datagram))+" Ack\n")

    '''
    Function to write the packets from window to file
    '''
    def writeMessage(self):
                #print 'writing to file', self.rwindow[self.writeptr]
                #print 'weiteptr', self.writeptr
		self.filetowrite.write(self.data(self.rwindow[self.writeptr]))
		self.removeFromWindow(self.rwindow[self.writeptr])
		self.writeptr +=1
		if (self.writeptr>=self.N):
                    self.writeptr = 0
    
    '''
    Recieves the packets from client		
    '''
    def receiveMessage(self):
    	while 1:
    		datagram,addr =self.sock.recvfrom(4096)
    		#EOF sequence to stop the server
    		if (datagram=='|!@#$%^&'):
    		    self.filetowrite.close()
    		    break
    		#Add to window if there is space in window and if sequence number is excpected sequence
    		elif self.seqno(datagram)==self.expected_seqn:
    			if(self.canAddToWindow()==True):
    				self.addToWindow(datagram)
    				counter = 0
                                while(self.rwindow[(self.seqno(datagram)+counter)%self.N]!=None):
                                    #print '            DATA in window', self.rwindow[(self.seqno(datagram)+counter)%self.N]
                                    self.writeMessage()
                                    #print '            counter', counter
                                    counter +=1
    				datagram=self.mkDatagram(self.expected_seqn+counter-1,self.N)
    			#self.writeMessage()
                        self.sendAck(datagram, counter-1)
                        if (counter == 0):
                            self.expected_seqn=self.expected_seqn+1
                        else:
                            self.expected_seqn=self.expected_seqn+counter
    		else:
                    #For Buffering out of order packets
                    if(self.canAddToWindow()==True):
                        self.addToWindow(datagram)
'''
Function to tell user how to input command in terminal    					
'''
def usage():
    sys.stdout = sys.stderr
    print 'Type the following command in terminal'
    print 'GBNserver.py [filename.extension]'
    sys.exit(2)
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
		usage()
    else:
        
        fName = 'serverLog.txt'
        filetosave= str(sys.argv[1])
        server=GBNServer()# Create server object
        server.logf = open(curdir + sep + fName, 'w+')
        server.receiveMessage()
        server.logf.close()

