from kivy.support import install_twisted_reactor

install_twisted_reactor()

x = []
y = []
z = []

# A simple Client that send messages to the echo server
from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        self.factory.app.datarecv(data)


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        self.app.print_message("connection lost")

    def clientConnectionFailed(self, conn, reason):
        rd = str(reason)
        st = ""
        st += rd[:len(rd) / 2 - 1]
        st += "\n"
        st += rd[len(rd) / 2 - 1:]
        self.app.print_message("connection failed" + " reason: \n" + st)


from kivy.lang import Builder
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from plyer import accelerometer
from plyer import tts
from kivy.uix.textinput import TextInput

Window.clearcolor = (1, 1, 1, 1.)


class GUI(BoxLayout):
    def __init__(self, app):
        super(GUI, self).__init__(orientation='vertical')
        self.app = app
        self.label = Label(text='Connecting To Server...', color=(0, 0, 0, 1), halign='center', valign='middle')

        bl = BoxLayout(orientation='vertical')
        self.ti = TextInput(multiline=False, size_hint_y=0.3)
        bn = Button(text="Start", size_hint_y=0.3)
        bn.bind(on_press=self.connect)
        bl.add_widget(self.ti)
        bl.add_widget(bn)
        self.pp = Popup(title='Enter IP Address of Server:',
                        content=bl)
        self.pp.open()

    def readactivity(self, activity):
        activity = activity.split("*****")
        activity = activity[0]
        msg = str("You are " + activity)
        try:
            tts.speak(msg)
        except NotImplementedError:
            print "Error!"

    def connect(self, btn):
        ip = self.ti.text
        self.app.connect_to_server(ip)
        self.pp.dismiss()
        self.add_widget(self.label)


class ActivityRecognitionApp(App):
    def build(self):
        self.gui = GUI(self)
        return self.gui

    def connect_to_server(self, ip):
        reactor.connectTCP(ip, 8000, EchoFactory(self))


    def datarecv(self, data):
        self.gui.readactivity(data)

    def on_connection(self, connection):
        self.print_message("connected succesfully!")
        self.connection = connection
        try:
            accelerometer.enable()
            Clock.schedule_interval(self.send_acceleration, 1 / 50.)
        except NotImplementedError:
            import traceback

            traceback.print_exc()

    def send_message(self, msg):
        if msg and self.connection:
            self.connection.write(msg)


    def print_message(self, msg):
        self.gui.label.text += "\n" + msg

    def send_acceleration(self, dt):
        global x, y, z
        val = accelerometer.acceleration[:3]
        x.append(str(val[0]))
        y.append(str(val[1]))
        z.append(str(val[2]))

        if len(x) == 2:
            msg = "^^^^^^^^^^ |" + '|'.join(x) + "|" + " ********** |" + '|'.join(y) + "|" + " ********** |" + '|'.join(z) + "| ##########"
            self.send_message(msg)
            x = []
            y = []
            z = []


if __name__ == '__main__':
    ActivityRecognitionApp().run()
