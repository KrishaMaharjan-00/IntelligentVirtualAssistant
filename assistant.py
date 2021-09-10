import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import cv2
import random
from requests import get
import pywhatkit as kit
import smtplib
import sys
import time
import pyjokes
import pyautogui
import requests
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from gui_assistant import Ui_Intelligent_Virtual_Assistant
from bs4 import BeautifulSoup




dict = {'dad':'prettygal.krisha@gmail.com','college':'prettygal.krisha@gmail.com','krisha':'prettygal.krisha@gmail.com'}


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

#text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=f16bed9c75d548588051776e582055c9'
    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first","second"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")


def wishMe():
    hour = int(datetime.datetime.now().hour)
    minute = int(datetime.datetime.now().minute)
    second = int(datetime.datetime.now().second)
    if hour>=0 and hour<12:
        speak('Good Morning!')
    elif hour>=12 and hour<18:
        speak('Good Afternoon!')
    else:
        speak('Good Evening!')
    speak(f"It's {hour} hour and {minute} minute and {second} second")
    speak("Hi I am V, please tell me how i may help you")


def sendEmail(to,content):

    server = smtplib.SMTP('smtp.gmail.com',587) # create a SMTP object for connection with server
    server.ehlo()
    server.starttls() #TLS connection required by gmail
    server.login('vindemo1230@gmail.com','vin.demo21')
    server.sendmail('sender@gmail.com',to,content) # from, to, content


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()


    def run(self):
        self.taskExecution()


    #to convert voice into text
    def takeCommand(self):
        #it takes microphone input from the user and returns string output
        r= sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening......')
            r.pause_threshold = 1
            #r.energy_threshold = 300
            audio = r.listen(source, timeout=1, phrase_time_limit=5)
            #we can also use r.record(source, duration=1, offset=5)
            r.adjust_for_ambient_noise(source)

        try:
            print('Recognizing.....')
            query = r.recognize_google(audio, language='en-in')
            print(f"You said: {query}\n")

        except Exception as e:
            #print(e)
            speak('say that again please...')
            return "None"
        return query


    def taskExecution(self):
        wishMe()
        while True:
        # if 1:
            self.query = self.takeCommand().lower()

            #logic for executing tasks based on query

            if 'wikipedia' in self.query:
                speak('Searching Wikipedia....')
                query = self.query.replace("wikipedia","")
                results = wikipedia.summary(query, sentences=2)
                speak('According To Wikipedia')
                print(results)
                speak(results)

            elif 'open command prompt' in self.query:
                os.system("start cmd")
            
            elif 'open camera' in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img= cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k==27:
                        break
                cap.release()
                cv2.destroyAllWindows()

            elif 'open youtube' in self.query:
                webbrowser.open("youtube.com")

            elif 'open stackoverflow' in self.query:
                webbrowser.open("stackoverflow.com")

            elif 'open facebook' in self.query:
                webbrowser.open("facebook.com")

            elif 'open google' in self.query:
                speak('Mam, what should i search on google')
                cm = self.takeCommand().lower()
                webbrowser.open(f"{cm}")

            elif 'send message' in self.query:
                kit.sendwhatmsg("+9779840021911","this is testing protocol",12,11)

            elif 'play music' in self.query:
                music_dir = "C:\\Users\\ghk\\Music\\bts"
                songs = os.listdir(music_dir)
                #print(songs)
                rd = random.choice(songs)
                # for song in songs:
                #     if song.endswith('.mp3'):
                os.startfile(os.path.join(music_dir,rd))

            elif 'ip address' in self.query:
                ip = get('https://api.ipify.org').text
                print(ip)
                speak(f"Your Ip Address Is {ip}")

            elif 'switch the window' in self.query:
                pyautogui.keyDown('alt')
                pyautogui.press('tab')
                time.sleep(1)
                pyautogui.keyUp('alt')
    
            elif 'play songs on youtube' in self.query:
                kit.playonyt("crystal snow")


            elif 'write down something' in self.query:
                speak("what should i write down mam?")
                note = self.takeCommand()
                remember = open("data.txt", "w")
                remember.write(note)
                remember.close()
                speak("I have noted that " + note)

            elif 'do you have anything' in self.query:
                remember = open("data.txt", "r").read()
                speak("You told me to remember that " + remember)    


            elif 'open notepad' in self.query:
                path = 'C:\\Windows\\System32\\notepad.exe'
                os.startfile(path)

            elif 'the time' in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Mam, The time is {strTime}")

            elif 'email to' in self.query:
                
                # speak("Mam Simple Message Or Meassage With File")
                # self.query = self.takeCommand().lower()
                # if 'Simple Meassage' in self.query:
                try:
                    name = list(self.query.split()) # extract receiver's name
                    name = name[name.index('to')+1]
                    speak("what should i say?")
                    content = self.takeCommand().lower()
                    to = dict[name]
                    sendEmail(to,content)
                    speak("email has been sent")

                except Exception as e:
                    print(e)
                    speak("sorry unable to send the email at the moment.Try again")

                # if 'With File' in self.query:
                #     try:
                #         name = list(self.query.split()) # extract receiver's name
                #         name = name[name.index('to')+1]
                #         to = dict[name]
                #         speak('okay mam, what is the subject for this email')
                #         self.query = self.takeCommand().lower()
                #         subject = self.query
                #         speak('and mam, what is the message for this email')
                #         self.query2 = self.takeCommand().lower()
                #         message = self.query2
                #         speak('mam, please enter the correct path of the file in the shell')
                #         file_location = input("please enter the path here")


                #         speak("Please Wait I am sending mail now")

                #         msg = MIMEMultipart()
                #         msg['From'] = name
                #         msg['To'] = to
                #         msg['Subject'] = subject


                #         msg.attach(MIMEText(message, 'plain'))


                #         filename = os.path.basename(file_location)
                #         attachment = open(file_location, "rb")
                #         part = MIMEBase('application','octet-stream')
                #         part.set_payload(attachment.read())
                #         encoders.encode_base64(part)
                #         part.add_header('Content-Disposition',"attachment; filename= %s" % filename)

                #         msg.attach(part)

                #         server = smtplib.SMTP('smtp.gmail.com',587) # create a SMTP object for connection with server
                #         server.ehlo()
                #         server.starttls() #TLS connection required by gmail
                #         server.login('vindemo1230@gmail.com','vin.demo21')
                #         server.sendmail('sender@gmail.com',to,text)
                #         server.quit()
                #         speak("email has been sent")

                #     except Exception as e:
                #         print(e)
                #         speak("sorry unable to send the email at the moment.Try again")
            elif 'weather' in self.query:
                search = "temperature in kathmandu"
                url = f"https://www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text,"html.parser")
                temp = data.find("div" ,class_="BNeawe").text
                speak(f"current {search} is {temp}")

            # to close any application
            elif 'close notepad' in self.query:
                speak('ok,Mam closing notepad')
                os.system('taskkill /f /im notepad.exe')

            elif 'alarm' in self.query:
                speak('mam, please tell me time to set alarm, for example set alarm for 5:30 am')
                tt = self.takeCommand()
                tt = tt.replace("set alarm for ", "")
                tt = tt.replace(".", "")
                tt = tt.upper()
                import MyAlarm
                MyAlarm.alarm(tt)

            #to set an alarm
            elif 'set the alarm' in self.query:
                vv = int(datetime.datetime.now().hour)
                if vv == 22:
                    music_dir = "C:\\Users\\ghk\\Music\\bts"
                    songs = os.listdir(music_dir)
                    os.startfile(os.path.join(music_dir,songs[0]))

            #to tell a joke
            elif 'tell me a joke' in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            #to tell latest news
            elif 'tell me latest news' in self.query:
                speak('Please Wait Mam, Fetching The Latest News')
                news()

            elif 'shut down the system' in self.query:
                os.system("shutdown /s /t s")

            elif 'restart the system' in self.query:
                os.system("shutdown /r /t s")

            elif 'sleep the system' in self.query:
                os.system("RUNDLL32.EXE powrprof.dll,SetSuspendState 0,1,0")

            elif 'you can sleep' in self.query:
                    speak("Thanks for using me,Mam, Have a good day")
                    sys.exit()

        # speak("Mam, do you have any other work")

