from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

 
class IphoneChat(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)
        self.currentCleint = self
        print "clients are ", self.factory.clients
 
    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        a = data.split(':')
        print a
        if len(a) > 1:
            command = a[0]
            content = a[1]
 
            msg = ""
            if command == "iam":
                self.name = content
                self.curr_clients[self.name] = self
                msg = self.name + " has joined"
                self.message(msg)
 
            elif command == "msg":
                msg = self.name + ": " + content
                print msg
                self.message(msg)
            else:
                if command in self.curr_clients:
                    self.curr_clients[command].message(self.name +": "+ content)
            
            #for c in self.factory.clients:
            #    if self.currentCleint == c:
            #        print c
            #        c.message(msg)
                
    def message(self, message):
        self.transport.write(message + '\n')
 
factory = Factory()
factory.protocol = IphoneChat
factory.clients = []
factory.protocol.curr_clients = {}
reactor.listenTCP(80, factory)
print "Iphone Chat server started"
reactor.run()