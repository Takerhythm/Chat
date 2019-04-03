from twisted.internet import protocol


class ChatClient(protocol.Protocol):
    def connectionMade(self):
        # self.transport.write('CONNECT'.encode('gbk'))
        self.factory.app.on_connect(self.transport)

    def dataReceived(self, data):
        self.factory.app.on_message(data)

class ChatClientFactory(protocol.ClientFactory):
    protocol = ChatClient

    def __init__(self, app):
        self.app = app