startExecution = MainThread()



class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Intelligent_Virtual_Assistant()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("D:/ai_assistant/images/imagess/1 (1).gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant/images/imagess/a865256d7ae3c7a90fec2e4cea5f2f17.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant/images/imagess/1502899273_tumblr_op0623jfYh1v22rhuo1_500.gif")
        self.ui.label_5.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant/images/imagess/GW0l.gif")
        self.ui.label_6.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant/images/imagess/FluffyCornyBetafish-size_restricted.gif")
        self.ui.label_7.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant/images/imagess/kateauthentificaiton (1).gif")
        self.ui.label_8.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant/images/imagess/tenor.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant//images/imagess/tumblr.gif")
        self.ui.label_9.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant//images/imagess/gif-6.gif")
        self.ui.label_10.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant//images/imagess/hr.gif")
        self.ui.label_11.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant//images/imagess/799654599dc7d94999f24deb1de15020.gif")
        self.ui.label_12.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant//images/imagess/47a029b4bbd3cd011da6c35ccaacea13.gif")
        self.ui.label_13.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant//images/imagess/db6c7od-25531326-4ae0-4ee5-bc5f-542cf9924e80.gif")
        self.ui.label_16.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant//images/imagess/2.gif")
        self.ui.label_17.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant//images/imagess/attack.gif")
        self.ui.label_18.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant//images/imagess/BigEnchantingIcefish-small.gif")
        self.ui.label_19.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant//images/imagess/brain5.gif")
        self.ui.label_20.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant//images/imagess/hawaii.gif")
        self.ui.label_21.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/ai_assistant//images/imagess/late.gif")
        self.ui.label_22.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

# if __name__ == "__main__":
#     # speak('Hi My Name Is V And I am a good boy')
    
app = QApplication(sys.argv)
assistant = Main()
assistant.show()
exit(app.exec_())