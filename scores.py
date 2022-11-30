#! /usr/bin/python3
import sys, time, os, json
from datetime import datetime
import dbhelper as DB
import readwriteconfig as CF
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QAction, QCompleter, QLineEdit, QStyledItemDelegate, QComboBox
from PyQt5.QtWidgets import QDialog, QPushButton, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QTime, QDate

configfile = "scores.conf"
#configlist = CF.Config(configfile).Fetch('database')
configdict = dict(CF.Config(configfile).Fetch('database'))
configlist = list(configdict.values())
session = str(CF.Config(configfile).Fetch('session')[0][1])
print(configdict)
print(configlist)

dbhost = ""
dbuser = ""
dbpass = ""
dbdb = ""
#session = str(CF.Config(configfile).Fetch('session')[0]['session'])
print("This is SESSION" ,session)

scoredate = ""
eventdict = {"PPC":1,"Tyro":2,"Rifle":3}
divdict = {"Open":1,"22":2,"Prod":3,"Revolver":4,"special":5}

#db1 = DB.dbh('192.168.33.88','mqttu','mqttu123','mqtt')
db1 = ""

#shooters = []

################################################################################################
# Convert UI to PyQt5 py file
################################################################################################
#os.system("/usr/bin/pyuic5 -x mainwindow.ui -o MainWindow.py")
os.system("pyuic5 -x mainwindow.ui -o MainWindow.py")
os.system("pyuic5 -x editscore.ui -o EditScore.py")
os.system("pyuic5 -x viewscoreswindow.ui -o ViewScoresWindow.py")
#from MainWindow import Ui_MainWindow
from MainWindow import *
from EditScore import *
from ViewScoresWindow import *


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
        #message = QLabel("Something happened, is that OK?")
        self.msgbox = QLabel()
        self.layout.addWidget(self.msgbox)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class ViewScoresWindow(QtWidgets.QMainWindow, Ui_ViewScoresWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(ViewScoresWindow, self).__init__(*args, **kwargs)
        #self.setupUi(self)
        self.ui = Ui_ViewScoresWindow()        
        self.ui.setupUi(self)
        self.setFixedSize(733,553) 
    
        self.ui.ButtShowScores.clicked.connect(self.loadscores)
    
    def loadscores(self, e):
        db3 = DB.dbh(dbhost,dbuser,dbpass,dbdb)
        sql = """select concat(fname, ' ', lname) as name,event.name as evt,division.name as divv,cal,score 
        from scores,shooters,event,division where shooterid = shooters.id and eid=event.id and did=division.id and 
        scores.dte='""" + viewwindow.ui.comboDate.currentText() + """"' order by fname,lname,scores.id;"""
        viewwindow.ui.tblScores.setColumnWidth(0,220)
        viewwindow.ui.tblScores.clearContents()
        viewwindow.ui.tblScores.setRowCount(0)
        try:
            data = db3.fetch(sql)
            if len(data) < 1:
                return
            viewwindow.ui.tblScores.setRowCount(len(data))
            tblindex = 0
            for i in data:
                viewwindow.ui.tblScores.setItem(tblindex,0,QtWidgets.QTableWidgetItem(str(i['name'])))
                viewwindow.ui.tblScores.setItem(tblindex,1,QtWidgets.QTableWidgetItem(str(i['evt'])))
                viewwindow.ui.tblScores.setItem(tblindex,2,QtWidgets.QTableWidgetItem(str(i['divv'])))
                viewwindow.ui.tblScores.setItem(tblindex,3,QtWidgets.QTableWidgetItem(str(i['cal'])))
                viewwindow.ui.tblScores.setItem(tblindex,4,QtWidgets.QTableWidgetItem(str(i['score'])))
                tblindex +=1
        except:
            return

    def OpenViewScoresWindow(self):
        #editwindow.ui.lblSelectedShooter.setStyleSheet("color: black")
        #editwindow.ui.lblSelectedShooter.setText('') 
        #editwindow.ui.ButtUpdate.setEnabled(0)
        viewwindow.ui.comboDate.clear()
        viewwindow.ui.tblScores.clearContents()
        viewwindow.ui.tblScores.setRowCount(0)

        db3 = DB.dbh(dbhost,dbuser,dbpass,dbdb)
        sql = "select dte from scores where leaguenum = " + session + " group by dte order by dte desc;"
        try:
            data = db3.fetch(sql)
            for i in data:
                viewwindow.ui.comboDate.addItem(str(i['dte']))
        except Exception as e:
            print("DB Error ", e)
        
        viewwindow.ui.lblSession.setText(window.windowTitle()) 
        
        viewwindow.show()    



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
        delegate = ReadOnlyDelegate(self.ui.tblScores)
        self.ui.tblScores.setItemDelegateForColumn(0, delegate)
        self.ui.tblScores.setItemDelegateForColumn(1, delegate)
        self.ui.tblScores.setItemDelegateForColumn(2, delegate)
        self.ui.ButtUpdate.clicked.connect(self.UpdateScores)

    
    
    def closeEvent(self, event):
        self.ui.lnEditScoreShooterName.setText('')
        event.accept()
    


    
    def UpdateScores(self):
        db6 = DB.dbh(dbhost,dbuser,dbpass,dbdb)
        #db6.execute(sql)
        print("The value in the box ", eventdict[combotblEventList[0].currentText()])
        #event = eventdict[self.ui.eventcomboBox.currentText()]
        #eventtext = self.ui.eventcomboBox.currentText() 
        rowCount = self.ui.tblScores.rowCount()
        columnCount = self.ui.tblScores.columnCount()
        cbox = [3,4]
        sqlquery = []
        for row in range(rowCount):
            rowData = 'update scores '
            for column in range(columnCount):
                cellitem = self.ui.tblScores.item(row,column)
                #if(cellitem and cellitem.text):
                if column == 0:
                    rid = cellitem.text()
                if column == 3:
                    event = eventdict[combotblEventList[row].currentText()]
                    rowData = rowData + 'set eid=' + str(event)
                if column == 4:    
                    div = divdict[combotblDivList[row].currentText()]
                    rowData = rowData + ',did=' + str(div)
                if column == 5:
                    rowData = rowData + ",cal='" + cellitem.text() + "'"
                if column == 6:
                    if len(cellitem.text()) < 1:
                        print('score blank')
                        rowData = "delete from scores"
                        
                    else:
                        rowData = rowData + ',score=' + cellitem.text()

                #else:
                    #self.ui.lblSelectedShooter.setText(self.ui.lblSelectedShooter.text() + ' Empty Cell')
                    #return
            rowData = rowData + ' where id=' + rid    
            sqlquery.append(rowData)        
            print(rowData + '\n')
        for i in sqlquery:
            print(i)
            db6.execute(i)
            window.ui.history.append(i)
        
        self.ui.lblSelectedShooter.setStyleSheet("color: red")
        current_time = QTime.currentTime()

        # converting QTime object to string
        label_time = current_time.toString('HH:mm:ss')

        self.ui.lblSelectedShooter.setText(self.ui.lblSelectedShooter.text() + ' Updated ' + label_time)
        #cellitem = editwindow.ui.tblScores.item(0,2)
        #print(cellitem.text())
        

        #reload table at end

    def addscorerows(self, e):
        def addrow():
            global combotblEventList
            global combotblDivList
            win = EditScoreWindow(self)
            editwindow.ui.lblSelectedShooter.setStyleSheet("color: black")
            sname = editwindow.ui.lnEditScoreShooterName.text()
            sdte = editwindow.ui.comboBoxDate.currentText()
            sql = """select scores.id,shooterid,scores.dte,event.name as eventname,division.name as divname,cal,score 
            from scores,event,division where shooterid = (select id from shooters 
            where concat(fname,' ',lname) = '""" + sname + """') and dte = '""" + sdte + """' 
            and scores.eid = event.id and scores.did=division.id;"""
            db4 = DB.dbh(dbhost,dbuser,dbpass,dbdb)
            try:
                data = db4.fetch(sql)
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
                cellitem = editwindow.ui.tblScores.item(0,2)
                print(cellitem.text())
            except Exception as e:
                print("DB Error ", e)
            
            #editwindow.ui.lnEditScoreShooterName.setText('')
        
        try:
            if e.key() == QtCore.Qt.Key_Return:
                print('got enter')
                addrow()
        except:
            print('no key')
        addrow()
    
    


    def CloseEditScoresWindow(self):
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
        db3 = DB.dbh(dbhost,dbuser,dbpass,dbdb)
        sql = "select dte from scores where leaguenum = " + session + " group by dte order by dte desc;"
        try:
            data = db3.fetch(sql)
        except Exception as e:
            print("DB Error ", e)
        
        for i in data:
            editwindow.ui.comboBoxDate.addItem(str(i['dte']))
        
        editwindow.ui.lblSession.setText(window.windowTitle()) 
        editwindow.show()    
    
    


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #self.setupUi(self)
        self.ui = Ui_MainWindow()        
        self.ui.setupUi(self)
        self.scores = ViewScoresWindow(self)
        editmenup = self.ui.actionPerson
        editmenup.triggered.connect(self.SelectShooter)
        editmenus = self.ui.actionScores
        editmenus.triggered.connect(EditScoreWindow.OpenEditScoresWindow)
        editmenuc = self.ui.actionconfig
        editmenuc.triggered.connect(self.showconfig)
        viewmenus = self.ui.actionViewScores
        viewmenus.triggered.connect(ViewScoresWindow.OpenViewScoresWindow)
        datemenuc = self.ui.actionChange_Date
        datemenuc.triggered.connect(lambda: self.ui.frameCal.show())
        

        
        #editmenup.addAction(editAction)
        #shoot = get_shooters()
        #stuff = ["apple","grace","steggy"]
        #completer = QCompleter(stuff)
        #self.ui.shooter.setCompleter(completer)
        #self.ui.eventcomboBox.addItems(["PPC","Tyro","Rifle"])
        self.ui.eventcomboBox.addItems(list(eventdict))
        #self.ui.divcomboBox.addItems(["Open","22","Prod","Revolver","Special"])
        self.ui.divcomboBox.addItems(list(divdict))
        self.ui.comboBoxGender.addItems(["Female","Male"])

        self.ui.divcomboBox.currentTextChanged.connect(self.check22)
        #self.ui.saveButton.clicked.connect(self.savebuttclk)
        self.ui.saveButton.clicked.connect(self.ScoreSaveButt)
        #self.ui.saveButton.keyPressEvent = self.savebuttent
        self.ui.saveButton.keyPressEvent = self.ScoreSaveButt
       #ScoreSaveButt 
        self.ui.Buttokayerrormsg.keyPressEvent = self.closeerrorbox
        self.ui.Buttokayerrormsg.clicked.connect(self.closeerrorbox)
        #self.ui.editpersonokayButton.keyPressEvent = self.openshooteredit
        self.ui.ButtSelectShooter.keyPressEvent = self.fillshooteredit
        self.ui.ButtSelectShooter.clicked.connect(self.fillshooteredit)
        #self.ui.ButtEditShooterCancel.
        #self.ui.lnEditShooter.focusInEvent(self.clearshooteredit)
        self.ui.ButtEditShooterCancel.keyPressEvent = self.clearshooteredit
        self.ui.ButtEditShooterCancel.clicked.connect(self.clearshooteredit)
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
        thedate = self.ui.calendarWidget.selectedDate()
        fdate = thedate.toString('yyyy-MM-dd')
        scoredate = fdate
        self.ui.lblInfo.setText('Score Date: ' +  scoredate)
        print(fdate)
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
        self.setWindowTitle(f"MNSL Scores - Session {session} Started ({findSessionStart()})")

            
    
    def closeconfig(self, e):
        try:
            if e.key() == QtCore.Qt.Key_Return:
                print('got enter')
                self.ui.frameConfig.hide()
        except:
            print('no key')
        self.ui.frameConfig.hide()
    
    def showconfig(self):
        self.ui.frameConfig.show()
        self.ui.lnConfigUser.setText(configdict['db_user'])
        self.ui.lnConfigPass.setText(configdict['db_pw'])
        self.ui.lnConfigDB.setText(configdict['db'])
        self.ui.lnConfigDBHost.setText(configdict['dbhost'])
        self.ui.lnConfigSession.setText(session)
        self.ui.lnConfigUser.setFocus()
        

    def clearshooteredit(self, e):
        def clearfields():
            self.ui.lnEditShooter.setText('')
            self.ui.lnEditShooterFirst.setText('')
            self.ui.lnEditShooterLast.setText('')
            self.ui.lnEditShooterId.setText('')
            self.ui.frameEditShooter.hide()
            self.ui.lnEditShooterEmail.setText('')
            self.ui.lnEditShooterPhone.setText('')
            self.ui.lblEditShooterJoinedDate.setText('')
        try:
            if e.key() == QtCore.Qt.Key_Return:
                print('got enter')
                clearfields()
        except:
            print('no key')
        clearfields()    
        
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
        #staff = self.ui.checkBoxStaff.checkState()
        id = self.ui.lnEditShooterId.text()
        staff = 1 if self.ui.checkBoxStaff.checkState() > 0 else 0
        junior = 1 if self.ui.checkBoxJunior.checkState() > 0 else 0
        print(lname, gen, staff, junior)
        
        sql =f"""update shooters set fname='{fname.title()}',lname='{lname.title()}', 
        gender={gen},junior={junior},staff={staff},email='{self.ui.lnEditShooterEmail.text()}' 
        where id={id}""" 
        print(sql)
        db2 = DB.dbh(dbhost,dbuser,dbpass,dbdb)
        db2.execute(sql)
        self.ui.lnEditShooter.setText('')
        self.ui.lnEditShooter.setFocus()



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
        db2 = DB.dbh(*configlist)
        sql = "select id,dte,fname,lname,gender,junior,staff,email,phone from shooters where concat(fname, ' ',lname) ='" + Shooter + "';"
        try:
            data = db2.fetch(sql)
            #return data
            #window.lblwater.setText(str(data[0]['ldate']))
            print(data[0]['fname'])
            print(data[0]['gender'])
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
            print(self.ui.checkBoxStaff.checkState())
        except Exception as e:
            print("DB Error ", e)
    
    

    def openshooteredit(self,e):
        self.ui.lnEditShooter.setFocus()
        pass
        #window.ui.divcomboBox
    
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
        
        print("Should Validate")
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
        #Check if shooter in DB
        db2 = DB.dbh(dbhost,dbuser,dbpass,dbdb)
        
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
        
        sql = "select id from shooters where concat(fname, ' ', lname) ='" + shooter + "'"
        try:
            data = db2.fetch(sql)
            print('SIZE OF DATA ',len(data))
            if len(data) < 1:
                msg = f"Error:\nCannot find shooter '{shooter}' \nor \nDB issue\n\n Should we try to ADD shooter '{shooter}' "
                if self.DisplayErrorDialog(msg):
                    sid = self.AddShooter(shooter)
                    if sid > 0:
                        shooterid = sid
                        LoadCompleters()
                    else:
                        msg = "Something went Wrong!"
                        self.DisplayErrorDialog(msg)
                        return
            else:
                shooterid = data[0]['id']
        except Exception as e:
            print('There was an error ',e)
            

        
            #self.displayerror(msg)
            return

        current_time = QTime.currentTime() 
        label_time = current_time.toString('HH:mm:ss')

        print(f"Input {event} {eventtext} {div} {shooter} ID {shooterid} {cal} {score}")
        msg = f"{label_time}  {shooter.ljust(26)}: {eventtext.ljust(6)} {divtext.ljust(9)} {cal.ljust(5)} {score}"
        #msg = "%s %s %s26 %s %s % (eventtext,divtext,shooter,cal,score})"
        sql = f"""insert into scores (dte,leaguenum,score,shooterid,eid,did,cal) values
        ('{scoredate}',{session},{score},{shooterid},{event},{div},'{cal}')"""
        print(sql)
        db2.execute(sql)
        self.ui.history.append(msg)
        return 1
  

    def AddShooter(self, sname):
        db2 = DB.dbh(dbhost,dbuser,dbpass,dbdb)
        sn = sname.split()
        
        sql = f"insert into shooters (fname, lname) values ('{sn[0].title()}','{' '.join(sn[1:]).title()}')"
        print(sql)
        try:
            db2.execute(sql)
        except Exception as e:
            self.errorlog(e)
            return
        try:
            sql = f"select id from shooters where concat(fname, ' ', lname) ='{sname}' "
            data = db2.fetch(sql)
            if len(data) > 0:
                return data[0]['id']
            else:
                return 0
        except Exception as e:
            self.errorlog(e)
            return

    def DisplayErrorDialog(self,msg):
        ebox = CustomDialog(self)
        ebox.setStyleSheet("QLabel{font-size:20px;}")
        ebox.setWindowTitle('Error!')
        ebox.msgbox.setText(msg)
        ebox.setFixedSize(450,250)
        if ebox.exec_():
            print('YES WE DO')
            return 1
        else:
            print('SUCK IT!!')
            return 0
    
    def displayerror(self, msg):
        self.ui.errorlog.append(msg)
        self.ui.lblerrorboxmsg.setText(msg)
        self.ui.frameerrormsg.show()
        self.ui.Buttokayerrormsg.setFocus()
    

    def check22(self):
        if self.ui.divcomboBox.currentText() == '22':
            self.ui.caliber.setText('.22')
            #self.ui.caliber.setFocus()
        else: 
            self.ui.caliber.setText('')    

        #print(self.ui.divcomboBox.currentText())
    
    def SelectShooter(self,e):
        
        window.ui.lnEditShooter.setFocus()
        print('EDIT Person')
        window.ui.frameEditShooter.move(100,80)
        window.ui.frameEditShooter.show()
    





def get_shooters():
    shooterlist = []
    db2 = DB.dbh(*configlist)
    sql = "select concat(fname, ' ', lname) as name from shooters;"
    try:
        data = db2.fetch(sql)
    except Exception as e:
        print("DB Error ", e)
    for i in data:
        shooterlist.append(i['name'])    
    return shooterlist

def loadcaliber():
    caliberlist = []
    db2 = DB.dbh(*configlist)
    sql = "select name from caliber;"
    try:
        data = db2.fetch(sql)
    except Exception as e:
        print("DB Error ", e)
    for i in data:
        caliberlist.append(i['name'])    
    return caliberlist

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
    db2 = DB.dbh(*configlist)
    sql = "select leaguenum from scores group by leaguenum order by leaguenum desc limit 1;"
    try:
        data = db2.fetch(sql)
    except Exception as e:
        print("DB Error ", e)
    if int(data[0]['leaguenum']) > int(session):
        msg = f"Current session {session} found {data[0]['leaguenum']} okay to use found"
        if window.DisplayErrorDialog(msg):
            adjustsession(data[0]['leaguenum'])

        
        #return int(data[0]['leaguenum'])

def adjustsession(ss):
    global session
    with open(configfile) as file:
        lines = file.readlines()
    configlines = [line.rstrip() for line in lines]
    session = str(ss)
    configlines[4] = "session=" + str(ss)
    with open(configfile, 'w') as f:
        for line in configlines:
            f.write(f"{line}\n")
    #window.ui.framesessioncheck.hide()
    window.setWindowTitle(f"MNSL Scores - Session {session} Started ({findSessionStart()})")


def findSessionStart():
    db2 = DB.dbh(*configlist)
    sql = "select min(dte) as sstart from scores where leaguenum =" + session + ";"
    data = db2.fetch(sql)
    print("Session Start " , data[0]['sstart'])
    return data[0]['sstart']
    


def restartapp():
    os.execv(__file__, sys.argv)



def LoadCompleters():
    shoot = get_shooters()
    completer = QCompleter(shoot)
    completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    window.ui.shooter.setCompleter(completer)
    window.ui.lnEditShooter.setCompleter(completer)
    editwindow.ui.lnEditScoreShooterName.setCompleter(completer)
    calibers = loadcaliber()
    compl = QCompleter(calibers)
    compl.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    window.ui.caliber.setCompleter(compl)

def main():
    global window
    global editwindow
    global viewwindow
    global scoredate
    newsession =''

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    editwindow = EditScoreWindow()
    viewwindow = ViewScoresWindow()

    
    current_date = QDate.currentDate()

    # converting QDate object to string
    scoredate = current_date.toString('yyyy-MM-dd')
    window.ui.lblInfo.setText("Score Date: " + scoredate)

    try:
        db1 = DB.dbh(dbhost,dbuser,dbpass,dbdb)
    except Exception as e:
        print(e)   
    
    try:
        shooters = get_shooters()
    except Exception as e: 
        print("DB Error in main ", e)    
    
    window.setFixedSize(900,700)
    LoadCompleters()

    window.ui.history.setFontFamily("monospace")
    #window.ui.frameEditShooter.hide()
    window.ui.frameerrormsg.move(100,100)
    window.ui.frameConfig.move(100,100)
    #window.ui.lblerrorboxmsg.setText('')
    window.ui.frameerrormsg.hide()
    window.ui.frameEditShooter.hide()
    window.ui.frameConfig.hide()
    window.ui.frameCal.hide()
    
    #finSessionStart()
    window.setWindowTitle(f"MNSL Scores - Session {session} Started ({findSessionStart()})")
    
    window.show()
    read_config()
    newsession = checksession()
    
    #editwindow.show()
    
    #window.ui.editpersoncancelButton.clicked.connect(cancel_edit_shooter)
    window.ui.ButtRestart.clicked.connect(restartapp)
    #window.btnofficeon.clicked.connect(lambda: officelights('on'))
    #window.btnofficeoff.clicked.connect(lambda: officelights('off'))
    #window.btnkiton.clicked.connect(lambda: kitlights('on'))
    #window.btnkitoff.clicked.connect(lambda: kitlights('off'))
    #window.btnlivon.clicked.connect(lambda: livlights('on'))
    #window.btnlivoff.clicked.connect(lambda: livlights('off'))
    #window.btnmasteroff.clicked.connect(lambda: masterlights('off'))
    #window.btnmasteron.clicked.connect(lambda: masterlights('on'))
    #window.btngamelampon.clicked.connect(lambda: gamelights('on'))
    #window.btngamelampoff.clicked.connect(lambda: gamelights('off'))
    ##window.lblwater.setText(str(getwater()))
    ##window.lblthermotemp.setText(str(getthermotemp()))
    ##Call temp update
    #getthermotemp()
    #update_temp_timer = QTimer()
    #update_temp_timer.timeout.connect(getthermotemp)
    #update_temp_timer.start(61000)
    ##Call water update
    ##Call mobile temp
    #getmobiletemp()
    #update_mobile_temp_timer = QTimer()
    #update_mobile_temp_timer.timeout.connect(getmobiletemp)
    #update_mobile_temp_timer.start(60000)

    #getwater()
    #update_water_display = QTimer()
    #update_water_display.timeout.connect(getwater)
    #update_water_display.start(3600000)
    app.exec()

if __name__ == '__main__':
    main()





#EOF
    
