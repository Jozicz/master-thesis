import serial
import os, time, sys
import posix

pipe_name = '/tmp/test'
global commandSeries
commandSeries = ''

ser=serial.Serial("/dev/ttyACM0",115200)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=115200

def sendPipe(message):
    pipeout = os.open(pipe_name, os.O_WRONLY)
    time.sleep(1)
    os.write(pipeout, message)

def commandCheck(message):
    global commandSeries
    if 'exit' in message:
        commandSeries = ''
    elif 'check state' in message:
        commandSeries = commandSeries + '1'
    elif 'which bathroom' in message:
        commandSeries = commandSeries + '2'
    elif 'switch alarm' in message:
        commandSeries = commandSeries + '3'
    elif 'first' in message:
        if commandSeries == '1' or commandSeries == '2':
            commandSeries = commandSeries + '5'
    elif 'second' in message:
        if commandSeries == '1' or commandSeries == '2':
            commandSeries = commandSeries + '6'
    elif 'third' in message:
        if commandSeries == '1':
            commandSeries = commandSeries + '7'
    elif 'fourth' in message:
        if commandSeries == '1':
            commandSeries = commandSeries + '8'
    elif 'all' in message:
        if commandSeries == '1':
            commandSeries = commandSeries + '11'
    elif 'temperature' in message:
        if commandSeries == '25' or commandSeries == '26':
            commandSeries = commandSeries + '9'
    elif 'humidity' in message:
        if commandSeries == '25' or commandSeries == '26':
            commandSeries = commandSeries + '10'
    elif 'on' in message:
        if commandSeries == '3':
            commandSeries = commandSeries + '12'
    elif 'off' in message:
        if commandSeries == '3':
            commandSeries = commandSeries + '13'

if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)

while True:
    read_ser=ser.readline()
    read_ser=read_ser.lower()
    commandCheck(str(read_ser))
    
    if commandSeries == '15':
        sendPipe(b'1\n')
        commandSeries = ''
    elif commandSeries == '16':
        sendPipe(b'2\n')
        commandSeries = ''
    elif commandSeries == '17':
        sendPipe(b'3\n')
        commandSeries = ''
    elif commandSeries == '18':
        sendPipe(b'4\n')
        commandSeries = ''
    elif commandSeries == '111':
        sendPipe(b'5\n')
        commandSeries = ''
    elif commandSeries == '259':
        sendPipe(b'6\n')
        commandSeries = ''
    elif commandSeries == '2510':
        sendPipe(b'7\n')
        commandSeries = ''
    elif commandSeries == '269':
        sendPipe(b'8\n')
        commandSeries = ''
    elif commandSeries == '2610':
        sendPipe(b'9\n')
        commandSeries = ''
    elif commandSeries == '312':
        sendPipe(b'10\n')
        commandSeries = ''
    elif commandSeries == '313':
        sendPipe(b'11\n')
        commandSeries = ''
