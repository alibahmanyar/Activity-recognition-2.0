from kivy.uix.floatlayout import FloatLayout
from kivy.support import install_twisted_reactor
import threading

install_twisted_reactor()
from time import time
from functions import predict, Save_acc, predict_activity
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from twisted.internet import reactor
from twisted.internet import protocol
from kivy.graphics import Rectangle
from kivy.clock import Clock

Window.clearcolor = (1, 1, 1, 1.)
gh = open("1.txt", "w")
gh.write('')
gh.close()
msgcounter = 0


class EchoProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        # if response:
        # self.transport.write(response)


class EchoFactory(protocol.Factory):
    protocol = EchoProtocol

    def __init__(self, app):
        self.app = app


class GUI(FloatLayout):
    def __init__(self, app):
        super(GUI, self).__init__()
        self.app = app
        self.lb = Label(text='Nothing happened yet!', color=(0, 0, 0, 1), markup=True, halign='center', valign='middle')
        self.connect=False
        self.accdatasx = []
        self.accdatasy = []
        self.accdatasz = []
        self.add_widget(self.lb)
        Clock.schedule_interval(self.make_thread_predict_activity, 2.56)

    def make_thread_predict_activity(self, dt):
        if self.connect:
            thread2 = predict_activity(2, "Activity_predictor" , self)
            thread2.start()

    def showactivity(self, activity):
        self.canvas.clear()
        with self.canvas:
            Rectangle(source=("%s.png" % activity.lower()), pos=(
                Window.width / 2.0 - ((Window.height / 2.0) / 2.0),
                Window.height / 2.0 - ((Window.height / 2.0) / 2.0)),
                      size=(Window.height / 2.0, Window.height / 2.0))

    def on_massege_received(self, message):
        # print "Message:", message
        thread = Save_acc(1, "Msg_saver", message)
        thread.start()


class ServerApp(App):
    def build(self):
        self.lastactivity = "Nothing"
        self.gui = GUI(self)
        reactor.listenTCP(3236, EchoFactory(self))
        return self.gui

    def on_connection(self, connection):
        self.print_message("connected succesfully!")
        self.gui.connect=True
        self.connection = connection

    def handle_message(self, msg):
        self.gui.on_massege_received(msg)

    def sendactivity(self, activity):
        if activity != self.lastactivity:
            self.lastactivity = activity
            if activity and self.connection:
                msg = str(activity).replace("_", " ") + "\n"
                self.connection.write(msg)

    def print_message(self, msg):
        self.gui.lb.text += "\n" + msg


if __name__ == '__main__':
    ServerApp().run()
