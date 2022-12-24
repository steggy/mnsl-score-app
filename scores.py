#! /usr/bin/python3
##
## Author: Steggy
## Gui for the MNSL score database
## Inspired by Ira Weiny's Perl version
##
## Github
## https://github.com/steggy/mnsl-score-app.git
##


import sys, time, os, json
from datetime import datetime
import readwriteconfig as CF
import mnslqueries as mnslq
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QAction, QCompleter, QLineEdit, QStyledItemDelegate, QComboBox
from PyQt5.QtWidgets import QDialog, QPushButton, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QTime, QDate

base = sys.path[0]
#sys.exit()
configfile = sys.path[0] + "/scores.conf"
configdict = dict(CF.Config(configfile).Fetch('database'))
configlist = list(configdict.values())
session = str(CF.Config(configfile).Fetch('session')[0][1])
ver = str(CF.Config(configfile).Fetch('version')[0][1])


scoredate = ""
eventdict = {"PPC":1,"Tyro":2,"Rifle":3}
divdict = {"Open":1,"22":2,"Prod":3,"Revolver":4,"special":5}



################################################################################################
# Convert UI to PyQt5 py file
################################################################################################
os.system("pyuic5 -x " + base + "/mainwindow.ui -o " + base + "/MainWindow.py")
os.system("pyuic5 -x " + base + "/editscore.ui -o " + base + "/EditScore.py")
os.system("pyuic5 -x " + base + "/scoresbyshooter.ui -o " + base + "/ScoresByShooter.py")
from MainWindow import *
from EditScore import *
from ScoresByShooter import *


class ReadOnlyDelegate(QStyledItemDelegate):
        def createEditor(self, parent, option, index):
            print('createEditor event fired')
            return

