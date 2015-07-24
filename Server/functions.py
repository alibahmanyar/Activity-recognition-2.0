import orange
import Orange
import pickle
import time

classifier = pickle.load(open('classifier - neural network.pck'))
recvstatus = 0
restrecv = 0


def processdata(rdata):
    rdata = rdata.replace("\n", "")
    if rdata.count("^^^^^^^^^^") > 1:
        rdata = rdata.split(" ##########")
        dataprs = []
        while '' in rdata:
            rdata.remove('')
        for i in range(len(rdata)):
            rdata[i]=rdata[i]+ " ##########"

        for i in range(len(rdata)):
            dataprs.append(processdata(rdata[i]))
        return dataprs
    else:
        data = rdata[12:-11]
        data = data.split(" ********** ")
        data[0] = data[0].split("|")
        data[2] = data[2].split("|")
        data[1] = data[1].split("|")
        x = []
        y = []
        z = []
        for i in range(len(data[0])):
            if data[0][i] != "":
                x.append(float(data[0][i]) / 9.81)
        for i in range(len(data[1])):
            if data[1][i] != "":
                y.append(float(data[1][i]) / 9.81)
        for i in range(len(data[2])):
            if data[2][i] != "":
                z.append(float(data[2][i]) / 9.81)

        return [x, y, z]


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