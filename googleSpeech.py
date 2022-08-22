import speech_recognition as sr
import pyttsx3
import os, sys, time

r = sr.Recognizer()
pipe_name = '/tmp/test'

def sendPipe(message):
    pipeout = os.open(pipe_name, os.O_WRONLY)
    time.sleep(1)
    os.write(pipeout, message)

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)

with sr.Microphone() as source:
    print("Silence please, calibrating background noise")
    r.adjust_for_ambient_noise(source, duration=2)
    print("Calibrated, now say something!")
while(1):
    with sr.Microphone() as source:
        audio = r.listen(source)

        MyText = r.recognize_google(audio)
        MyText = MyText.lower()
        print(MyText)
    
        if "first window" in MyText:
            sendPipe(b'1\n')
            time.sleep(2)
            os.system('clear')
            print("Speak now...")
        elif "second window" in MyText:
            sendPipe(b'2\n')
            time.sleep(2)
            os.system('clear')
            print("Speak now...")
        elif "third window" in MyText:
            sendPipe(b'3\n')
            time.sleep(2)
            os.system('clear')
            print("Speak now...")
        elif "fourth window" in MyText:
            sendPipe(b'4\n')
            time.sleep(2)
            os.system('clear')
            print("Speak now...")
        elif "all windows" in MyText:
            sendPipe(b'5\n')
            time.sleep(6)
            os.system('clear')
        elif "first bathroom" in MyText:
            sendPipe(b'12\n')
            time.sleep(10)
            os.system('clear')
            print("Speak now...")
        elif "second bathroom" in MyText:
            sendPipe(b'13\n')
            time.sleep(10)
            os.system('clear')
            print("Speak now...")
        elif "switch on the alarm" in MyText:
            sendPipe(b'10\n')
            time.sleep(2)
            os.system('clear')
            print("Speak now...")
        elif "switch off the alarm" in MyText:
            sendPipe(b'11\n')
            time.sleep(2)
            os.system('clear')
            
#try:
#   print(r.recognize_google(audio))
#except sr.UnknownValueError:
#   print("Google Speech Recognition could not understand audio")
#except sr.RequestError as e:
#   print("Could not request results from Google Speech Recognition Service; {0}".format(e))

