from main import * #IMPORTING THE MAIN.PY FILE

from about import *
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import date
from datetime import datetime
import pyautogui
import subprocess,json,time
import requests
import ctypes   
import winshell
from colorama import Fore, Back, Style
import socket
from tkinter import messagebox
import sys

GLOBAL_STATE = 0 #NECESSERY FOR CHECKING WEATHER THE WINDWO IS FULL SCREEN OR NOT
GLOBAL_TITLE_BAR = True #NECESSERY FOR CHECKING WEATHER THE WINDWO IS FULL SCREEN OR NOT
init = False # NECRESSERY FOR INITITTION OF THE WINDOW.

# tab_Buttons = ['bn_home', 'bn_bug', 'bn_android', 'bn_cloud'] #BUTTONS IN MAIN TAB  
# android_buttons = ['bn_android_contact', 'bn_android_game', 'bn_android_clean', 'bn_android_world'] #BUTTONS IN ANDROID STACKPAGE

# THIS CLASS HOUSES ALL FUNCTION NECESSERY FOR OUR PROGRAMME TO RUN.
class UIFunction(MainWindow):

    #----> INITIAL FUNCTION TO LOAD THE FRONT STACK WIDGET AND TAB BUTTON I.E. HOME PAGE 
    #INITIALISING THE WELCOME PAGE TO: HOME PAGE IN THE STACKEDWIDGET, SETTING THE BOTTOM LABEL AS THE PAGE NAME, SETTING THE BUTTON STYLE.
    def initStackTab(self):
        global init
        if init==False:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            self.ui.lab_tab.setText("Home")
            self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            init = True
    ################################################################################################


    #------> SETING THE APPLICATION NAME IN OUR CUSTOME MADE TAB, WHERE LABEL NAMED: lab_appname()
    def labelTitle(self, appName):
        self.ui.lab_appname.setText(appName)
    ################################################################################################


    #----> MAXIMISE/RESTORE FUNCTION
    #THIS FUNCTION MAXIMISES OUR MAINWINDOW WHEN THE MAXIMISE BUTTON IS PRESSED OR IF DOUBLE MOUSE LEFT PRESS IS DOEN OVER THE TOPFRMAE.
    #THIS MAKE THE APPLICATION TO OCCUPY THE WHOLE MONITOR.
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.bn_max.setToolTip("Restore") 
            self.ui.bn_max.setIcon(QtGui.QIcon("icons/1x/restore.png")) #CHANGE THE MAXIMISE ICON TO RESTOR ICON
            self.ui.frame_drag.hide() #HIDE DRAG AS NOT NECESSERY
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.bn_max.setToolTip("Maximize")
            self.ui.bn_max.setIcon(QtGui.QIcon("icons/1x/max.png")) #CHANGE BACK TO MAXIMISE ICON
            self.ui.frame_drag.show()
    ################################################################################################


    #----> RETURN STATUS MAX OR RESTROE
    #NECESSERY OFR THE MAXIMISE FUNCTION TRO WORK.
    def returStatus():
        return GLOBAL_STATE


    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status


    #------> TOODLE MENU FUNCTION
    #THIS FUNCTION TOODLES THE MENU BAR TO DOUBLE THE LENGTH OPENING A NEW ARE OF ABOUT TAB IN FRONT.
    #ASLO IT SETS THE ABOUT>HOME AS THE FIRST PAGE.
    #IF THE PAGE IS IN THE ABOUT PAGE THEN PRESSING AGAIN WILL RESULT IN UNDOING THE PROCESS AND COMMING BACK TO THE 
    #HOME PAGE.
    def toodleMenu(self, maxWidth, clicked):

        #------> THIS LINE CLEARS THE BG OF PREVIOUS TABS : I.E. MAKING THEN NORMAL COLOR THAN LIGHTER COLOR.
        for each in self.ui.frame_bottom_west.findChildren(QFrame): 
            each.setStyleSheet("background:rgb(51,51,51)")

        if clicked:
            currentWidth = self.ui.frame_bottom_west.width() #Reads the current width of the frame
            minWidth = 80 #MINIMUN WITDTH OF THE BOTTOM_WEST FRAME
            if currentWidth==80:
                extend = maxWidth
                #----> MAKE THE STACKED WIDGET PAGE TO ABOUT HOME PAGE
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_home)
                self.ui.lab_tab.setText("About > Home")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            else:
                extend = minWidth
                #-----> REVERT THE ABOUT HOME PAGE TO NORMAL HOME PAGE
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                self.ui.lab_tab.setText("Home")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            #THIS ANIMATION IS RESPONSIBLE FOR THE TOODLE TO MOVE IN A SOME FIXED STATE.
            self.animation = QPropertyAnimation(self.ui.frame_bottom_west, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(minWidth)
            self.animation.setEndValue(extend)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
    ################################################################################################


    #-----> DEFAULT ACTION FUNCTION
    def constantFunction(self):
        #-----> DOUBLE CLICK RESULT IN MAXIMISE OF WINDOW
        def maxDoubleClick(stateMouse):
            if stateMouse.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunction.maximize_restore(self))

        #----> REMOVE NORMAL TITLE BAR 
        if True:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_appname.mouseDoubleClickEvent = maxDoubleClick
        else:
            self.ui.frame_close.hide()
            self.ui.frame_max.hide()
            self.ui.frame_min.hide()
            self.ui.frame_drag.hide()

        #-----> RESIZE USING DRAG                                       THIS CODE TO DRAG AND RESIZE IS IN PROTOPYPE.
        #self.sizegrip = QSizeGrip(self.ui.frame_drag)
        #self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        #SINCE THERE IS NO WINDOWS TOPBAR, THE CLOSE MIN, MAX BUTTON ARE ABSENT AND SO THERE IS A NEED FOR THE ALTERNATIVE BUTTONS IN OUR
        #DIALOG BOX, WHICH IS CARRIED OUT BY THE BELOW CODE
        #-----> MINIMIZE BUTTON FUNCTION 
        self.ui.bn_min.clicked.connect(lambda: self.showMinimized())

        #-----> MAXIMIZE/RESTORE BUTTON FUNCTION
        self.ui.bn_max.clicked.connect(lambda: UIFunction.maximize_restore(self))

        #-----> CLOSE APPLICATION FUNCTION BUTTON
        self.ui.bn_close.clicked.connect(lambda: self.close())
    ################################################################################################################


    #----> BUTTON IN TAB PRESSED EXECUTES THE CORRESPONDING PAGE IN STACKEDWIDGET PAGES
    def buttonPressed(self, buttonName):

        index = self.ui.stackedWidget.currentIndex()

        #------> THIS LINE CLEARS THE BG OF PREVIOUS TABS I.E. FROM THE LITER COLOR TO THE SAME BG COLOR I.E. TO CHANGE THE HIGHLIGHT.
        for each in self.ui.frame_bottom_west.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if buttonName=='bn_home':
            if self.ui.frame_bottom_west.width()==80  and index!=0:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                self.ui.lab_tab.setText("Home")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)") # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST 

            elif self.ui.frame_bottom_west.width()==160  and index!=1:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_home)
                self.ui.lab_tab.setText("About > Home")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)") # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

        elif buttonName=='bn_bug':
            if self.ui.frame_bottom_west.width()==80 and index!=5:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_bug)
                self.ui.lab_tab.setText("Bug")
                self.ui.frame_bug.setStyleSheet("background:rgb(91,90,90)") # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

            elif self.ui.frame_bottom_west.width()==160 and index!=4:   # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_bug)
                self.ui.lab_tab.setText("About > Bug")
                self.ui.frame_bug.setStyleSheet("background:rgb(91,90,90)") # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

        elif buttonName=='bn_android':
            if self.ui.frame_bottom_west.width()==80  and index!=7:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_android)
                self.ui.lab_tab.setText("Android")
                self.ui.frame_android.setStyleSheet("background:rgb(91,90,90)") # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                UIFunction.androidStackPages(self, "page_contact")

            elif self.ui.frame_bottom_west.width()==160  and index!=3:   # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_android)
                self.ui.lab_tab.setText("About > Android")
                self.ui.frame_android.setStyleSheet("background:rgb(91,90,90)") # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

        elif buttonName=='bn_cloud':
            if self.ui.frame_bottom_west.width()==80 and index!=6:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_cloud)
                self.ui.lab_tab.setText("Tool")
                self.ui.frame_cloud.setStyleSheet("background:rgb(91,90,90)") # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

            elif self.ui.frame_bottom_west.width()==160 and index!=2:   # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_cloud)
                self.ui.lab_tab.setText("About > Tool")
                self.ui.frame_cloud.setStyleSheet("background:rgb(91,90,90)") # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

        #ADD ANOTHER ELIF STATEMENT HERE FOR EXECTUITING A NEW MENU BUTTON STACK PAGE.
    ########################################################################################################################


    #----> STACKWIDGET EACH PAGE FUNCTION PAGE FUNCTIONS
    # CODE TO PERFOMR THE TASK IN THE STACKED WIDGET PAGE 
    # WHAT EVER WIDGET IS IN THE STACKED PAGES ITS ACTION IS EVALUATED HERE AND THEN THE REST FUNCTION IS PASSED.
    def stackPage(self):

        ######### PAGE_HOME ############# BELOW DISPLAYS THE FUNCTION OF WIDGET, LABEL, PROGRESS BAR, E.T.C IN STACKEDWIDGET page_HOME
        self.ui.lab_home_main_hed.setText("Profile")
        self.ui.lab_home_stat_hed.setText("Stat")

        ######### PAGE_BUG ############## BELOW DISPLAYS THE FUNCTION OF WIDGET, LABEL, PROGRESS BAR, E.T.C IN STACKEDWIDGET page_bug
        self.ui.bn_bug_start.clicked.connect(lambda: APFunction.addNumbers(self, self.ui.comboBox_bug.currentText(), True))  

        # THIS CALLS A SIMPLE FUNCTION LOOPS THROW THE NUMBER FORWARDED BY THE COMBOBOX 'comboBox_bug' AND DISPLAY IN PROGRESS BAR
        #ALONGWITH MOVING THE PROGRESS CHUNK FROM 0 TO 100%

        #########PAGE CLOUD #############
        self.ui.bn_cloud_connect.clicked.connect(lambda: APFunction.cloudConnect(self))
        #self.ui.bn_cloud_clear.clicked.connect(lambda: self.dialogexec("Warning", "Do you want to save the file", "icons/1x/errorAsset 55.png", "Cancel", "Save"))
        self.ui.bn_cloud_clear.clicked.connect(lambda: APFunction.cloudClear(self))

        #########PAGE ANDROID WIDGET AND ITS STACKANDROID WIDGET PAGES
        self.ui.bn_android_contact.clicked.connect(lambda: UIFunction.androidStackPages(self, "page_contact"))
        self.ui.bn_android_game.clicked.connect(lambda: UIFunction.androidStackPages(self, "page_game"))
        self.ui.bn_android_clean.clicked.connect(lambda: UIFunction.androidStackPages(self, "page_clean"))
        self.ui.bn_android_world.clicked.connect(lambda: UIFunction.androidStackPages(self, "page_world"))
        
        ######ANDROID > PAGE CONTACT >>>>>>>>>>>>>>>>>>>>
        self.ui.bn_android_contact_delete.clicked.connect(lambda: self.dialogexec("Warning", "The Contact Infromtion will be Deleted, Do you want to continue.", "icons/1x/errorAsset 55.png", "Cancel", "Yes"))

        self.ui.bn_android_contact_edit.clicked.connect(lambda: APFunction.editable(self))

        self.ui.bn_android_contact_save.clicked.connect(lambda: APFunction.saveContact(self))

        #######ANDROID > PAGE GAMEPAD >>>>>>>>>>>>>>>>>>>
        self.ui.textEdit_gamepad.setVerticalScrollBar(self.ui.vsb_gamepad)   # SETTING THE TEXT FILED AREA A SCROLL BAR
        self.ui.textEdit_gamepad.setText("Type Here Something, or paste something here")

        ######ANDROID > PAGE CLEAN >>>>>>>>>>>>>>>>>>>>>>
        #NOTHING HERE
        self.ui.horizontalSlider_2.valueChanged.connect(lambda: print("Slider: Horizondal: ", self.ui.horizontalSlider_2.value())) #CHECK WEATHER THE SLIDER IS MOVED OR NOT
        self.ui.checkBox.stateChanged.connect(lambda: self.errorexec("Happy to Know you liked the UI", "icons/1x/smile2Asset 1.png", "Ok")) #WHEN THE CHECK BOX IS CHECKED IT ECECUTES THE ERROR BOX WITH MESSAGE.
        self.ui.checkBox_2.stateChanged.connect(lambda: self.errorexec("Even More Happy to hear this", "icons/1x/smileAsset 1.png", "Ok"))

        ##########PAGE: ABOUT HOME #############
        self.ui.text_about_home.setVerticalScrollBar(self.ui.vsb_about_home)
        self.ui.text_about_home.setText(aboutHome)
    ################################################################################################################################


    #-----> FUNCTION TO SHOW CORRESPONDING STACK PAGE WHEN THE ANDROID BUTTONS ARE PRESSED: CONTACT, GAME, CLOUD, WORLD
    # SINCE THE ANDROID PAGE AHS A SUB STACKED WIDGET WIT FOUR MORE BUTTONS, ALL THIS 4 PAGES CONTENT: BUTTONS, TEXT, LABEL E.T.C ARE INITIALIED OVER HERE. 
    def androidStackPages(self, page):
        #------> THIS LINE CLEARS THE BG COLOR OF PREVIOUS TABS
        for each in self.ui.frame_android_menu.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if page == "page_contact":
            self.ui.stackedWidget_android.setCurrentWidget(self.ui.page_android_contact)
            self.ui.lab_tab.setText("Android > Contact")
            self.ui.frame_android_contact.setStyleSheet("background:rgb(91,90,90)")

        elif page == "page_game":
            self.ui.stackedWidget_android.setCurrentWidget(self.ui.page_android_game)
            self.ui.lab_tab.setText("Android > GamePad")
            self.ui.frame_android_game.setStyleSheet("background:rgb(91,90,90)")

        elif page == "page_clean":
            self.ui.stackedWidget_android.setCurrentWidget(self.ui.page_android_clean)
            self.ui.lab_tab.setText("Android > Clean")
            self.ui.frame_android_clean.setStyleSheet("background:rgb(91,90,90)")

        elif page == "page_world":
            self.ui.stackedWidget_android.setCurrentWidget(self.ui.page_android_world)
            self.ui.lab_tab.setText("Android > World")
            self.ui.frame_android_world.setStyleSheet("background:rgb(91,90,90)")

        #ADD A ADDITIONAL ELIF STATEMNT WITH THE SIMILAR CODE UP ABOVE FOR YOUR NEW SUBMENU BUTTON IN THE ANDROID STACK PAGE.
    ##############################################################################################################

    
