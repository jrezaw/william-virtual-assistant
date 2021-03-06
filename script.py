import aiml
import os
import time, sys
import pyttsx3
import warnings
import threading
import pocketsphinx
from os import system
from PyQt4 import QtCore,QtGui
import speech_recognition as sr
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QApplication, QLabel, QMovie, QPainter, QFontMetrics 
import urllib


try:
    from urllib.request import urlretrieve
except ImportError:
     from urllib import urlretrieve

r = sr.Recognizer()
mode = "voice"
if len(sys.argv) > 1:
    if sys.argv[1] == "--voice" or sys.argv[1] == "voice":
        try:
            import speech_recognition as sr
            mode = "voice"
        except ImportError:
            print("\nInstall SpeechRecognition to use this feature.\nStarting text mode\n")
terminate = ['bye','buy','shutdown','exit','quit','gotosleep','goodbye']


class QTextMovieLabel(QLabel):
    
    def __init__(self, fileName):
        QLabel.__init__(self)
        thread = Thread(self)
        m = QMovie(fileName)
        m.start()
        self.setMovie(m)
        app.aboutToQuit.connect(thread.stop)
        thread.start()

    def setMovie(self, movie):
        QLabel.setMovie(self, movie)
        s=movie.currentImage().size()
        self._movieWidth = s.width()
        self._movieHeight = s.height()

class Thread(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)
        self.window = parent
        self._lock = threading.Lock()
        self.running = True

    def run(self):
        self.running = True
        

        def speak(jarvis_speech):
           tts = gTTS(text=jarvis_speech, lang='en')
           tts.save('jarvis_speech.mp3')
           mixer.init()
           mixer.music.load('jarvis_speech.mp3')
           mixer.music.play()
           while mixer.music.get_busy():
               time.sleep(1)

        def offline_speak(jarvis_speech):
            engine = pyttsx3.init()
            engine.setProperty('rate', 175)
            engine.say(jarvis_speech)
            engine.runAndWait()

        def listen():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Talk to William: ")
                audio = r.listen(source)
            try:
                   print (r.recognize_sphinx(audio))
                   return  r.recognize_sphinx(audio)

            except sr.UnknownValueError:
                return(listen())
            except sr.RequestError as e:
                print("Could not request results from speech service; {0}".format(e))


        kernel = aiml.Kernel()
        if os.path.isfile("bot_brain.brn"):
            kernel.bootstrap(brainFile = "bot_brain.brn")
        else:
            kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
            
        while True:
            if mode == "voice":
                response = listen()
            else:
                response = raw_input("Talk to William : ")
            if response.upper().replace(" ","") in terminate:
                response = listen()    
            jarvis_speech = kernel.respond(response)
            print ("William: " + jarvis_speech)
            offline_speak(jarvis_speech)

    def stop(self):
        engine = pyttsx3.init()
        engine.say("goodbye reza")
        engine.runAndWait()
        self.running = False



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    l = QTextMovieLabel('William.gif')
    l.setWindowTitle("William")
    l.show()
    sys.exit(app.exec_())
