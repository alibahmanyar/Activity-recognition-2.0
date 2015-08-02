import orange
import Orange
import pickle
import time
import threading

classifier = pickle.load(open('classifier - neural network.pck'))
recvstatus = 0
restrecv = 0

acceleration_data = ""


class Save_acc(threading.Thread):
    def __init__(self, threadID, name, message):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.message = message

    def run(self):
        global acceleration_data
        acceleration_data += self.message


class predict_activity(threading.Thread):
    def __init__(self, threadID, name, gui):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.line_number = 0
        self.data = acceleration_data
        self.x_data = []
        self.y_data = []
        self.z_data = []
        self.gui = gui

    def read_line(self):
        global acceleration_data

        line = ""
        cr = 0
        f = True
        while cr < len(self.data) - 1:

            line += self.data[cr]
            if self.data[cr + 1] == "\n":
                f = False
                break

            cr += 1
        if f:
            return False
        if cr == len(self.data) - 2:
            self.data = ""
            try:
                acceleration_data = acceleration_data[cr + 2:]
            except:
                acceleration_data = ""
        else:
            self.data = self.data[cr + 2:]
            acceleration_data = acceleration_data[cr + 2:]

        return line

    def run(self):
        while True:

            line = self.read_line()
            if not line:
                break
            line_splited = line.split("|")
            self.x_data.append(line_splited[1])
            self.y_data.append(line_splited[2])
            self.z_data.append(line_splited[3])

        x_acc = self.x_data[:len(self.x_data) - (len(self.x_data) % 128)]
        y_acc = self.y_data[:len(self.y_data) - (len(self.y_data) % 128)]
        z_acc = self.z_data[:len(self.z_data) - (len(self.z_data) % 128)]

        x_acc = x_acc[::len(x_acc) / 128]
        y_acc = y_acc[::len(y_acc) / 128]
        z_acc = z_acc[::len(z_acc) / 128]

        x_acc = [str(float(ol) / 9.80665) for ol in x_acc]
        y_acc = [str(float(ol) / 9.80665) for ol in y_acc]
        z_acc = [str(float(ol) / 9.80665) for ol in z_acc]

        activity = predict(x_acc, y_acc, z_acc)
        self.gui.showactivity(activity)
        self.gui.app.sendactivity(activity)


def write(x, y, z):
    csvfile = open("datax.csv", "w")
    firstr = ""
    for i in range(1, 129):
        firstr += "X" + str(i) + ","
    for i in range(1, 129):
        firstr += "Y" + str(i) + ","
    for i in range(1, 129):
        firstr += "Z" + str(i) + ","
    firstr = firstr[:-1] + "\n"
    csvfile.write(firstr)

    csvfile.write(','.join(x) + ',' + ','.join(y) + ',' + ','.join(z) + '\n')

    csvfile.close()


def predict(x, y, z):
    global classifier
    try:

        write(x, y, z)

        data = Orange.data.Table("datax")

        for inst in data:
            prediction = classifier(inst)
            # print "Prediction:", prediction, "\n"
            return str(prediction)

    except Exception as e:
        errorfile = open("Errored Data (predicting).txt", "a")
        errorfile.write(str(x) + "\n" + "\n" + "\n" + str(y) + "\n" + "\n" + "\n" + str(z) + "\n" + "\n" + "\n\n\n\n")
        errorfile.close()
        print "\n\n\n" + "An error occurred in predicting!" + "\n\n\n"
        print e

        return "Error"
