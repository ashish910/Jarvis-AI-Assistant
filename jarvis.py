from lib2to3.pgen2 import driver
import pyttsx3
import requests
import speech_recognition as sr
import datetime
import os
import cv2
import random
import webbrowser
import wikipedia
from requests import get
import pyautogui
import time
import pywhatkit as kit
import sys
from playsound import playsound
from selenium import webdriver
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisUi import Ui_jarvisUi
import psutil
from kivy.app import App
from kivy.uix.video import Video
from kivy.clock import  Clock
import splash_screen


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# text to Speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def news():
    main_url = 'https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=5afb0ec34dc64e558c4c0bb703c95765'

    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")


def wish():
    hour = (datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour >= 0 and hour <= 12:
        speak(f"Good Morning Sir,its {tt}")
    elif hour > 12 and hour < 18:
        speak(f"Good Afternoon Sir,its {tt}")
    else:
        speak(f"Good Evening Sir, its {tt}")
    speak("I am jarvis  online and ready sir. how are you sir today")

def account_info():
    with open('account_info.txt','r') as f:
        info = f.read().split()
        email = info[0]
        password = info[1]
    return email,password

def account_infoo():
    with open('account_info1.txt','r') as f:
        info = f.read().split()
        email = info[0]
        password = info[1]
    return email, password



class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        speak("please say wake up to continue")
        while True:
            self.query = self.takecommand()
            if "wake up" in self.query or "are you there" in self.query or "hello jarvis" in self.query:
                self.authentication()

    def authentication(self):
        speak("look at your camera")
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)

        font = cv2.FONT_HERSHEY_SIMPLEX

        id = 2
        names = ['','asp']

        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cam.set(3, 640)
        cam.set(4, 480)

        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)

        while True:
            ret, img = cam.read()
            converted_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
            converted_image,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
         )

            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                id, accuracy = recognizer.predict(converted_image[y:y+h,x:x+w])

                if (accuracy < 100):
                    id = names[id]
                    accuracy = " {0}%".format(round(100 - accuracy))
                    self.TaskExecution()

                else:
                    id = "unknown"
                    accuracy =  " {0}%".format(round(100 - accuracy))
                    speak("user authentication is failed")
                    break

                cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(accuracy), (x+5,y+h-5), font, 1, (255,255,0), 1) 

            #cv2.imshow('camera',img)


            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break

        cam.release()
        cv2.destroyAllWindows()



