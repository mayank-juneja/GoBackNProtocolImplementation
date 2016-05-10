WebServer Program Version 1.0 19/10/2014
author: Mayank Juneja

OBJECTIVE
------------------
Overview:
1. An understanding of reliable transmission transport layer protocols
2. An understanding of cumulative acknowledgements
3. An understanding of sliding windows
4. An understanding of sequencing packets
5. An understanding of flow control

DESCRIPTION OF APPLICATION
-----------------------------------------------
- GoBackN protocol has been implemented to send data from client to server.
- Two python files named gbnClient.py and gbnServer.py have been created to act as a sender and reciever.
- Application creates two Log files named clientLog and serverLog to log activities at client and server.
- It also contains a configuration file where the datasize of sent packets can be initialized.
- A sample text file named 'sample1.txt' has been attached for testing purposes.

GENERAL USAGE NOTES
--------------------------------------
- Run .py file named gbnClient.py and gbnServer.py using command prompt.
- Write the name of file 'To Be Sent' and file 'To Be Creted' along with the above python file name. 
- Window Size of Client and Server can be modified in the init files of gbnClient.py and gbnServer.py, 
- Both sent and received files can be compared using md5sum.

TECHNICAL DETAILS OF THE APPLICATION
-------------------------------------
- This Version of Go Back N Protocol is developed using Python 2.7 on Windows OS
- This protocol is made to run on localhost and static port numbers have been assigned as 9090 and 10001 for carrying out two directional traffic.
- This Version  can recieve a maximum packet size of 4096 Bytes.
- The sequence '||||' is used as a seperator to extract packet parameters from the datagram packet. If data contains this same sequence then we might encounter an error.
- Application has been tested to handle large file sizes, reliability of sent and recieved files has been checked using md5sum on Ubuntu OS
- Implemented Functionalities are:
	- Reliably transfer a data file between a client and server despite possible packet losses(packet error rate will vary during our testing to evaluate the correctness of your protocol implementation)
	- Sliding windows at both the client and server with Cummulative Acknowledgements.
	- Timeouts with retransmission(set as 0.5 sec, can be changed in constructor of gbnClient).
	- Discarding of out of range packets
	- Buffering out of order packets
	- Window based flow control such that the receiver's advertised window size dynamically adjusts to the receiver's ability to process
- Negative Scenarios can be inplemented by making changes to sendDatagram() function in gbnClient.(uncomment random function and set indentation).

References
-----------------
- http://www.youtube.com/watch?v=9BuaeEjIeQI
- http://www.w3.org/Protocols/rfc1945/rfc1945
- http://www.pythonforbeginners.com/
- https://wiki.python.org/
- http://ilab.cs.byu.edu/python/socket/echoserver.html
- Professor's Mail Subject:[TLEN5330-001] TLEN 5330: Programming Assignment #2 Sample Code and Instructions (Due Oct. 12) Dated:Oct 02 2014
----------------------------------------------------------------------------------------------------------------------------
Mayank Juneja can be reached at:

Voice:	530-820-2311
E-mail:	mayank.juneja@colorado.edu