class comboEvent(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.addItems(['PPC','Tyro', 'Rifle'])

class comboDiv(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.addItems(['Open','22', 'Prod','Revolver','special'])

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("HELLO!")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.msgbox = QLabel()
        self.layout.addWidget(self.msgbox)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class ScoresByShooter(QtWidgets.QMainWindow, Ui_ScoresByShooter):
    def __init__(self, *args, obj=None, **kwargs):
        super(ScoresByShooter, self).__init__(*args, **kwargs)
        #self.setupUi(self)
        self.ui = Ui_ScoresByShooter()        
        self.ui.setupUi(self)
        self.setFixedSize(915,600) 
    
        self.ui.ButtShowScores.clicked.connect(self.loadscores)
        self.ui.ButtShowScores.keyPressEvent = self.loadscores
        self.ui.lblSession.setText("Crap")
        self.ui.comboSession.currentTextChanged.connect(self.on_session_changed)
    
    def keyPressEvent(self, event: QtGui.QKeyEvent):
        print(chr(event.key()+ 73))

    
    def on_session_changed(self):
        if SBS.ui.comboSession.currentText() == '':
            sess = "'%'"
        else:
            sess = SBS.ui.comboSession.currentText()
    
        SBS.ui.comboSBSDate.clear()
        SBS.ui.comboSBSDate.addItem('')
        dtelist = list(map(lambda x : str(x['dte']), mnslq.MNSLQuery(configfile).FetchSessionDates(sess)))
        SBS.ui.comboSBSDate.addItems(dtelist)

    def loadscores(self, e):
        if not e:
            pass
        else:
            try:
                if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
                    pass
                else:
                    return
            except:
                print('No Key')
                return
        self.ui.tblScores.setColumnWidth(2,220)
        self.ui.tblScores.clearContents()
        self.ui.tblScores.setRowCount(0)
        sname = self.ui.lnShooter.text()
        dte = self.ui.comboSBSDate.currentText()
        sess = self.ui.comboSession.currentText()
        data = mnslq.MNSLQuery(configfile).FetchScoreBySSD(mnslq.MNSLQuery(configfile).FetchShooterId(sname),dte,sess)
        try:
            if len(data) < 1:
                return
        except:
            return
        self.ui.tblScores.setRowCount(len(data))
        tblindex = 0
        for i in data:
            self.ui.tblScores.setItem(tblindex,0,QtWidgets.QTableWidgetItem(str(i['dte'])))
            self.ui.tblScores.setItem(tblindex,1,QtWidgets.QTableWidgetItem(str(i['lnum'])))
            self.ui.tblScores.setItem(tblindex,2,QtWidgets.QTableWidgetItem(str(i['name'])))
            self.ui.tblScores.setItem(tblindex,3,QtWidgets.QTableWidgetItem(str(i['evt'])))
            self.ui.tblScores.setItem(tblindex,4,QtWidgets.QTableWidgetItem(str(i['divv'])))
            self.ui.tblScores.setItem(tblindex,5,QtWidgets.QTableWidgetItem(str(i['cal'])))
            self.ui.tblScores.setItem(tblindex,6,QtWidgets.QTableWidgetItem(str(i['score'])))
            tblindex +=1

    def OpenWindow(self):
        #self.show()
        SBS.ui.lblSession.setText('') 
        SBS.ui.comboSBSDate.clear() 
        SBS.ui.tblScores.clearContents()
        SBS.ui.tblScores.setRowCount(0)
        sessdict = mnslq.MNSLQuery(configfile).FetchSessionList()
        sesslist = list(map(lambda x : str(x['leaguenum']), sessdict))
        SBS.ui.comboSession.addItem('')
        SBS.ui.comboSession.addItems(sesslist)
        
        SBS.ui.comboSBSDate.addItem('')
        dtelist = list(map(lambda x : str(x['dte']), mnslq.MNSLQuery(configfile).FetchSessionDates(session)))
        SBS.ui.lblSession.setText(window.windowTitle()) 
        SBS.show()
    
    def closeEvent(self, event):
        self.ui.lnShooter.setText('')
        event.accept()



class EditScoreWindow(QtWidgets.QMainWindow, Ui_EditScoreWindow):
    combotblEventList = []
    combotblDivList = []
    def __init__(self, *args, obj=None, **kwargs):
        super(EditScoreWindow, self).__init__(*args, **kwargs)
        #self.setupUi(self)
        self.ui = Ui_EditScoreWindow()        
        self.ui.setupUi(self)
        self.setFixedSize(733,600) 

        self.ui.ButtSelect.clicked.connect(self.addscorerows)
        self.ui.ButtSelect.keyPressEvent = self.addscorerows
        self.ui.ButtCancel.clicked.connect(self.CloseEditScoresWindow)
        self.ui.ButtCancel.clicked.connect(self.CloseEditScoresWindow)
        self.ui.ButtCancel.keyPressEvent = self.CloseEditScoresWindow
        delegate = ReadOnlyDelegate(self.ui.tblScores)
        self.ui.tblScores.setItemDelegateForColumn(0, delegate)
        self.ui.tblScores.setItemDelegateForColumn(1, delegate)
        self.ui.tblScores.setItemDelegateForColumn(2, delegate)
        self.ui.ButtUpdate.clicked.connect(self.UpdateScores)
        self.ui.tblScores.setColumnWidth(0,20)
        self.ui.tblScores.setColumnWidth(1,20)
    
    
    def closeEvent(self, event):
        self.ui.lnEditScoreShooterName.setText('')
        event.accept()
    


    
    def UpdateScores(self):
        rowCount = self.ui.tblScores.rowCount()
        itemdict = {}
        columnCount = self.ui.tblScores.columnCount()
        cbox = [3,4]
        scorelist = []
        for row in range(rowCount):
            #print("ROW",row)
            rowData = 'update scores '
            for column in range(columnCount):
                cellitem = self.ui.tblScores.item(row,column)
                #if(cellitem and cellitem.text):
                if column == 0:
                    rid = cellitem.text()
                    itemdict['id']=rid
                if column == 3:
                    event = eventdict[combotblEventList[row].currentText()]
                    rowData = rowData + 'set eid=' + str(event)
                    itemdict['eid']=str(eventdict[combotblEventList[row].currentText()])
                if column == 4:    
                    div = divdict[combotblDivList[row].currentText()]
                    rowData = rowData + ',did=' + str(div)
                    itemdict['did'] = str(divdict[combotblDivList[row].currentText()])
                if column == 5:
                    rowData = rowData + ",cal='" + cellitem.text() + "'"
                    itemdict['cal'] = cellitem.text()
                if column == 6:
                    if len(cellitem.text()) < 1:
                        rowData = "delete from scores"
                        itemdict['delete'] = 1

                        
                    else:
                        rowData = rowData + ',score=' + cellitem.text()
                        itemdict['score'] = cellitem.text()
                        itemdict['delete'] = 0

            scorelist.append(itemdict)
            itemdict = {}
        mnslq.MNSLQuery(configfile).UpdateScore(scorelist)
        
        self.ui.lblSelectedShooter.setStyleSheet("color: red")
        current_time = QTime.currentTime()

        # converting QTime object to string
        label_time = current_time.toString('HH:mm:ss')

        self.ui.lblSelectedShooter.setText(self.ui.lblSelectedShooter.text() + ' Updated ' + label_time)

        #reload table at end

    def addscorerows(self, e):
        global combotblEventList
        global combotblDivList
        if not e:
            pass
        else:
            try:
                if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
                    pass
                else:
                    return
            except:
                print('No Key')
                return
        
        win = EditScoreWindow(self)
        editwindow.ui.lblSelectedShooter.setStyleSheet("color: black")
        sname = editwindow.ui.lnEditScoreShooterName.text()
        sdte = editwindow.ui.comboBoxDate.currentText()
        
        sid = mnslq.MNSLQuery(configfile).FetchShooterId(sname)
        data = mnslq.MNSLQuery(configfile).FetchShooterScoresByDate(sid,session,sdte)
        editwindow.ui.lblSelectedShooter.clear()
        editwindow.ui.tblScores.clearContents()
        editwindow.ui.tblScores.setRowCount(0)
        if len(data) < 1:
            editwindow.ui.lblSelectedShooter.setText('No DATA')
            editwindow.ui.ButtUpdate.setEnabled(0)
            return
        editwindow.ui.ButtUpdate.setEnabled(1)
        editwindow.ui.tblScores.setRowCount(len(data))
        tblindex = 0
        combotblEventList = []
        combotblDivList = []
        for i in data:
            editwindow.ui.tblScores.setItem(tblindex,0,QtWidgets.QTableWidgetItem(str(i['id'])))
            editwindow.ui.tblScores.setItem(tblindex,1,QtWidgets.QTableWidgetItem(str(i['shooterid'])))
            editwindow.ui.tblScores.setItem(tblindex,2,QtWidgets.QTableWidgetItem(str(i['dte'])))
            combotblEventList.append(comboEvent(editwindow.ui.tblScores)) 
            combotblDivList.append(comboDiv(editwindow.ui.tblScores)) 
            ix = combotblEventList[tblindex].findText(str(i['eventname']))
            editwindow.ui.tblScores.setCellWidget(tblindex,3,combotblEventList[tblindex])
            combotblEventList[tblindex].setCurrentIndex(int(ix))
            
            ix = combotblDivList[tblindex].findText(str(i['divname']))
            editwindow.ui.tblScores.setCellWidget(tblindex,4,combotblDivList[tblindex])
            combotblDivList[tblindex].setCurrentIndex(int(ix))
            editwindow.ui.tblScores.setItem(tblindex,5,QtWidgets.QTableWidgetItem(str(i['cal'])))
            editwindow.ui.tblScores.setItem(tblindex,6,QtWidgets.QTableWidgetItem(str(i['score'])))
            tblindex += 1
        editwindow.ui.lblSelectedShooter.setText(str(data[0]['shooterid']) + ' ' +  sname)


    def CloseEditScoresWindow(self ,e):
        if not e:
            pass
        else:
            try:
                if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
                    pass
                else:
                    return
            except:
                print('No Key')
                return
        self.ui.lnEditScoreShooterName.clear()
        self.ui.lblSelectedShooter.setText('')
        self.ui.tblScores.clearContents()
        self.ui.tblScores.setRowCount(0)
        self.ui.ButtUpdate.setEnabled(0)
        self.close()

    def OpenEditScoresWindow(self):
        editwindow.ui.lblSelectedShooter.setStyleSheet("color: black")
        editwindow.ui.lblSelectedShooter.setText('') 
        editwindow.ui.ButtUpdate.setEnabled(0)
        shooterlist = list(map(lambda x : str(x['name']),mnslq.MNSLQuery(configfile).FetchShooterIfScore(session)))
        completer = QCompleter(shooterlist)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        editwindow.ui.lnEditScoreShooterName.setCompleter(completer)

        dtelist = list(map(lambda x : str(x['dte']), mnslq.MNSLQuery(configfile).FetchSessionDates(session)))
        editwindow.ui.comboBoxDate.addItem('')  
        editwindow.ui.comboBoxDate.addItems(dtelist)
        
        editwindow.ui.lblSession.setText(window.windowTitle()) 
        editwindow.show()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #self.setupUi(self)
        self.ui = Ui_MainWindow()        
        self.ui.setupUi(self)
        editmenup = self.ui.actionPerson
        editmenup.triggered.connect(self.SelectShooter)
        editmenus = self.ui.actionScores
        editmenus.triggered.connect(EditScoreWindow.OpenEditScoresWindow)
        editmenuc = self.ui.actionconfig
        editmenuc.triggered.connect(self.showconfig)
        viewmenusbs = self.ui.actionScores_By_Shooter
        viewmenusbs.triggered.connect(ScoresByShooter.OpenWindow)
        datemenuc = self.ui.actionChange_Date
        datemenuc.triggered.connect(lambda: self.ui.frameCal.show())
        aboutmenu = self.ui.actionAbout
        aboutmenu.triggered.connect(lambda: self.DisplayAboutDialog())
        
        self.ui.eventcomboBox.addItems(list(eventdict))
        self.ui.divcomboBox.addItems(list(divdict))
        self.ui.comboBoxGender.addItems(["Female","Male"])

        self.ui.divcomboBox.currentTextChanged.connect(self.check22)
        self.ui.saveButton.clicked.connect(self.ScoreSaveButt)
        self.ui.saveButton.keyPressEvent = self.ScoreSaveButt
        self.ui.Buttokayerrormsg.keyPressEvent = self.closeerrorbox
        self.ui.Buttokayerrormsg.clicked.connect(self.closeerrorbox)
        self.ui.ButtSelectShooter.keyPressEvent = self.fillshooteredit
        self.ui.ButtSelectShooter.clicked.connect(self.fillshooteredit)
        self.ui.ButtEditShooterCancel.keyPressEvent = self.CloseEditShooterBox
        self.ui.ButtEditShooterCancel.clicked.connect(self.CloseEditShooterBox)
        self.ui.ButtUpdateShooter.clicked.connect(self.updateshooter)
        self.ui.ButtConfigCancel.clicked.connect(self.closeconfig)
        self.ui.ButtConfigCancel.keyPressEvent = self.closeconfig
        self.ui.ButtConfigOkay.clicked.connect(self.SaveConfig)
        self.ui.ButtConfigOkay.keyPressEvent = self.SaveConfig
        self.ui.ButtGetDate.clicked.connect(self.updateDate)
        self.ui.ButtCalCancel.clicked.connect(lambda: self.ui.frameCal.hide())
        self.ui.ButtCalCancel.keyPressEvent = self.ui.frameCal.hide()
        
        
    def updateDate(self):
        global scoredate
        scoredate = self.ui.calendarWidget.selectedDate().toString('yyyy-MM-dd')
        self.ui.lblInfo.setText('Score Date: ' +  self.ui.calendarWidget.selectedDate().toString('yyyy-MM-dd'))
        self.ui.frameCal.hide()

    def SaveConfig(self, e):
        if not e:
            pass
        else:
            try:
                if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
                    pass
                else:
                    return
            except:
                print('No Key')
                return
        
        linedict = {'db_user':str(self.ui.lnConfigUser.text()),
                'db_pw':self.ui.lnConfigPass.text(),
                'db':self.ui.lnConfigDB.text(),
                'dbhost':self.ui.lnConfigDBHost.text()}
        sdict = {'session':self.ui.lnConfigSession.text()}
        CF.Config(configfile).Update('session',sdict)
        CF.Config(configfile).Update('database',linedict)
        read_config()
        self.ui.frameConfig.hide()
        self.setWindowTitle(f"""MNSL Scores - Session {session} Started 
                ({mnslq.MNSLQuery(configfile).FetchSessionStart()[0]['sstart']})""")


    def closeconfig(self, e):
        if not e:
            pass
        else:
            try:
                if e.key() == QtCore.Qt.Key_Return:
                    print('got enter')
                    pass
                else:
                    return
            except:
                print('no key')
                return
        self.ui.frameConfig.hide()
    
    def showconfig(self):
        self.ui.frameConfig.show()
        self.ui.lnConfigUser.setText(configdict['db_user'])
        self.ui.lnConfigPass.setText(configdict['db_pw'])
        self.ui.lnConfigDB.setText(configdict['db'])
        self.ui.lnConfigDBHost.setText(configdict['dbhost'])
        self.ui.lnConfigSession.setText(session)
        self.ui.lnConfigUser.setFocus()
        

    
    def CloseEditShooterBox(self,e):
        if not e:
            pass
        else:
            try:
                if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
                    pass
                else:
                    return
            except:
                print('No Key')
                return
        self.clearshooteredit('')
        self.ui.frameEditShooter.hide()
    
    def clearshooteredit(self, e):
        if not e:
            pass
        else:
            try:
                if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
                    pass
                else:
                    return
            except:
                print('No Key')
                return
        self.ui.lnEditShooter.setText('')
        self.ui.lnEditShooterFirst.setText('')
        self.ui.lnEditShooterLast.setText('')
        self.ui.lnEditShooterId.setText('')
        self.ui.lnEditShooterEmail.setText('')
        self.ui.lnEditShooterPhone.setText('')
        self.ui.lblEditShooterJoinedDate.setText('')
        self.ui.lnEditShooterPhone.setText('')
        self.ui.checkBoxStaff.setChecked(0)
        self.ui.checkBoxJunior.setChecked(0)
                
    def updateshooter(self, e):
        if not e:
            pass
        else:
            try:
                if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
                    pass
                else:
                    return
            except:
                print('No Key')
                return
        #update shooter info
        fname = self.ui.lnEditShooterFirst.text()
        lname = self.ui.lnEditShooterLast.text()
        gen = self.ui.comboBoxGender.currentIndex()
        sid = self.ui.lnEditShooterId.text()
        staff = 1 if self.ui.checkBoxStaff.checkState() > 0 else 0
        junior = 1 if self.ui.checkBoxJunior.checkState() > 0 else 0
        email = self.ui.lnEditShooterEmail.text()
        phone = self.ui.lnEditShooterPhone.text()
        infodict = {'fname':fname.title(),'lname':lname.title(),'gender':gen,'junior':junior,
                'staff':staff,'email':email,'phone':phone,'id':sid} 
        mnslq.MNSLQuery(configfile).UpdateShooter(infodict)
        self.clearshooteredit('')
        self.ui.lnEditShooter.setText('')
        self.ui.lnEditShooter.setFocus()
        LoadCompleters()

    def fillshooteredit(self,e):
        if not e:
            pass
        else:    
            try:
                if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
                    pass
                else:
                    return
            except:
                print('no key')
                return
        if self.ui.lnEditShooter.text() == '':
            pass
        else:
            Shooter = self.ui.lnEditShooter.text()
        data = mnslq.MNSLQuery(configfile).FetchShooter(Shooter)
        self.ui.lnEditShooterId.setText(str(data[0]['id']))
        self.ui.lnEditShooterFirst.setText(data[0]['fname'])
        self.ui.lnEditShooterLast.setText(data[0]['lname'])
        self.ui.comboBoxGender.setCurrentIndex(data[0]['gender'])
        self.ui.checkBoxJunior.setChecked(data[0]['junior'])
        self.ui.checkBoxStaff.setChecked(data[0]['staff'])
        self.ui.lnEditShooterEmail.setText(data[0]['email'])
        self.ui.lnEditShooterPhone.setText(data[0]['phone'])
        self.ui.lblEditShooterJoinedDate.setText(str(data[0]['dte']))
        self.ui.ButtUpdateShooter.setEnabled(1)

    def openshooteredit(self,e):
        self.ui.lnEditShooter.setFocus()
    
    def closeerrorbox(self,e):
        try:
            if e.key() == QtCore.Qt.Key_Return:
                print('got enter')
                self.ui.frameerrormsg.hide()
        except:
            print('no key')
        print(e)
        self.ui.frameerrormsg.hide()
        self.ui.score.setFocus()

    def ScoreSaveButt(self,e):
        if not e:
            pass
        else:    
            try:
                if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
                    pass
                else:
                    return
            except:
                print('no key')
                return
        
        # Validate
        if self.validatescore() == 1:
            # Clear last entry if validate completes
            self.ui.shooter.setText('')
            self.ui.caliber.setText('')
            self.ui.score.setText('')
            self.ui.eventcomboBox.setFocus()

    
     

    
    def validatescore(self):
        if self.ui.shooter.text() == '':
            return 0
        event = eventdict[self.ui.eventcomboBox.currentText()]
        eventtext = self.ui.eventcomboBox.currentText()
        div = divdict[self.ui.divcomboBox.currentText()]
        divtext = self.ui.divcomboBox.currentText()
        shooter = self.ui.shooter.text()
        cal = self.ui.caliber.text()
        score = self.ui.score.text()
        
        try:
            value = score
            int(value)
            if int(score) > 480:
                msg = f"Error {eventtext} {shooter} score is greater than 480"
                self.displayerror(msg)
                return 0
        except:    
            msg = f"Error {eventtext} {shooter} score needs to be greater than 0"
            self.displayerror(msg)
            return 0
        
        if div == 2 and cal != '.22':
            msg = 'Only .22 allowed in 22 division'
            self.displayerror(msg)
            return 0
        
        if len(cal) < 1:
            msg = 'You need a caliber'
            self.displayerror(msg)
            return 0

        sid = mnslq.MNSLQuery(configfile).FetchShooterId(shooter)
        #Check if shooter in DB
        if sid == 0:
            msg = f"Error:\nCannot find shooter '{shooter}' \nor \nDB issue\n\n Should we try to ADD shooter '{shooter}' "
            if self.DisplayErrorDialog(msg):
                sid = self.AddShooter(shooter)
                if sid > 0:
                    LoadCompleters()
                else:
                    msg = "Something went Wrong!"
                    self.DisplayErrorDialog(msg)
                    return
            else:
                return 0
           

        current_time = QTime.currentTime() 
        label_time = current_time.toString('HH:mm:ss')
        msg = f"{label_time}  {shooter.ljust(26)}: {eventtext.ljust(6)} {divtext.ljust(9)} {cal.ljust(5)} {score}"
        
        scoredict = {'dte':scoredate,'lnum':int(session),'score':int(score),'sid':sid,'eid':event,'did':div,'cal':cal}
        mnslq.MNSLQuery(configfile).AddScore(scoredict)
        self.ui.history.append(msg)
        return 1
  

    def AddShooter(self, sname):
        if mnslq.MNSLQuery(configfile).AddShooter(sname):
            sid = mnslq.MNSLQuery(configfile).FetchShooterId(sname)
            if len(sid) > 0 and sid != 0:
                return sid
            else:
                return 0
        else:
            return 0


    def DisplayErrorDialog(self,title,msg):
        ebox = CustomDialog(self)
        ebox.setStyleSheet("QLabel{font-size:20px;}")
        ebox.setWindowTitle(title)
        ebox.msgbox.setText(msg)
        ebox.setFixedSize(450,250)
        if ebox.exec_():
            return 1
        else:
            return 0
    
    def DisplayAboutDialog(self):
        abox = CustomDialog(self)
        abox.setStyleSheet("QLabel{font-size:18px;}")
        abox.setWindowTitle("About This Thing")
        msg = f"MNSL Score Keeper\n\nOct. 2022\nAuthor: Steggy\nver. {ver}\nA revamp of the Perl version"
        msg += f"\nInspired by Ira Weiny\nThanks for playing\nGithub:\nhttps://github.com/steggy/mnsl-score-app.git"
        abox.msgbox.setText(msg)
        abox.setFixedSize(455,280)
        abox.exec_()
        #if abox.exec_():
        #    return 1
        #else:
        #    return 0
    
    def displayerror(self, msg):
        self.ui.errorlog.append(msg)
        self.ui.lblerrorboxmsg.setText(msg)
        self.ui.frameerrormsg.show()
        self.ui.Buttokayerrormsg.setFocus()
    
    def check22(self):
        if self.ui.divcomboBox.currentText() == '22':
            self.ui.caliber.setText('.22')
        else: 
            self.ui.caliber.setText('')    
    
    def SelectShooter(self,e):
        window.ui.lnEditShooter.setFocus()
        window.ui.frameEditShooter.move(100,80)
        window.ui.frameEditShooter.show()


def read_config():
    global configlist
    global configdict
    global session
    configdict = dict(CF.Config(configfile).Fetch('database'))
    configlist = list(configdict.values())
    session = str(CF.Config(configfile).Fetch('session')[0][1])


def cancel_edit_shooter():
    window.ui.frameSelectShooter.hide()

def checksession():
    global window
    lnum = mnslq.MNSLQuery(configfile).FetchSession()
    if int(lnum) > int(session):
        msg = f"Current session {session} found {lnum} okay to use found"
        if window.DisplayErrorDialog('Achtung',msg):
            adjustsession(lnum)
        return
    wk = mnslq.MNSLQuery(configfile).Fetchweeks(session)
    if int(wk) >=12:
        msg = f"We might be done with session {session}\nShow config editor?"
        
        if window.DisplayErrorDialog('Achtung',msg):
            # we need to update DB with new league start date
            window.showconfig()


def adjustsession(ss):
    global session
    ss = str(ss)
    dct = {'session':ss}
    CF.Config(configfile).Update('session',dct)
    session = ss
    window.setWindowTitle(f"MNSL Scores - Session {session} Started ({mnslq.MNSLQuery(configfile).FetchSessionStart()[0]['sstart']})")


def restartapp():
    os.execv(__file__, sys.argv)



def LoadCompleters():
    shooterlist = list(map(lambda x : str(x['name']),mnslq.MNSLQuery(configfile).FetchAllShooters()))
    completer = QCompleter(shooterlist)
    completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    window.ui.shooter.setCompleter(completer)
    window.ui.lnEditShooter.setCompleter(completer)
    SBS.ui.lnShooter.setCompleter(completer)
    caliberlist = list(map(lambda x : str(x['name']),mnslq.MNSLQuery(configfile).FetchCaliber()))
    compl = QCompleter(caliberlist)
    compl.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    window.ui.caliber.setCompleter(compl)


def CheckDBConnection():
    try:
        DB = mnslq.MNSLQuery(configfile)
        return 1
    except Exception as e:
        window.ui.errorlog.append(str(e))
        #print(e)
        return 0

def main():
    global window
    global editwindow
    global viewwindow
    global scoredate
    global SBS
    newsession =''
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    editwindow = EditScoreWindow()
    SBS = ScoresByShooter()
    current_date = QDate.currentDate()
    # converting QDate object to string
    scoredate = current_date.toString('yyyy-MM-dd')
    window.ui.lblInfo.setText("Score Date: " + scoredate)
    window.setFixedSize(900,700)
    window.ui.history.setFontFamily("monospace")
    window.ui.frameerrormsg.move(100,100)
    window.ui.frameConfig.move(100,100)
    window.ui.frameerrormsg.hide()
    window.ui.frameEditShooter.hide()
    window.ui.frameConfig.hide()
    window.ui.frameCal.hide()
    
    
    window.show()
    read_config()
    if not CheckDBConnection():
        crap = input("DB Error!!!")
    window.setWindowTitle(f"MNSL Scores - Session {session} Started ({mnslq.MNSLQuery(configfile).FetchSessionStart()[0]['sstart']})")
    newsession = checksession()
    LoadCompleters()
    window.ui.ButtRestart.clicked.connect(restartapp)
    app.exec()

if __name__ == '__main__':
    main()





#EOF
    
