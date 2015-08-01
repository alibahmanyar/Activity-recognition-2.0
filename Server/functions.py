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
        data = self.data
        line = ""
        cr = 0
        f = True
        while cr < len(data) - 1:
            # print 1
            line += data[cr]
            if data[cr + 1] == "\n":
                f = False
                break

            cr += 1
        if f:
            return False
        if cr == len(data) - 2:
            data = ""
            try:
                acceleration_data = acceleration_data[cr + 2:]
            except:
                acceleration_data = ""
        else:
            data = data[cr + 2:]
            acceleration_data = acceleration_data[cr + 2:]
        print "Line:", line
        return line

    def run(self):

        while True:
            # print 2
            line = self.read_line()
            if line == False:
                break
            line_splited = line.split("|")
            self.x_data.append(line_splited[1])
            self.x_data.append(line_splited[2])
            self.x_data.append(line_splited[3])
        print "\n\nLists:\n\n"
        print self.x_data
        print self.y_data
        print self.z_data
        print "\n\n"

        # x_acc = self.x_data[:len(self.x_data) - (len(self.x_data) % 128)]
        # y_acc = self.y_data[:len(self.y_data) - (len(self.y_data) % 128)]
        # z_acc = self.z_data[:len(self.z_data) - (len(self.z_data) % 128)]
        #
        # x_acc = x_acc[ : :len(x_acc)/128]
        # y_acc = y_acc[ : :len(y_acc)/128]
        # z_acc = z_acc[ : :len(z_acc)/128]
        # activity = predict(x_acc, y_acc, z_acc)
        # self.gui.showactivity(activity)
        # self.gui.app.sendactivity(activity)



def processdata(rdata):
    pass
    # rdata = rdata.replace("\n", "")
    # if "##########" not in rdata or "^^^^^^^^^^" not in rdata or "**********" not in rdata or rdata.count("**********")<2:
    #         return False
    # if rdata.count("^^^^^^^^^^") > 1:
    #     rdata = rdata.split(" ##########")
    #     dataprs = []
    #     while '' in rdata:
    #         rdata.remove('')
    #     for i in range(len(rdata)):
    #         if not rdata[i].count("**********")<2 and "^^^^^^^^^^" in rdata[i] and "##########" not in rdata[i]:
    #             rdata[i]=rdata[i]+ " ##########"
    #         else:
    #             rdata[i]="False"
    #     for i in range(len(rdata)):
    #         r=processdata(rdata[i])
    #         if r!=False:
    #             dataprs.append(r)
    #     return dataprs
    # else:
    #
    #     if "##########" not in rdata or "^^^^^^^^^^" not in rdata or "**********" not in rdata or rdata.count("**********")<2 or rdata.count("^^^^^^^^^^")>1 or rdata.count("##########")>1:
    #         return False
    #     data = rdata[12:-11]
    #     data = data.split(" ********** ")
    #     data[0] = data[0].split("|")
    #     data[2] = data[2].split("|")
    #     data[1] = data[1].split("|")
    #     x = []
    #     y = []
    #     z = []
    #     for i in range(len(data[0])):
    #         if data[0][i] != "":
    #              x.append(float(data[0][i]) / 9.80665)
    #     for i in range(len(data[1])):
    #         if data[1][i] != "":
    #             y.append(float(data[1][i]) / 9.80665)
    #     for i in range(len(data[2])):
    #         if data[2][i] != "":
    #             z.append(float(data[2][i]) / 9.80665)
    #     return [x, y, z]


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
