import pickle
import tkinter

from kivy.support import install_twisted_reactor

from client import ChatClientFactory
from config import HOST
install_twisted_reactor()
from kivy.app import App
from twisted.internet import reactor


class ChatApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.factory = ChatClientFactory(self)
        reactor.connectTCP(HOST, 9096, self.factory)

    def on_connect(self, conn):
        self.conn = conn
        # self.root.current = 'chatroom'

    def send_msg(self):
        msg = self.root.ids.message.text
        data = {'func': 'CHAT', 'body': msg}
        data = pickle.dumps(data)
        self.conn.write(data)
        self.root.ids.chat_logs.text += ('%s says: %s\n' % (self.nick, msg))
        self.root.ids.message.text = ''

    def on_message(self, msg):
        data = msg.decode('gbk')
        if data == '1':
            self.root.current = 'chatroom'
            self.root.ids.username.text = ''
            self.root.ids.pwd1.text = ''
            self.root.ids.pwd2.text = ''
            self.nick = self.root.ids.nickname.text
            self.root.ids.nickname.text = ''
            return
        elif data == '0' or data == '-1':
            return
        self.root.ids.chat_logs.text += data + '\n'

    def disconnect(self):
        if self.conn:
            self.conn.loseConnection()
            del self.conn
        self.root.current = 'login'
        self.root.ids.chat_logs.text = ''

    def register(self):
        tk = tkinter.Tk()
        username = self.root.ids.username.text
        pwd1 = self.root.ids.pwd1.text
        pwd2 = self.root.ids.pwd2.text
        nickname = self.root.ids.nickname.text
        if not all([username, pwd1, pwd2, nickname]):
            tkinter.messagebox.showinfo('不能为空')
            tk.destroy()
            return
        if pwd1 != pwd2:
            tkinter.messagebox.showwarning('密码不一致')
            tk.destroy()
            return
        data = {'func': 'REGISTER',
                'body': {
                    'username': username,
                    'pwd1': pwd1,
                    'pwd2': pwd2,
                    'nickname': nickname}}
        data = pickle.dumps(data)
        self.conn.write(data)

    def swap_register(self):

        self.root.current = 'register'

    def login(self):
        tk = tkinter.Tk()
        username = self.root.ids.account
        password = self.root.ids.pwd
        if not all([username, password]):
            tkinter.messagebox.showinfo('不能为空')
            tk.destroy()
        params = {
            'func': 'LOGIN',
            'body': {
                'username': username,
                'password': password
            }
        }
        data = pickle.dumps(params)
        self.conn.write(data)


    def swap_login(self):
        self.root.current = 'login'


if __name__ == '__main__':
    ChatApp().run()