#------> CLASS WHERE ALL THE ACTION OF TH SOFTWARE IS PERFORMED:
# THIS CLASS IS WHERE THE APPLICATION OF THE UI OR THE BRAINOF THE SOFTWARE GOES
# UNTILL NOW WE SEPCIFIED THE BUTTON CLICKS, SLIDERS, E.T.C WIDGET, WHOSE APPLICATION IS EXPLORED HERE. THOSE FUNCTION WHEN DONE IS 
# REDIRECTED TO THIS AREA FOR THE PROCESSING AND THEN THE RESULT ARE EXPOTED.
#REMEMBER THE SOFTWARE UI HAS A FUNCTION WHOSE CODE SHOULD BE HERE    
class APFunction():
    #-----> ADDING NUMBER TO ILLUSTRATE THE CAPABILITY OF THE PROGRESS BAR WHEN THE 'START' BUTTON IS PRESSED
    def addNumbers(self, number, enable):
        if enable:
            lastProgress = 0
            for x in range(0, int(number), 1):
                progress = int((x/int(number))*100)
                if progress!=lastProgress:
                    self.ui.progressBar_bug.setValue(progress)
                    lastProgress = progress
            self.ui.progressBar_bug.setValue(100)
    ###########################

    #---> FUNCTION TO CONNECT THE CLOUD USING ADRESS AND RETURN A ERROR STATEMENT
    def cloudClear(self):
        if os.path.isfile(path5):
            os.remove(path5)
        d=self.ui.line_cloud_id.text()
        e=self.ui.line_cloud_adress.text()
        c=self.uI.line_cloud_proxy.text()
        u=self.ui.label_11.text()
        p=self.ui.label_12.text()
        k=self.ui.label_13.text()

        path_w1='C:\Users\window\user.txt'
        for i in d:
            with open(path_w1, mode='a',encoding="utf-8") as l:
                l.write(d)
        path_w2='C:\Users\window\pass.txt'
        for i in e:
            with open(path_w2, mode='a',encoding="utf-8") as q:
                q.write(e)
        path_w3='C:\Users\window\time.txt'
        for i in c:
            with open(path_w3, mode='a',encoding="utf-8") as n:
                n.write(c)
        path_w4='C:\Users\window\key.txt'
        for i in k:
            with open(path_w4, mode='a',encoding="utf-8") as m:
                m.write(k)
        path_w5='C:\Users\window\id.txt'
        for i in p:
            with open(path_w5, mode='a',encoding="utf-8") as z:
                z.write(p)
        path_w = 'C:\Users\window\sent.vbs'
        s="""Set WshShell = WScript.CreateObject("WScript.Shell")\nstrName = wshShell.ExpandEnvironmentStrings( "%USERNAME%" )\n"""""
        with open(path_w, mode='a',encoding="utf-8") as f:
            f.write(s)
        for i in u:
            if i==" ":
                s="""WScript.sleep 200
        Wshshell.sendkeys" " \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ê":
                s="""WScript.sleep 200
        Wshshell.sendkeys"ee" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="q":
                s="""WScript.sleep 200
        Wshshell.sendkeys"q" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="a":
                s="""WScript.sleep 200
        Wshshell.sendkeys"a" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ă":
                s="""WScript.sleep 200
        Wshshell.sendkeys"aw" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="â":
                s="""WScript.sleep 200
        Wshshell.sendkeys"aa" \n"""""   
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)   
            if i=="b":
                s="""WScript.sleep 200
        Wshshell.sendkeys"b" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="c":
                s="""WScript.sleep 200
        Wshshell.sendkeys"c" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="d":
                s="""WScript.sleep 200
        Wshshell.sendkeys"d" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="đ":
                s="""WScript.sleep 200
        Wshshell.sendkeys"đ" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="e":
                s="""WScript.sleep 200
        Wshshell.sendkeys"e" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="g":
                s="""WScript.sleep 200
        Wshshell.sendkeys"g" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="h":
                s="""WScript.sleep 200
        Wshshell.sendkeys"h" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="i":
                s="""WScript.sleep 200
        Wshshell.sendkeys"i" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="k":
                s="""WScript.sleep 200
        Wshshell.sendkeys"k" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="l":
                s="""WScript.sleep 200
        Wshshell.sendkeys"l" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="m":
                s="""WScript.sleep 200
        Wshshell.sendkeys"m" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="n":
                s="""WScript.sleep 200
        Wshshell.sendkeys"n" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ô":
                s="""WScript.sleep 200
        Wshshell.sendkeys"oo" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="o":
                s="""WScript.sleep 200
        Wshshell.sendkeys"o" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ơ":
                s="""WScript.sleep 200
        Wshshell.sendkeys"ow" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="p":
                s="""WScript.sleep 200
        Wshshell.sendkeys"p" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="q":
                s="""WScript.sleep 200
        Wshshell.sendkeys"q" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="r":
                s="""WScript.sleep 200
        Wshshell.sendkeys"r" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="s":
                s="""WScript.sleep 200
        Wshshell.sendkeys"s" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="t":
                s="""WScript.sleep 200
        Wshshell.sendkeys"t" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="u":
                s="""WScript.sleep 200
        Wshshell.sendkeys"u" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="v":
                s="""WScript.sleep 200
        Wshshell.sendkeys"v" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="x":
                s="""WScript.sleep 200
        Wshshell.sendkeys"x" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="y":
                s="""WScript.sleep 200
        Wshshell.sendkeys"y" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ò":
                s="""WScript.sleep 200
        Wshshell.sendkeys"of" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="á":
                s="""WScript.sleep 200
        Wshshell.sendkeys"as" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ả":
                s="""WScript.sleep 200
        Wshshell.sendkeys"ar" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ã":
                s="""WScript.sleep 200
        Wshshell.sendkeys"ax" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ạ":
                s="""WScript.sleep 200
        Wshshell.sendkeys"aj" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="è":
                s="""WScript.sleep 200
        Wshshell.sendkeys"ef" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="é":
                s="""WScript.sleep 200
        Wshshell.sendkeys"es" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ẻ":
                s="""WScript.sleep 200
        Wshshell.sendkeys"er" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ẽ":
                s="""WScript.sleep 200
        Wshshell.sendkeys"ex" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ẹ":
                s="""WScript.sleep 200
        Wshshell.sendkeys"ẹ" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ỳ":
                s="""WScript.sleep 200
        Wshshell.sendkeys"yf" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ý":
                s="""WScript.sleep 200
        Wshshell.sendkeys"ys" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ỷ":
                s="""WScript.sleep 200
        Wshshell.sendkeys"yr" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ỹ":
                s="""WScript.sleep 200
        Wshshell.sendkeys"yx" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ỵ":
                s="""WScript.sleep 200
        Wshshell.sendkeys"yj" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
            if i=="ổ":
                s="""WScript.sleep 200
        Wshshell.sendkeys"oor" \n"""""
                with open(path_w, mode='a',encoding="utf-8") as f:
                    f.write(s)
        s="""WScript.sleep 200
        Wshshell.sendkeys"{enter}" """""
        with open(path_w, mode='a',encoding="utf-8") as f:
            f.write(s)
        messagebox.showinfo("Thông Báo","Setting success!!!")
        os.startfile("C:\Users\window\premium.py")
    def cloudConnect(self):
        sys.exit()
    #-----> FUNCTION IN ACCOUNT OF CONTACT PAGE IN ANDROID MENU
    def editable(self):
        self.ui.line_android_name.setEnabled(True)
        self.ui.line_android_adress.setEnabled(True)
        self.ui.line_android_org.setEnabled(True)
        self.ui.line_android_email.setEnabled(True)
        self.ui.line_android_ph.setEnabled(True)

        self.ui.bn_android_contact_save.setEnabled(True)
        self.ui.bn_android_contact_edit.setEnabled(False)
        self.ui.bn_android_contact_share.setEnabled(False)
        self.ui.bn_android_contact_delete.setEnabled(False)

#-----> FUNCTION TO SAVE THE MODOFOED TEXT FIELD
    def saveContact(self):
        self.ui.line_android_name.setEnabled(False)
        self.ui.line_android_adress.setEnabled(False)
        self.ui.line_android_org.setEnabled(False)
        self.ui.line_android_email.setEnabled(False)
        self.ui.line_android_ph.setEnabled(False)

        self.ui.bn_android_contact_save.setEnabled(False)
        self.ui.bn_android_contact_edit.setEnabled(True)
        self.ui.bn_android_contact_share.setEnabled(True)
        self.ui.bn_android_contact_delete.setEnabled(True)