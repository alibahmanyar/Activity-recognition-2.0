from kivy.uix.floatlayout import FloatLayout
from kivy.support import install_twisted_reactor

install_twisted_reactor()

from functions import processdata, predict
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from twisted.internet import reactor
from twisted.internet import protocol
from kivy.graphics import Rectangle

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
        self.accdatasx = []
        self.accdatasy = []
        self.accdatasz = []
        self.add_widget(self.lb)

    def showactivity(self, activity):
        self.canvas.clear()
        with self.canvas:
            Rectangle(source=("%s.png" % activity.lower()), pos=(
                Window.width / 2.0 - ((Window.height / 2.0) / 2.0),
                Window.height / 2.0 - ((Window.height / 2.0) / 2.0)),
                      size=(Window.height / 2.0, Window.height / 2.0))


    def show_acceleration(self, val):

        if not "None" in val:
            dt = processdata(val)
            if isinstance(dt[0][0], list):
                for i in range(len(dt)):
                    for j in range(len(dt[i][0])):
                        self.accdatasx.append(str(float(dt[i][0][j])))
                        self.accdatasy.append(str(float(dt[i][1][j])))
                        self.accdatasz.append(str(float(dt[i][2][j])))
            else:
                for i in range(len(dt[0])):
                    self.accdatasx.append(str(float(dt[0][i])))
                    self.accdatasy.append(str(float(dt[1][i])))
                    self.accdatasz.append(str(float(dt[2][i])))
        if len(self.accdatasx) >= 128:
            activity = predict(self.accdatasx[-128:], self.accdatasy[-128:], self.accdatasz[-128:])
            self.accdatasx = self.accdatasx[-129:]
            self.accdatasy = self.accdatasy[-129:]
            self.accdatasz = self.accdatasz[-129:]
            if activity != "Error":
                self.showactivity(activity)
                self.app.sendactivity(activity)


class ServerApp(App):
    def build(self):
        self.lastactivity = "Nothing"
        self.gui = GUI(self)
        reactor.listenTCP(3236, EchoFactory(self))
        return self.gui

    def on_connection(self, connection):
        self.print_message("connected succesfully!")
        self.connection = connection

    def handle_message(self, msg):
        self.gui.show_acceleration(msg)

    def sendactivity(self, activity):
        if activity != self.lastactivity:
            self.lastactivity = activity
            if activity and self.connection:
                msg = str(activity).replace("_", " ") + "*****"
                self.connection.write(msg)

    def print_message(self, msg):
        self.gui.lb.text += "\n" + msg


if __name__ == '__main__':
    ServerApp().run()
