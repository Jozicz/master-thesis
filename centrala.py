import struct
import os, sys, time
import pyttsx3
import ctypes as ct
import fcntl
from threading import Thread
from nonblock import nonblock_read
from RF24 import RF24, RF24_250KBPS, RF24_PA_HIGH
from RF24Network import RF24Network

pipe_name = '/tmp/test'
if not os.path.exists(pipe_name):
	os.mkfifo(pipe_name)

global line
line = ''

def readPipe():
    global line
    pipein = open(pipe_name, 'r')
    while True:
        line = pipein.readline()[:-1]
        commandResponse(line)

thread = Thread(target=readPipe)
thread.start()
   
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def commandResponse(code):
    global windows, temperatures, humidities, alarm
    if code == '1' or code == '2' or code == '3' or code == '4':
        x = windows[int(code) - 1]
        say = "Window " + code + " is "
        if x == 1:
            say = say + "closed"
        else:
            say = say + "open"
        SpeakText(say)
    elif code == '5':
        for x in range(4):
            say = "Window " + str(x+1) + " is "
            if windows[x] == 1:
                say = say + "closed"
            else:
                say = say + "open"
            SpeakText(say)
    elif code == '6' or code == '12':
        say = "The temperature in first bathroom is " + str(temperatures[0]) + " degrees celsius" 
        SpeakText(say)
    if code == '7' or code == '12':
        say = "The humidity in first bathroom is " + str(humidities[0]) + " percent" 
        SpeakText(say)
    elif code == '8' or code == '13':
        say = "The temperature in second bathroom is " + str(temperatures[1]) + " degrees celsius" 
        SpeakText(say)
    if code == '9' or code == '13':
        say = "The humidity in second bathroom is " + str(humidities[1]) + " percent" 
        SpeakText(say)
    elif code == '10':
        if alarm == 1:
            SpeakText("The alarm is already on")
        else:
            alarm = 1
            SpeakText("Alarm switched on")
    elif code == '11':
        if alarm == 0:
            SpeakText("The alarm is already off")
        else:
            alarm = 0
            SpeakText("Alarm switched off")

def printing(windows = [0, 0, 0, 0], voltages = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], temperatures = [0.0, 0.0], humidities = [0.0, 0.0]):
    os.system('clear')
    for i in range(4):
        print("Window ", i+1, ": ", end = ' ')
        if windows[i] == 1:
            print("closed", end = '')
        else:
            print("open!", end = '')
        print("\tVoltage: ", voltages[i], "V")
    for i in range(2):
        print("\nBathroom ", i+1, ":")
        print("Temperature: ", temperatures[i], "°C", "\nHumidity: ", humidities[i], "%", "\nVoltage: ", voltages[i+4], "V")

radio = RF24(25, 0)
network = RF24Network(radio)

this_node = 0o0

global windows, temperatures, humidities, alarm
windows = [0.0] * 4
voltages = [0.0] * 6
temperatures = [0.0] * 2
humidities = [0.0] * 2
alarm = 0

# initialize the radio
if not radio.begin():
    raise RuntimeError("radio hardware not responding")

radio.channel = 80
radio.setDataRate(RF24_250KBPS)
radio.setPALevel(RF24_PA_HIGH)

# initialize the network node
network.begin(this_node)

radio.printPrettyDetails()

radio.startListening()  # put radio in RX mode
try:
    while True:
        network.update()
        while network.available():
            header, var = network.read()
            
            val = struct.unpack('f', var)
            #print("payload length ", len(val))
            val = float(val[0])

            node = oct(header.from_node)
            #node = ct.c_uint16(node)
            if (node == '0o1' or node == '0o2' or node == '0o3' or node == '0o4'):
                if node == '0o1':
                    if (val == 0.0 or val == 1.0):
                        windows[0] = val
                    else:
                        voltages[0] = val
                if node == '0o2':
                    if (val == 0.0 or val == 1.0):
                        windows[1] = val
                    else:
                        voltages[1] = val
                if node == '0o3':
                    if (val == 0.0 or val == 1.0):
                        windows[2] = val
                    else:
                        voltages[2] = val
                if node == '0o4':
                    if (val == 0.0 or val == 1.0):
                        windows[3] = val
                    else:
                        voltages[3] = val
            else:
                if val > 1000.0:
                    val = val - 1000.0
                    val = float(f'{val:.2f}')
                    if val > 100.0:
                        val = val - 100.0
                        val = float(f'{val:.2f}')
                        humidities[0] = val
                    elif val < 8.0:
                        voltages[4] = val
                    else:
                        temperatures[0] = val
                else:
                    val = float(f'{val:.2f}')
                    if val > 100.0:
                        val = val - 100.0
                        val = float(f'{val:.2f}')
                        humidities[1] = val
                    elif val < 8.0:
                        voltages[5] = val
                    else:
                        temperatures[1] = val
            printing(windows, voltages, temperatures, humidities)
	
except KeyboardInterrupt:
    print("powering down radio and exiting.")
    radio.powerDown()
