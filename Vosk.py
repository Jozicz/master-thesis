#!/usr/bin/env python3

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys, time
import pyttsx3

pipe_name = '/tmp/test'
q = queue.Queue()

def sendPipe(message):
    pipeout = os.open(pipe_name, os.O_WRONLY)
    time.sleep(1)
    os.write(pipeout, message)

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

global WAKE_UP
WAKE_UP = 0

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def commandScanner(sentence):
    global WAKE_UP
    if "window number one" in sentence:
        sendPipe(b'1\n');
        WAKE_UP = 0
    elif "window number two" in sentence:
        sendPipe(b'2\n');
        WAKE_UP = 0
    elif "window number three" in sentence:
        sendPipe(b'3\n');
        WAKE_UP = 0
    elif "window number four" in sentence:
        sendPipe(b'4\n');
        WAKE_UP = 0
    elif "each window" in sentence:
        sendPipe(b'5\n');
        WAKE_UP = 0
    elif "switch on the alarm" in sentence:
        sendPipe(b'10\n');
        WAKE_UP = 0
    elif "switch off the alarm" in sentence:
        sendPipe(b'11\n');
        WAKE_UP = 0
    elif "first bathroom" in sentence:
        sendPipe(b'12\n');
        WAKE_UP = 0
    elif "second bathroom" in sentence:
        sendPipe(b'13\n');
        WAKE_UP = 0

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(lang="en-us")

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            
            if not os.path.exists(pipe_name):
                os.mkfifo(pipe_name)
                
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    sentence = str(rec.Result())
                    if WAKE_UP == 1:
                        commandScanner(sentence)
                    if "helen" in sentence:
                        SpeakText("Yes?")
                        WAKE_UP = 1
                if dump_fn is not None:
                    dump_fn.write(data)

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
