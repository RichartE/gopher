
import sys, socket, tty

class Line:
    def __init__(self, type, title, x, server, port):
        self.type = type
        self.title = title
        self.x = x
        self.server = server
        self.port = port

class GopherClient:
    def __init__(self):
        self.options = []
        #self.server = raw_input("What server are we connecting to?\n")
        #self.port = input("What port are we connecting to?\n")
        self.server = "localhost"
        self.port = 50000
        self.back = []
        self.type = 1
        self.title = "back"
        sys.stdout.write(u"\u001b[2J")
        sys.stdout.write(u"\u001b[1000D")
        answer = self.request(self.server, self.port, "")
        self.options.append(Line(1, "back", "back", self.server, self.port))
        self.back.append("back")
        self.process(answer)
        move = self.display()
        self.main(move)
    
    def display(self):
        position = 0
        tty.setraw(sys.stdin)
        while True:
            linecount = 0
            for line in self.options:
                sys.stdout.write(u"\u001b[1000D")
                title = line.title.upper()
                if line.type == 1:
                    title = title + "..."
                if linecount == position:
                    print(u"\u001b[4m\u001b[46m" + title + u"\u001b[0m")
                else:
                    print(title)
                linecount += 1
                sys.stdout.write(u"\u001b[1000D")
            sys.stdout.write(u"\u001b[0m")
            sys.stdout.write(u"\u001b[" + str(len(self.options)) + "A")
            sys.stdout.write(u"\u001b[1000D")
            char = ord(sys.stdin.read(1))
            if char == 3:
                sys.stdout.write(u"\u001b[2J")
                sys.stdout.write(u"\u001b[1000D")
                sys.exit()
            elif char == 27:
                next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
                if next1 == 91:
                    if next2 == 65: # UP
                        position = max(0, position - 1)
                    elif next2 == 66: # DOWN
                        position = min(len(self.options) - 1, position + 1)
            elif char ==  13 or char == 10:
                sys.stdout.write(u"\u001b[2J")
                return position
            sys.stdout.flush()
    
    def main(self, move):
        moveTo = self.options[move]
        if moveTo.type == 0:
            back = Line(1, "back", self.title, self.server, self.port)
            answer = self.request(moveTo.server, moveTo.port, moveTo.x)
            sys.stdout.write(u"\u001b[1000D")
            print(answer)
            self.server = moveTo.server
            self.port = moveTo.port
            del self.options[:]
            self.options.append(back)
            self.back.append(self.title)
        else:
            if moveTo.title == "back":
                try:
                    prev = self.back.pop()
                except IndexError:
                    prev = "back"
                back = Line(1, "back", prev, self.server, self.port)
                answer = self.request(moveTo.server, moveTo.port, prev)
                self.title = prev
            else:
                answer = self.request(moveTo.server, moveTo.port, moveTo.x)
                back = Line(1, "back", moveTo.x, self.server, self.port)
                self.back.append(self.title)
                self.title = moveTo.x
            self.server = moveTo.server
            self.port = moveTo.port
            del self.options[:]
            self.options.append(back)
            self.process(answer)
        move = self.display()
        self.main(move)
        
    
    def request(self, serv, prt, msg):
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
        serverSock.send(message.encode("ascii"))

        returned = serverSock.recv(1024)
        serverSock.close()
        
        return returned.decode("ascii")
    
    def process(self, answer):
        answer = answer.split("\n")
        for line in answer:
            if line.startswith('.'):
                break
            type = 0
            title = ""
            x = ""
            server = ""
            port = 0
            if line.startswith("1"):
                type = 1
            filename = line.split("\t")
            title = filename[0][1:]
            x = filename[1]
            server = filename[2]
            port = int(filename[3])
            self.options.append(Line(type, title, x, server, port))

GopherClient()
        
