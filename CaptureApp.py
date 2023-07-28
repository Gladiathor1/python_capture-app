import os

from datetime import datetime


import pyautogui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
import cv2
from PyQt5.QtCore import QThread
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import zipfile


def delfiles():
    file1 = open('username.txt', 'r')
    # Lines = file1.readlines()

    lname = file1.readline()
    lname = lname.rstrip(("\n"))
    fname = file1.readline()
    fname = fname.rstrip("\n")
    idn = file1.readline()
    file1.close()
    path = lname + "." + fname + "." + idn
    dir = path + "\\"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))  # ,
            # os.path.relpath(os.path.join(root, file),
            #               os.path.join(path, '..')))


def sendmail():
    file1 = open('username.txt', 'r')
    # Lines = file1.readlines()

    lname = file1.readline()
    lname = lname.rstrip(("\n"))
    fname = file1.readline()
    fname = fname.rstrip("\n")
    idn = file1.readline()
    file1.close()
    path = lname + "." + fname + "." + idn

    email_user = 'captureapp@emvia.com'
    email_password = 'D3vT3$t1g'
    email_send = 'submissions@emvia.com'

    subject = path

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = ''
    msg.attach(MIMEText(body, 'plain'))

    filename = path + '.zip'
    attachment = open(filename, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.ionos.com', 587)
    server.starttls()
    server.login(email_user, email_password)

    server.sendmail(email_user, email_send, text)
    server.quit()


def checkcam():

    for i in range(9):


        try:
            cap = cv2.VideoCapture(i)
            if cap is not None or cap.isOpened():
                ret, cv_img = cap.read()
                if ret:
                    #cap.release()
                    return i
            #cap.release()
        except:
            pass

    return -1

class VideoThread(QThread):

    def run(self):
        # capture from web cam
        file1 = open('username.txt', 'r')
        # Lines = file1.readlines()

        lname = file1.readline()
        lname = lname.rstrip(("\n"))
        fname = file1.readline()
        fname = fname.rstrip("\n")
        idn = file1.readline()
        file1.close()
        path = lname + "." + fname + "." + idn
        if not os.path.exists(path):
            os.makedirs(path)
        num =checkcam()
        if num>-1:
            cap=cv2.VideoCapture(num)
        while True:
            now = datetime.now()
            var = now.strftime("%Y%m%d %H%M")

            img_name = path + "\\"+str(var)+"Cam.jpg"
            if num>-1:
                try:
                    ret, cv_img = cap.read()
                    if ret:
                        cv2.imwrite(img_name, cv_img)
                except:
                    date = datetime.now()
                    date2 = date.strftime("%Y/%m/%d %H:%M:%S")
                    check = open(path + "\\Event.txt", "a")
                    check.write("Webcam Disconnected " + date2)
                    check.write("\n")
                    check.close()
            else:
                date = datetime.now()
                date2 = date.strftime("%Y/%m/%d %H:%M:%S")
                check = open(path + "\\Event.txt", "a")
                check.write("Webcam not connected " + date2)
                check.write("\n")
                check.close()
            try:
                myScreenshot = pyautogui.screenshot()
                myScreenshot.save(path + "\\" + str(var) + "Desktop_frame.jpg")
            except:
                date = datetime.now()
                date2 = date.strftime("%Y/%m/%d %H:%M:%S")
                check = open(path + "\\Event.txt", "a")
                check.write("Desktop capture failure " + date2)
                check.write("\n")
                check.close()

            QThread.sleep(300)




class otherwork(QThread):
    def run(self):
        file1 = open('username.txt', 'r')
        # Lines = file1.readlines()

        lname = file1.readline()
        lname = lname.rstrip(("\n"))
        fname = file1.readline()
        fname = fname.rstrip("\n")
        idn = file1.readline()
        file1.close()
        path = lname + "." + fname + "." + idn
        while True:
            QThread.sleep(18000)
            if os.path.exists(path):
                zipf = zipfile.ZipFile(path + '.zip', 'w', zipfile.ZIP_DEFLATED)
                zipdir(path + "\\", zipf)
                zipf.close()
                try:
                    sendmail()
                    delfiles()
                # os.remove('data1.zip')
                except:
                    date = datetime.now()
                    date2 = date.strftime("%Y/%m/%d %H:%M:%S")
                    check = open(path + "\\Event.txt", "a")
                    check.write("connection error " + date2)
                    check.write("\n")
                    check.close()


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('logo.jpeg'))
        self.setStyleSheet("background-color: darkBlue;")
        self.w = None  # No external window yet.
        self.setWindowTitle("Capture App")
        self.disply_width = 1000
        self.display_height = 1000
        self.button = QPushButton("Submit")
        self.button.setStyleSheet("background-color: white;")
        self.button.clicked.connect(self.show_new_window)
        self.textbox1 = QLineEdit(self)
        self.textbox1.setStyleSheet("color: white")
        self.textbox1.move(20, 20)
        self.textbox1.resize(280, 40)
        self.textbox2 = QLineEdit(self)
        self.textbox2.setStyleSheet("color: white")
        self.textbox2.move(20, 20)
        self.textbox2.resize(280, 40)
        self.textbox3 = QDateEdit(self)
        self.textbox3.setDisplayFormat("MM-dd-yyyy")
        self.textbox3.setStyleSheet("color: white")
        self.textbox3.move(20, 20)
        self.textbox3.resize(280, 40)
        self.qlabel1 = QLabel("Enter First Name", self)
        self.qlabel1.setStyleSheet("color: white")
        self.qlabel2 = QLabel("Enter Last Name", self)
        self.qlabel2.setStyleSheet("color: white")
        self.qlabel3 = QLabel("Enter Date of Birth as (MM,DD,YYYY)", self)
        self.qlabel3.setStyleSheet("color: white")
        self.caution = QLabel("This is a one time only Process\n Please Enter valid name")
        self.caution.setStyleSheet("color: white")
        myFont = QFont()
        myFont.setBold(True)
        self.caution.setFont(myFont)
        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.caution)
        vbox.addWidget(self.qlabel1)
        vbox.addWidget(self.textbox1)
        vbox.addWidget(self.qlabel2)
        vbox.addWidget(self.textbox2)
        vbox.addWidget(self.qlabel3)
        vbox.addWidget(self.textbox3)
        vbox.addWidget(self.button)
        # set the vbox layout as the widgets layout
        self.setMinimumSize(300, 300)
        self.setLayout(vbox)

    def show_new_window(self, checked):
        if self.w is None:

            f = open("username.txt", "w+")
            f.write(self.textbox2.text())
            f.write("\n")
            f.write(self.textbox1.text())
            f.write("\n")
            f.write(self.textbox3.text())
            f.close()
            self.w = MainWindow()
            self.w.tray_icon.show()
            self.hide()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('logo.jpeg'))
        self.setStyleSheet("background-color: darkBlue;")
        self.img_count = 0
        self.setWindowTitle("Capture App")
        self.disply_width = 1000
        self.display_height = 1000
        # create the label that holds the image
        #self.image_label = QLabel(self)


        #self.image_label.resize(self.disply_width, self.display_height)

        # Using readlines()
        file1 = open('username.txt', 'r')

        lname = file1.readline()

        fname = file1.readline()
        fname = fname.rstrip("\n")
        file1.close()
        # create a text label
        self.textLabel = QLabel("Welcome " + fname + " " + lname)
        self.textLabel.setStyleSheet("color: white")
        self.Exitbutton = QPushButton("Exit")
        self.Exitbutton.setStyleSheet("background-color: white;")
        self.Exitbutton.clicked.connect(self.stop_thread)
        myFont = QFont()
        myFont.setBold(True)
        self.textLabel.setFont(myFont)

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.textLabel)
        # vbox.addWidget(self.textLabel)
        vbox.addWidget(self.Exitbutton)
        # set the vbox layout as the widgets layout
        self.setMinimumSize(200, 200)
        self.setLayout(vbox)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("logo.jpeg"))

        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.stop_thread)
        tray_menu = QMenu()
        tray_menu.addAction("User: " + fname + " " + lname)
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()


        # appstarted()

        # create the video capture thread
        self.thread = VideoThread()
        self.thread2 = otherwork()

        # start the thread
        self.thread.start()

        self.thread2.start()




    def stop_thread(self):
        cv2.destroyAllWindows()
        file1 = open('username.txt', 'r')
        # Lines = file1.readlines()

        lname = file1.readline()
        lname = lname.rstrip(("\n"))
        fname = file1.readline()
        fname = fname.rstrip("\n")
        idn = file1.readline()
        file1.close()
        path = lname + "." + fname + "." + idn
        date = datetime.now()
        date2 = date.strftime("%Y/%m/%d %H:%M:%S")
        check = open(path + "\\Event.txt", "a")
        check.write("User terminated the app on " + date2)
        check.write("\n")
        check.close()
        exit()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    if not os.path.exists("username.txt"):

        a = App()
        a.show()

    else:
        a = MainWindow()

        #a.show()

    sys.exit(app.exec_())







