'''
A simple TCP "echo" server written in Python.

author:  Amy Csizmar Dalal and [YOUR NAMES HERE]
CS 331, Fall 2020
'''
import sys, socket, re

class File:
    def __init__(self):
        self.links = []
        self.message = ''
        file = open(".links", "r")
        for line in file:
            if line.startswith("0"):
                filename = re.split("\s{2,}", line)[1]
                self.links.append(filename)
            self.message = self.message + line
        self.message = self.message + "."
        
class TCPServer:
    def __init__(self, port=50000):
        self.port = port
        self.host = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.file = File()

    def listen(self):
        self.sock.listen(5)

        while True:
            clientSock, clientAddr = self.sock.accept()
            print ("Connection received from ",  clientSock.getpeername())
            # Get the message and echo it back
            while True:
                data = clientSock.recv(1024)
                print ("Rm:  " + data.decode("ascii"))
                if not len(data):
                    break
                elif data.decode("ascii") == "__blank__":
                    clientSock.sendall(self.file.message)
                    break
                elif data.decode("ascii") in self.file.links:
                    clientSock.sendall(open(data.decode("ascii")).read())
                    break
                print ("Received message:  " + data.decode("ascii"))

                clientSock.sendall(data)
            clientSock.close()

def main():
    # Create a server
    if len(sys.argv) > 1:
        try:
            server = TCPServer(int(sys.argv[1]))
        except ValueError as e:
            print ("Error in specifying port. Creating server on default port.")
            server = TCPServer()
    else:
        server = TCPServer()

    # Listen forever
    print ("Listening on port " + str(server.port))
    server.listen()

main()
