'''
A simple "echo" client written in Python.

author:  Amy Csizmar Dalal and [YOUR NAMES HERE]
CS 331, Fall 2020
'''
import sys, socket

def usage():
    print ("Usage:  python SimpleTCPClient <server IP> <port number> <message>")
    sys.exit()

def main(serv, prt, msg):
    # Process command line args (server, port, message)

    try:
        server = serv
        port = prt
        if msg == "":
            message = "__blank__"
        else:
            message = msg
    except ValueError as e:
        usage()

    serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSock.connect((server, port))
    print ("Connected to server; sending message")

    serverSock.send(message.encode("ascii"))
    print ("Sent message; waiting for reply")

    returned = serverSock.recv(1024)
    print ("Received reply: "+ returned.decode("ascii"))

    serverSock.close()
    
    return returned.decode("ascii")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        usage()
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