# To Convert voice into text
    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("listening...")
            r.pause_threshold = 1
            audio = r.listen(source,timeout=5,phrase_time_limit=10)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")

        except Exception as e:
            speak("say that again please...")
            return "none"
        query = query.lower()
        return query


    def TaskExecution(self):
        pyautogui.press('esc')
        speak('verification successful')
        speak('Welcome back Ashish sir')
        wish()
        while True:
            self.query = self.takecommand()

            if "open notepad" in self.query:
                npath = "C:\\WINDOWS\\system32\\notepad.exe"
                os.startfile(npath)

            elif "open command prompt" in self.query:
                os.system(" start cmd")

            elif "open camera" in self.query:
                cam = cv2.VideoCapture(0)

                cv2.namedWindow("test")

                img_counter = 0

                while True:
                    ret, frame = cam.read()
                    if not ret:
                        print("failed to grab frame")
                        break
                    cv2.imshow("test", frame)

                    k = cv2.waitKey(1)
                    if k % 256 == 27:
                        # ESC pressed
                        print("Escape hit, closing...")
                        break
                    elif k % 256 == 32:
                        img_name = "opencv_frame_{}.png".format(img_counter)
                        cv2.imwrite(img_name, frame)
                        print("{} written!".format(img_name))
                        img_counter += 1

                cam.release()

                cv2.destroyAllWindows()

            elif "play music" in self.query:
                music_dir = "C:\\Users\\Ashish\\Music\\Playlists\\asp1"
                songs = os.listdir(music_dir)
                rd = random.choice(songs)
                os.startfile(os.path.join(music_dir, rd))

            elif "ip address" in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"your IP address is {ip}")

            elif "wikipedia" in self.query:
                speak("searching wikipedia....")
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query, sentences=2)
                speak("According to wikipedia")
                speak(results)


            elif "open Youtube" in self.query:
                webbrowser.open(("www.youtube.com"))

            elif "open facebook" in self.query:               
                email, password = account_info()

                tweet = speak('Enter the message')
                z = self.takecommand()
                print(f"{z}")

                options = webdriver.ChromeOptions()
                options.add_experimental_option('excludeSwitches',['enable-logging'])
                options.add_argument("start-maximized")
                driver = webdriver.Chrome(options=options)
                driver.get("https://www.facebook.com/login/")

                email_xpath = '//*[@id="email"]'
                password_xpath = '//*[@id="pass"]'
                login_xpath = '//*[@id="loginbutton"]'

                time.sleep(3)
                driver.find_element_by_xpath(email_xpath).send_keys(email)
                time.sleep(2)
                driver.find_element_by_xpath(password_xpath).send_keys(password)
                time.sleep(1)
                driver.find_element_by_xpath(login_xpath).click()
                time.sleep(50)
                pyautogui.click(721,462)
                time.sleep(5)
                pyautogui.typewrite(z)
                time.sleep(3)
                pyautogui.click(620,609)

            elif "open twitter" in self.query:
                email, password = account_infoo()
                options = webdriver.ChromeOptions()
                options.add_experimental_option('excludeSwitches',['enable-logging'])
                options.add_argument("start-maximized")
                driver = webdriver.Chrome(options=options)
                driver.get("https://twitter.com/i/flow/login?input_flow_data=%7B%22requested_variant%22%3A%22eyJsYW5nIjoiZW4ifQ%3D%3D%22%7D")  

                tw = speak('Enter the message')
                o = self.takecommand()
                print(f"{o}")

                email_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[5]/label/div/div[2]/div/input'
                next_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[6]/div'
                password_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
                login_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div'

                time.sleep(10)
                driver.find_element_by_xpath(email_xpath).send_keys(email)
                time.sleep(2)
                driver.find_element_by_xpath(next_xpath).click()
                time.sleep(2)
                driver.find_element_by_xpath(password_xpath).send_keys(password)
                time.sleep(2)
                driver.find_element_by_xpath(login_xpath).click()

                time.sleep(20)
                pyautogui.click(733,203)
                time.sleep(5)
                pyautogui.typewrite(o)
                time.sleep(4)
                pyautogui.click(837,294)

            elif "open google" in self.query:
                speak("sir, what should i search on google")
                cm = self.takecommand()
                webbrowser.open(f"{cm}")

            elif "open whatsapp" in self.query:
                webbrowser.open('https://web.whatsapp.com/')
                person_name = speak("Enter the Person Name Whom you want to send a message:-")
                p = self.takecommand()
                print(f"{p}")
                my_msg = speak("Enter Your Message:-")
                m = self.takecommand()
                print(f"{m}")
                time.sleep(20)
                pyautogui.click(130, 154)
                pyautogui.typewrite(p)

                time.sleep(5)
                pyautogui.click(113, 253)

                time.sleep(5)
                pyautogui.typewrite(m)

                time.sleep(2)
                pyautogui.click(1324, 695)

            elif "play songs on youtube" in self.query:
                speak("sir, what should i play")
                cm = self.takecommand()
                kit.playonyt(f"{cm}")

            elif "open gmail" in self.query:
                sender_gmail = input("Enter the gmail to send:-")
                subject = input("Enter Your subject:-")
                content = input("Enter the content:-")
                webbrowser.open('https://mail.google.com/')

                time.sleep(20)
                pyautogui.click(64, 175)
                time.sleep(3)
                pyautogui.click(869, 317)
                pyautogui.typewrite(sender_gmail)

                time.sleep(5)
                pyautogui.click(1263, 354)
                pyautogui.typewrite(subject)

                time.sleep(5)
                pyautogui.click(921, 501)
                pyautogui.typewrite(content)

                time.sleep(2)
                pyautogui.click(841, 698)

            elif "how much power we have" in self.query or "how much power left" in self.query or "battery" in self.query:
                battery = psutil.sensors_battery()
                percentage = battery.percent
                speak(f"sir our system have{percentage} percent battery")
                if percentage >= 75:
                    speak("we have enough power to continue our work")
                elif percentage >= 40 and percentage <= 75:
                    speak("It is sufficient to do work")
                elif percentage <= 15 and percentage <= 30:
                    speak("we don't have enough power to work,please connect to charging")
                elif percentage <= 15:
                    speak("we have very low power, please connect to charging the system will be shutdown very soon")
   

    # closing all applications
            elif "close notepad" in self.query:
                speak("okay sir,closing notepad")
                os.system("taskkill /f /im notepad.exe")

            elif "close facebook" in self.query:
                speak("okay sir,closing facebook")
                os.system("taskkill /f /im chrome.exe")

            elif "close youtube" in self.query:
                speak("okay sir,closing youtube")
                os.system("taskkill /f /im chrome.exe")

            elif "close music" in self.query:
                speak("okay sir,closing music")
                os.system("taskkill /f /im Music.UI.exe")

            elif "close command prompt" in self.query:
                speak("okay sir,closing command prompt")
                os.system("taskkill /f /im cmd.exe")

            elif "weather" in self.query or "temperature" in self.query:
               location =  speak("Tell the city name:")
               l = self.takecommand()
               print(f"{l}")
               complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+l+"&appid="+"924acd60bc4c1f15562bb40b5380145b"
               api_link = requests.get(complete_api_link)
               api_data = api_link.json()
               if api_data['cod']  !='404':
                temp_city = round(((api_data['main']['temp'])-273.15),2)
                weather_desc = api_data['weather'][0]['description']
                hmdt = api_data['main']['humidity']
                wind_spd  = api_data['wind']['speed']
                speak(f"The weather in {l} is currently {weather_desc} with a temperature of {temp_city} degree celsius and humidity is {hmdt} %  and wind speed reaching {wind_spd} kilometers per hour ")
               else:
                    print("Invalid City: {},please check your city name".format(location))

            elif 'switch the window' in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif 'tell me news' in self.query:
                speak("please wait sir,fetching the latest news")
                news()

            elif "where i am" in self.query or 'where we are' in self.query:
                speak("wait sir,let me check")
                ipAd = requests.get('https://api.ipify.org').text
                print(ipAd)
                r = requests.get('https://get.geojs.io/')
                ip_request = requests.get("https://get.geojs.io/v1/ip.json")
                ipAdd = ip_request.json()['ip']

                url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                geo_request = requests.get(url)
                geo_data = geo_request.json()
                city = geo_data['city']
                country = geo_data['country']
                speak(f"sir i am not sure,but i think we are in {city} city of {country} country")

            elif "volume up" in self.query:
                pyautogui.press("volumeup")   

            elif "volume down" in self.query:
                pyautogui.press("volumedown")

            elif "volume mute" in self.query or "mute" in self.query:
                pyautogui.press("volumemute ")

            elif "remember that" in self.query:
                remembermsg = self.query.replace("remember that","")
                remembermsg = remembermsg.replace("jarvis","")
                speak("You tell me to remind that: "+remembermsg)
                remember = open('data.txt','w')
                remember.write(remembermsg)
                remember.close()

            elif "what do you remember" in self.query :
                remember = open('data.txt','r')
                speak('you tell me that'+ remember.read())       
                                    
    #--------------system operations---------------------
            elif "shut down the system" in self.query:
                os.system("shutdown /s /t 5")

            elif "restart the system" in self.query:
                os.system("shutdown /r /t 5")

            elif "sleep the system" in self.query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    #----------------To take screenshot-------------

            elif "take screenshot" in self.query or "take a screenshot" in self.query:
                speak("Sir,please tell me the name of screenshot file")
                name = self.takecommand()
                speak("please sir hold the screen for few seconds, i am taking screenshot")
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("I am done sir,the screenshot is saved in our main folder .now i am ready for next command")

    #--------------To hide files and folder------------
            elif "hide all files" in self.query or "hide this folder" in self.query or "visible for everyone" in self.query:
                speak("sir please tell me you want to hide this folder or make it visible for everyone")
                condition = self.takecommand()
                if "hide" in condition:
                    os.system("attrib +h /s /d")
                    speak("sir,all the files in this folder are now hidden")

                elif "visible" in condition:
                    os.system("attrib -h /s /d")
                    speak("sir,all the files in this folder are now visible to everyone . i wish you are taking this decision in your own peace")

                elif "leave it" in condition or "leave for now" in condition:
                    speak("ok sir")


            elif "no thanks" in self.query or "you can close now" in self.query:
                speak("Ok sir i am going to offline,Thanks for using me sir,have a good day...")
                sys.exit()

            elif "hello" in self.query or "hey" in self.query:
                speak("hello sir, may i help you with something")

            elif "how are you" in self.query:
                speak("I am fine sir ,what about you")

            elif "also good" in self.query or "fine" in self.query:
                speak("I am also fine that's great to hear from you")

            elif "thank you" in self.query or "thanks" in self.query:
                speak("It's my pleasure sir")

            elif "you can sleep" in self.query or "sleep now" in self.query:
                speak("okay sir,i am going to sleep you can call me anytime.")
                break                  

            elif "i am fine " in self.query:
                speak("I am also fine that's great to hear from you")

            elif "okay jarvis " in self.query or "let perform some task" in self.query:
                speak("I am always be ready sir ")    

startExecution = MainThread()

class Main(QMainWindow):
  
    def __init__(self):
       super().__init__()
       self.ui = Ui_jarvisUi()
       self.ui.setupUi(self)
       self.ui.pushButton.clicked.connect(self.startTask)
       self.ui.pushButton_2.clicked.connect(self.close)

    

    def startTask(self):
        self.ui.movie = QtGui.QMovie("../../../Downloads/Jarvis Gif/7LP8.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../../../Downloads/Jarvis Gif/BigheartedVagueFoal-size_restricted.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../../../Downloads/Jarvis Gif/jarvisvoice.gif")
        self.ui.label_3.setMovie(self.ui.movie)
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

app = QApplication(sys.argv)
jarvis = Main()
video_window=splash_screen.VideoWindow()
video_window.run()
Clock.schedule_once(video_window.stop,50)
jarvis.show()
exit(app.exec_())
