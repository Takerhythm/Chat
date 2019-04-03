import pickle

import pymysql
from twisted.internet import protocol, reactor


transports = set()
con = pymysql.connect(host='127.0.0.1', user='root', password='mysql', database='chat', port=3306)
cursor = con.cursor()

class Chat(protocol.Protocol):
    def dataReceived(self, data):
        data = pickle.loads(data)
        print(data)
        if data['func'] == 'CHAT':
            return self.chat(data['body'])
        elif data['func'] == 'LOGIN':
            return self.login(data['body'])
        elif data['func'] == 'REGISTER':
            return self.register(data['body'])


    def register(self, params):
        username = params.get('username', None)
        pwd1 = params.get('pwd1', None)
        pwd2 = params.get('pwd2', None)
        nickname = params.get('nickname', None)
        if not all([username, pwd1, pwd2, nickname]):
            self.transport.write('0'.encode('gbk'))
            return
        if pwd1 != pwd2:
            self.transport.write('-1'.encode('gbk'))
            return
        sql = 'insert into user VALUES (0, username=%s, password=%s, nickname=%s)'
        cursor.execute(sql, [username, pwd1, nickname])
        con.commit()
        transports.add(self.transport)
        self.transport.write('1'.encode('gbk'))

    def login(self, data):
        username = data['username']
        password = data['password']
        transports.add(self.transport)
        pass

    def chat(self, data):
        cli, msg = data.split(':', 1)
        for transport in transports:
            if transport is not self.transport:
                transport.write('%s send %s' % (cli, msg))

class Main(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()

reactor.listenTCP(9096, Main())
reactor.run()