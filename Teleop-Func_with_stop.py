# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QFileDialog
from PyQt5.QtCore import QRunnable,pyqtSlot,pyqtSignal,QThreadPool, QObject
import sys
from URCommunicationClass import UR_Communication

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    result
        `object` data returned from processing, anything

    '''

    result = pyqtSignal(object)


class Get_Modbus_data_from_robot(QRunnable):
    def __init__(self,RobotCommunicationClass):
        super(Get_Modbus_data_from_robot, self).__init__()
        self.SelectedRobot = RobotCommunicationClass
        self.signals = WorkerSignals()
        self.counter = 0


    @pyqtSlot()
    def run(self):
        try:
            self.SelectedRobot.Modbus_dataframe_update_read_registers()
        except:
            print("Communication failed")

        finally:
            self.signals.result.emit(self.SelectedRobot.Modbus_df_reg)


class Ui_MainWindow(object):
    def __init__(self,MainWindow_qtwidget):
        self.setupUi(MainWindow_qtwidget)
        self.CreateConnections()
        self.MainWindow = MainWindow_qtwidget
        self.MainWindow.setWindowTitle("Sergi Ponsà Cobas TFM Project")
        self.Robots = []
        self.Robots_ip = []
        self.Robots_serial = []
        self.Robots_type = []
        self.Robot_OperationMode = 0 #To allow me toggle from one to another
        self.Robot_Freedrive = True #To allow me toggle from one to another

        #Determine the object communication to use
        self.SelectedRobot = None
        self.SelectedRobotOld = None

        #Modbus Refresh timer
        self.timer_Modbus = QtCore.QTimer(self.MainWindow)
        self.time_refresh_Modbus = 2000

        #Modbus thread
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())


        #To debug, set to false
        self.RobotConnectionRequired = True
    def setupUi(self, MainWindow):

        #MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(774, 306)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        #Multiple windows
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")

        #NewRobotWindow
        self.pageAssignNewRobot = QtWidgets.QWidget()
        self.pageAssignNewRobot.setObjectName("pageAssignNewRobot")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.pageAssignNewRobot)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_2.addItem(spacerItem)
        self.TitleNewRobot = QtWidgets.QLabel(self.pageAssignNewRobot)
        self.TitleNewRobot.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.TitleNewRobot.setObjectName("TitleNewRobot")
        self.verticalLayout_2.addWidget(self.TitleNewRobot)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 26, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem1)
        self.MessageRobotIP = QtWidgets.QLabel(self.pageAssignNewRobot)
        self.MessageRobotIP.setAlignment(QtCore.Qt.AlignCenter)
        self.MessageRobotIP.setWordWrap(False)
        self.MessageRobotIP.setObjectName("MessageRobotIP")
        self.verticalLayout.addWidget(self.MessageRobotIP)
        spacerItem2 = QtWidgets.QSpacerItem(20, 49, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem2)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.ConnectRobotBt = QtWidgets.QPushButton(self.pageAssignNewRobot)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ConnectRobotBt.sizePolicy().hasHeightForWidth())
        self.ConnectRobotBt.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ConnectRobotBt.setFont(font)
        self.ConnectRobotBt.setObjectName("ConnectRobotBt")
        self.gridLayout_4.addWidget(self.ConnectRobotBt, 2, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem3, 0, 0, 1, 1)
        self.InsertIPField = QtWidgets.QLineEdit(self.pageAssignNewRobot)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.InsertIPField.sizePolicy().hasHeightForWidth())
        self.InsertIPField.setSizePolicy(sizePolicy)
        self.InsertIPField.setMinimumSize(QtCore.QSize(209, 23))
        self.InsertIPField.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.InsertIPField.setFont(font)
        self.InsertIPField.setText("")
        self.InsertIPField.setAlignment(QtCore.Qt.AlignCenter)
        self.InsertIPField.setObjectName("InsertIPField")
        self.gridLayout_4.addWidget(self.InsertIPField, 0, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 19, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout_4.addItem(spacerItem4, 1, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem5, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        spacerItem6 = QtWidgets.QSpacerItem(20, 146, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.stackedWidget.addWidget(self.pageAssignNewRobot)
        self.pageMainCommands = QtWidgets.QWidget()

        #Main Command Window
        self.pageMainCommands.setObjectName("pageMainCommands")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.pageMainCommands)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.StopRobotBt = QtWidgets.QPushButton(self.pageMainCommands)
        self.StopRobotBt.setStyleSheet("background-color: rgb(255, 0, 0);\n"\
                                        "font: 12pt \"Sans Serif\";")
        self.StopRobotBt.setObjectName("StopRobotBt")
        self.verticalLayout_3.addWidget(self.StopRobotBt)
        self.tabWidget = QtWidgets.QTabWidget(self.pageMainCommands)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(True)

        #TabWindows of Main Command Window
        self.tabWidget.setObjectName("tabWidget")
        self.DashBoardtab = QtWidgets.QWidget()

        #DashBoard tab of TabWindows of Main Command Window
        self.DashBoardtab.setObjectName("DashBoardtab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.DashBoardtab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollAreaDash = QtWidgets.QScrollArea(self.DashBoardtab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaDash.sizePolicy().hasHeightForWidth())
        self.scrollAreaDash.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.scrollAreaDash.setFont(font)
        self.scrollAreaDash.setWidgetResizable(True)
        self.scrollAreaDash.setObjectName("scrollAreaDash")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 704, 298))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.ReleaseBreakesDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.ReleaseBreakesDashBt.setObjectName("ReleaseBreakesDashBt")
        self.gridLayout_3.addWidget(self.ReleaseBreakesDashBt, 3, 1, 1, 1)
        self.ClosePopUpDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.ClosePopUpDashBt.setObjectName("ClosePopUpDashBt")
        self.gridLayout_3.addWidget(self.ClosePopUpDashBt, 9, 3, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem7, 0, 1, 1, 1)
        self.PowerOffDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.PowerOffDashBt.setObjectName("PowerOffDashBt")
        self.gridLayout_3.addWidget(self.PowerOffDashBt, 1, 3, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem8, 10, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem9, 6, 1, 1, 1)
        self.PauseProgramDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.PauseProgramDashBt.setObjectName("PauseProgramDashBt")
        self.gridLayout_3.addWidget(self.PauseProgramDashBt, 7, 3, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem10, 14, 1, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem11, 12, 1, 1, 1)
        self.PowerOnDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.PowerOnDashBt.setObjectName("PowerOnDashBt")
        self.gridLayout_3.addWidget(self.PowerOnDashBt, 1, 1, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem12, 2, 1, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem13, 1, 4, 1, 1)
        self.RunProgramDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.RunProgramDashBt.setObjectName("RunProgramDashBt")
        self.gridLayout_3.addWidget(self.RunProgramDashBt, 7, 1, 1, 1)
        self.LoadInstallationDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.LoadInstallationDashBt.setObjectName("LoadInstallationDashBt")
        self.gridLayout_3.addWidget(self.LoadInstallationDashBt, 5, 1, 1, 1)
        self.ActualRobotModeBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.ActualRobotModeBt.setObjectName("ActualRobotModeBt")
        self.gridLayout_3.addWidget(self.ActualRobotModeBt, 11, 3, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem14, 1, 0, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem15, 8, 1, 1, 1)
        self.CloseSafetyPopUPDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.CloseSafetyPopUPDashBt.setObjectName("CloseSafetyPopUPDashBt")
        self.gridLayout_3.addWidget(self.CloseSafetyPopUPDashBt, 13, 3, 1, 1)
        self.OpenPopUpDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.OpenPopUpDashBt.setObjectName("OpenPopUpDashBt")
        self.gridLayout_3.addWidget(self.OpenPopUpDashBt, 9, 1, 1, 1)
        self.WriteLogDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.WriteLogDashBt.setObjectName("WriteLogDashBt")
        self.gridLayout_3.addWidget(self.WriteLogDashBt, 11, 1, 1, 1)
        self.ChangeOperationalModeDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.ChangeOperationalModeDashBt.setObjectName("ChangeOperationalModeDashBt")
        self.gridLayout_3.addWidget(self.ChangeOperationalModeDashBt, 13, 1, 1, 1)
        self.ActualProgramDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.ActualProgramDashBt.setObjectName("ActualProgramDashBt")
        self.gridLayout_3.addWidget(self.ActualProgramDashBt, 3, 3, 1, 1)
        self.UnlockProtectiveStopDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.UnlockProtectiveStopDashBt.setObjectName("UnlockProtectiveStopDashBt")
        self.gridLayout_3.addWidget(self.UnlockProtectiveStopDashBt, 15, 3, 1, 1)
        spacerItem16 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem16, 16, 1, 1, 1)
        self.LoadProgramDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.LoadProgramDashBt.setObjectName("LoadProgramDashBt")
        self.gridLayout_3.addWidget(self.LoadProgramDashBt, 5, 3, 1, 1)
        self.ActualSafetyModeDashBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.ActualSafetyModeDashBt.setObjectName("ActualSafetyModeDashBt")
        self.gridLayout_3.addWidget(self.ActualSafetyModeDashBt, 15, 1, 1, 1)
        spacerItem17 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem17, 4, 1, 1, 1)
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem18, 1, 2, 1, 1)
        self.scrollAreaDash.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollAreaDash, 0, 0, 1, 1)
        self.tabWidget.addTab(self.DashBoardtab, "")

        #TCPIP tab of TabWindows of Main Command Window
        self.tabTCPIP = QtWidgets.QWidget()
        self.tabTCPIP.setObjectName("tabTCPIP")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tabTCPIP)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.scrollAreaTCPIP = QtWidgets.QScrollArea(self.tabTCPIP)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.scrollAreaTCPIP.setFont(font)
        self.scrollAreaTCPIP.setWidgetResizable(True)
        self.scrollAreaTCPIP.setObjectName("scrollAreaTCPIP")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 718, 181))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.FreeDriveTCPBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.FreeDriveTCPBt.setObjectName("FreeDriveTCPBt")
        self.gridLayout_5.addWidget(self.FreeDriveTCPBt, 1, 1, 1, 1)
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem19, 1, 0, 1, 1)
        self.ExecuteScriptTCPBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.ExecuteScriptTCPBt.setObjectName("ExecuteScriptTCPBt")
        self.gridLayout_5.addWidget(self.ExecuteScriptTCPBt, 1, 3, 1, 1)
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem20, 1, 2, 1, 1)
        self.ComandTCPText = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents_3)
        self.ComandTCPText.setObjectName("ComandTCPText")
        self.ComandTCPText.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.ComandTCPText.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.gridLayout_5.addWidget(self.ComandTCPText, 3, 1, 1, 1)
        spacerItem21 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem21, 2, 1, 1, 1)
        self.SendScriptTCPBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.SendScriptTCPBt.setObjectName("SendScriptTCPBt")
        self.gridLayout_5.addWidget(self.SendScriptTCPBt, 3, 3, 1, 1)
        spacerItem22 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem22, 1, 4, 1, 1)
        spacerItem23 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem23, 0, 1, 1, 1)
        spacerItem24 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem24, 4, 1, 1, 1)
        self.scrollAreaTCPIP.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout_5.addWidget(self.scrollAreaTCPIP)
        self.tabWidget.addTab(self.tabTCPIP, "")

        #Modbus tab of TabWindows of Main Command Window
        self.tabModBus = QtWidgets.QWidget()
        self.tabModBus.setObjectName("tabModBus")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tabModBus)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scrollAreaModbus = QtWidgets.QScrollArea(self.tabModBus)
        self.scrollAreaModbus.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollAreaModbus.setWidgetResizable(True)
        self.scrollAreaModbus.setObjectName("scrollAreaModbus")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 718, 181))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.listWidgetRegisterNumber = QtWidgets.QListWidget(self.scrollAreaWidgetContents_2)
        self.listWidgetRegisterNumber.setStyleSheet("font: 12pt \"Sans Serif\";")
        self.listWidgetRegisterNumber.setObjectName("listWidgetRegisterNumber")
        self.vsRN = self.listWidgetRegisterNumber.verticalScrollBar()
        item = QtWidgets.QListWidgetItem()
        self.listWidgetRegisterNumber.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetRegisterNumber.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetRegisterNumber.addItem(item)
        self.horizontalLayout_2.addWidget(self.listWidgetRegisterNumber)
        self.listWidgetRegisterDescription = QtWidgets.QListWidget(self.scrollAreaWidgetContents_2)
        self.listWidgetRegisterDescription.setStyleSheet("font: 12pt \"Sans Serif\";")
        self.listWidgetRegisterDescription.setObjectName("listWidgetRegisterDescription")
        self.vsRD = self.listWidgetRegisterDescription.verticalScrollBar()
        item = QtWidgets.QListWidgetItem()
        self.listWidgetRegisterDescription.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetRegisterDescription.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetRegisterDescription.addItem(item)
        self.horizontalLayout_2.addWidget(self.listWidgetRegisterDescription)
        self.listWidgetRegisterValue = QtWidgets.QListWidget(self.scrollAreaWidgetContents_2)
        self.listWidgetRegisterValue.setStyleSheet("font: 12pt \"Sans Serif\";")
        self.listWidgetRegisterValue.setObjectName("listWidgetRegisterValue")
        self.vsRV = self.listWidgetRegisterValue.verticalScrollBar()
        item = QtWidgets.QListWidgetItem()
        self.listWidgetRegisterValue.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetRegisterValue.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetRegisterValue.addItem(item)
        self.horizontalLayout_2.addWidget(self.listWidgetRegisterValue)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.scrollAreaModbus.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.addWidget(self.scrollAreaModbus)
        self.tabWidget.addTab(self.tabModBus, "")

        #Remote Control tab of TabWindows of Main Command Window
        self.tabRemoteControl = QtWidgets.QWidget()
        self.tabRemoteControl.setObjectName("tabRemoteControl")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tabRemoteControl)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.tabWidgetControls = QtWidgets.QTabWidget(self.tabRemoteControl)
        self.tabWidgetControls.setObjectName("tabWidgetControls")

        #Joint Control tab of Remote Control tab of TabWindows of Main Command Window
        self.tabJointControl = QtWidgets.QWidget()
        self.tabJointControl.setObjectName("tabJointControl")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tabJointControl)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.scrollArea_4 = QtWidgets.QScrollArea(self.tabJointControl)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 904, 569))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_4)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.JointControlDecWrist1Bt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.JointControlDecWrist1Bt.setObjectName("JointControlDecWrist1Bt")
        self.horizontalLayout_6.addWidget(self.JointControlDecWrist1Bt)
        self.JointControlIncWrist1Bt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.JointControlIncWrist1Bt.setObjectName("JointControlIncWrist1Bt")
        self.horizontalLayout_6.addWidget(self.JointControlIncWrist1Bt)
        self.gridLayout_8.addLayout(self.horizontalLayout_6, 14, 2, 1, 1)
        self.labelJointControlShoulder = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.labelJointControlShoulder.setObjectName("labelJointControlShoulder")
        self.gridLayout_8.addWidget(self.labelJointControlShoulder, 6, 2, 1, 1)
        self.labelJointControlWrist1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.labelJointControlWrist1.setObjectName("labelJointControlWrist1")
        self.gridLayout_8.addWidget(self.labelJointControlWrist1, 12, 2, 1, 1)
        self.progressBarJointControlWrist3 = QtWidgets.QProgressBar(self.scrollAreaWidgetContents_4)
        self.progressBarJointControlWrist3.setMinimum(-360)
        self.progressBarJointControlWrist3.setMaximum(360)
        self.progressBarJointControlWrist3.setProperty("value", 0)
        self.progressBarJointControlWrist3.setObjectName("progressBarJointControlWrist3")
        self.gridLayout_8.addWidget(self.progressBarJointControlWrist3, 19, 2, 1, 1)
        self.labelJointControlWrist2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.labelJointControlWrist2.setObjectName("labelJointControlWrist2")
        self.gridLayout_8.addWidget(self.labelJointControlWrist2, 15, 2, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.JointControlDecBaseBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.JointControlDecBaseBt.setObjectName("JointControlDecBaseBt")
        self.horizontalLayout_3.addWidget(self.JointControlDecBaseBt)
        self.JointControlIncBaseBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.JointControlIncBaseBt.setObjectName("JointControlIncBaseBt")
        self.horizontalLayout_3.addWidget(self.JointControlIncBaseBt)
        self.gridLayout_8.addLayout(self.horizontalLayout_3, 4, 2, 1, 1)
        self.progressBarJointControlShoulder = QtWidgets.QProgressBar(self.scrollAreaWidgetContents_4)
        self.progressBarJointControlShoulder.setMinimum(-360)
        self.progressBarJointControlShoulder.setMaximum(360)
        self.progressBarJointControlShoulder.setProperty("value", 0)
        self.progressBarJointControlShoulder.setTextVisible(True)
        self.progressBarJointControlShoulder.setObjectName("progressBarJointControlShoulder")
        self.gridLayout_8.addWidget(self.progressBarJointControlShoulder, 7, 2, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.JointControlDecWrist2Bt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.JointControlDecWrist2Bt.setObjectName("JointControlDecWrist2Bt")
        self.horizontalLayout_7.addWidget(self.JointControlDecWrist2Bt)
        self.JointControlIncWrist2Bt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.JointControlIncWrist2Bt.setObjectName("JointControlIncWrist2Bt")
        self.horizontalLayout_7.addWidget(self.JointControlIncWrist2Bt)
        self.gridLayout_8.addLayout(self.horizontalLayout_7, 17, 2, 1, 1)
        self.progressBarJointControlWrist1 = QtWidgets.QProgressBar(self.scrollAreaWidgetContents_4)
        self.progressBarJointControlWrist1.setMinimum(-360)
        self.progressBarJointControlWrist1.setMaximum(360)
        self.progressBarJointControlWrist1.setProperty("value", 0)
        self.progressBarJointControlWrist1.setObjectName("progressBarJointControlWrist1")
        self.gridLayout_8.addWidget(self.progressBarJointControlWrist1, 13, 2, 1, 1)
        self.labelJointControlWrist3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.labelJointControlWrist3.setObjectName("labelJointControlWrist3")
        self.gridLayout_8.addWidget(self.labelJointControlWrist3, 18, 2, 1, 1)
        self.progressBarJointControlBase = QtWidgets.QProgressBar(self.scrollAreaWidgetContents_4)
        self.progressBarJointControlBase.setMinimum(-360)
        self.progressBarJointControlBase.setMaximum(360)
        self.progressBarJointControlBase.setProperty("value", 0)
        self.progressBarJointControlBase.setObjectName("progressBarJointControlBase")
        self.gridLayout_8.addWidget(self.progressBarJointControlBase, 3, 2, 1, 1)
        self.progressBarJointControlWrist2 = QtWidgets.QProgressBar(self.scrollAreaWidgetContents_4)
        self.progressBarJointControlWrist2.setMinimum(-360)
        self.progressBarJointControlWrist2.setMaximum(360)
        self.progressBarJointControlWrist2.setProperty("value", 0)
        self.progressBarJointControlWrist2.setObjectName("progressBarJointControlWrist2")
        self.gridLayout_8.addWidget(self.progressBarJointControlWrist2, 16, 2, 1, 1)
        self.labelJointControlElbow = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.labelJointControlElbow.setObjectName("labelJointControlElbow")
        self.gridLayout_8.addWidget(self.labelJointControlElbow, 9, 2, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.JointControlDecWrist3Bt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.JointControlDecWrist3Bt.setObjectName("JointControlDecWrist3Bt")
        self.horizontalLayout_8.addWidget(self.JointControlDecWrist3Bt)
        self.JointControlIncWrist3Bt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.JointControlIncWrist3Bt.setObjectName("JointControlIncWrist3Bt")
        self.horizontalLayout_8.addWidget(self.JointControlIncWrist3Bt)
        self.gridLayout_8.addLayout(self.horizontalLayout_8, 20, 2, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.JointControlDecElbowBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.JointControlDecElbowBt.setObjectName("JointControlDecElbowBt")
        self.horizontalLayout_5.addWidget(self.JointControlDecElbowBt)
        self.JointControlIncElbowBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.JointControlIncElbowBt.setObjectName("JointControlIncElbowBt")
        self.horizontalLayout_5.addWidget(self.JointControlIncElbowBt)
        self.gridLayout_8.addLayout(self.horizontalLayout_5, 11, 2, 1, 1)
        self.progressBarJointControlElbow = QtWidgets.QProgressBar(self.scrollAreaWidgetContents_4)
        self.progressBarJointControlElbow.setMinimum(-360)
        self.progressBarJointControlElbow.setMaximum(360)
        self.progressBarJointControlElbow.setProperty("value", 0)
        self.progressBarJointControlElbow.setObjectName("progressBarJointControlElbow")
        self.gridLayout_8.addWidget(self.progressBarJointControlElbow, 10, 2, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.JointControlDecShoulderBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.JointControlDecShoulderBt.setObjectName("JointControlDecShoulderBt")
        self.horizontalLayout_4.addWidget(self.JointControlDecShoulderBt)
        self.JointControlIncShoulderBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.JointControlIncShoulderBt.setObjectName("JointControlIncShoulderBt")
        self.horizontalLayout_4.addWidget(self.JointControlIncShoulderBt)
        self.gridLayout_8.addLayout(self.horizontalLayout_4, 8, 2, 1, 1)
        self.labelJointControlBase = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.labelJointControlBase.setObjectName("labelJointControlBase")
        self.gridLayout_8.addWidget(self.labelJointControlBase, 2, 2, 1, 1)
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.labelDescriptionJointControl = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.labelDescriptionJointControl.setObjectName("labelDescriptionJointControl")
        self.gridLayout_12.addWidget(self.labelDescriptionJointControl, 1, 0, 1, 1)
        self.ActualJointAnglesBt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.ActualJointAnglesBt.setObjectName("ActualJointAnglesBt")
        self.gridLayout_12.addWidget(self.ActualJointAnglesBt, 1, 1, 1, 1)
        self.doubleSpinBoxVariationAngle = QtWidgets.QDoubleSpinBox(self.scrollAreaWidgetContents_4)
        self.doubleSpinBoxVariationAngle.setObjectName("doubleSpinBoxVariationAngle")
        self.gridLayout_12.addWidget(self.doubleSpinBoxVariationAngle, 2, 1, 1, 1)
        self.labelChangeVariationValue = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.labelChangeVariationValue.setObjectName("labelChangeVariationValue")
        self.gridLayout_12.addWidget(self.labelChangeVariationValue, 2, 0, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_12, 1, 2, 1, 1)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.gridLayout_7.addWidget(self.scrollArea_4, 8, 1, 1, 1)
        self.tabWidgetControls.addTab(self.tabJointControl, "")

        #Cartesian Control tab of Remote Control tab of TabWindows of Main Command Window
        self.tabCartesianControl = QtWidgets.QWidget()
        self.tabCartesianControl.setObjectName("tabCartesianControl")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.tabCartesianControl)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.scrollArea_5 = QtWidgets.QScrollArea(self.tabCartesianControl)
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 918, 478))
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_5)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.comboBoxCartesianControlReference = QtWidgets.QComboBox(self.scrollAreaWidgetContents_5)
        self.comboBoxCartesianControlReference.setObjectName("comboBoxCartesianControlReference")
        self.comboBoxCartesianControlReference.addItem("")
        self.comboBoxCartesianControlReference.addItem("")
        self.verticalLayout_8.addWidget(self.comboBoxCartesianControlReference)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBoxPosition = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_5)
        self.groupBoxPosition.setObjectName("groupBoxPosition")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.groupBoxPosition)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.spinBoxVariationPosition = QtWidgets.QSpinBox(self.groupBoxPosition)
        self.spinBoxVariationPosition.setObjectName("spinBoxVariationPosition")
        self.verticalLayout_11.addWidget(self.spinBoxVariationPosition)
        self.label_ActualPosition = QtWidgets.QLabel(self.groupBoxPosition)
        self.label_ActualPosition.setObjectName("label_ActualPosition")
        self.verticalLayout_11.addWidget(self.label_ActualPosition)
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.CartesianControlIncYBt = QtWidgets.QPushButton(self.groupBoxPosition)
        self.CartesianControlIncYBt.setObjectName("CartesianControlIncYBt")
        self.gridLayout_9.addWidget(self.CartesianControlIncYBt, 1, 2, 1, 1)
        self.CartesianControlIncXBt = QtWidgets.QPushButton(self.groupBoxPosition)
        self.CartesianControlIncXBt.setObjectName("CartesianControlIncXBt")
        self.gridLayout_9.addWidget(self.CartesianControlIncXBt, 0, 1, 1, 1)
        self.CartesianControlDecXBt = QtWidgets.QPushButton(self.groupBoxPosition)
        self.CartesianControlDecXBt.setObjectName("CartesianControlDecXBt")
        self.gridLayout_9.addWidget(self.CartesianControlDecXBt, 2, 1, 1, 1)
        self.CartesianControlDecYBt = QtWidgets.QPushButton(self.groupBoxPosition)
        self.CartesianControlDecYBt.setObjectName("CartesianControlDecYBt")
        self.gridLayout_9.addWidget(self.CartesianControlDecYBt, 1, 0, 1, 1)
        self.verticalLayout_11.addLayout(self.gridLayout_9)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.CartesianControlIncZBt = QtWidgets.QPushButton(self.groupBoxPosition)
        self.CartesianControlIncZBt.setObjectName("CartesianControlIncZBt")
        self.verticalLayout_9.addWidget(self.CartesianControlIncZBt)
        self.CartesianControlDecZBt = QtWidgets.QPushButton(self.groupBoxPosition)
        self.CartesianControlDecZBt.setObjectName("CartesianControlDecZBt")
        self.verticalLayout_9.addWidget(self.CartesianControlDecZBt)
        self.verticalLayout_11.addLayout(self.verticalLayout_9)
        self.horizontalLayout.addWidget(self.groupBoxPosition)
        self.groupBoxOrientation = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_5)
        self.groupBoxOrientation.setObjectName("groupBoxOrientation")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.groupBoxOrientation)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.doubleSpinBoxVariationOrientation = QtWidgets.QDoubleSpinBox(self.groupBoxOrientation)
        self.doubleSpinBoxVariationOrientation.setObjectName("doubleSpinBoxVariationOrientation")
        self.verticalLayout_12.addWidget(self.doubleSpinBoxVariationOrientation)
        self.label_ActualOrientation = QtWidgets.QLabel(self.groupBoxOrientation)
        self.label_ActualOrientation.setObjectName("label_ActualOrientation")
        self.verticalLayout_12.addWidget(self.label_ActualOrientation)
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.CartesianControlIncRxBt = QtWidgets.QPushButton(self.groupBoxOrientation)
        self.CartesianControlIncRxBt.setObjectName("CartesianControlIncRxBt")
        self.gridLayout_10.addWidget(self.CartesianControlIncRxBt, 0, 1, 1, 1)
        self.CartesianControlIncRyBt = QtWidgets.QPushButton(self.groupBoxOrientation)
        self.CartesianControlIncRyBt.setObjectName("CartesianControlIncRyBt")
        self.gridLayout_10.addWidget(self.CartesianControlIncRyBt, 1, 2, 1, 1)
        self.CartesianControlDecRyBt = QtWidgets.QPushButton(self.groupBoxOrientation)
        self.CartesianControlDecRyBt.setObjectName("CartesianControlDecRyBt")
        self.gridLayout_10.addWidget(self.CartesianControlDecRyBt, 1, 0, 1, 1)
        self.CartesianControlDecRxBt = QtWidgets.QPushButton(self.groupBoxOrientation)
        self.CartesianControlDecRxBt.setObjectName("CartesianControlDecRxBt")
        self.gridLayout_10.addWidget(self.CartesianControlDecRxBt, 2, 1, 1, 1)
        self.verticalLayout_12.addLayout(self.gridLayout_10)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.CartesianControlIncRzBt = QtWidgets.QPushButton(self.groupBoxOrientation)
        self.CartesianControlIncRzBt.setObjectName("CartesianControlIncRzBt")
        self.verticalLayout_10.addWidget(self.CartesianControlIncRzBt)
        self.CartesianControlDecRzBt = QtWidgets.QPushButton(self.groupBoxOrientation)
        self.CartesianControlDecRzBt.setObjectName("CartesianControlDecRzBt")
        self.verticalLayout_10.addWidget(self.CartesianControlDecRzBt)
        self.verticalLayout_12.addLayout(self.verticalLayout_10)
        self.horizontalLayout.addWidget(self.groupBoxOrientation)
        self.verticalLayout_8.addLayout(self.horizontalLayout)
        spacerItem25 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem25)
        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)
        self.verticalLayout_13.addWidget(self.scrollArea_5)
        self.tabWidgetControls.addTab(self.tabCartesianControl, "")
        self.tabMoveToPosition = QtWidgets.QWidget()

        #Move to position tab of Remote Control tab of TabWindows of Main Command Window
        self.tabMoveToPosition.setObjectName("tabMoveToPosition")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.tabMoveToPosition)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.scrollArea_6 = QtWidgets.QScrollArea(self.tabMoveToPosition)
        self.scrollArea_6.setWidgetResizable(True)
        self.scrollArea_6.setObjectName("scrollArea_6")
        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 682, 390))
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_6)
        self.verticalLayout_16.setObjectName("verticalLayout_16")

        #Tabs of Move to position tab of Remote Control tab of TabWindows of Main Command Window
        self.tabWidgetPositions = QtWidgets.QTabWidget(self.scrollAreaWidgetContents_6)
        self.tabWidgetPositions.setTabBarAutoHide(False)
        self.tabWidgetPositions.setObjectName("tabWidgetPositions")
        self.tabCartesianPosition = QtWidgets.QWidget()

        #Cartesian tab of Tabs of Move to position tab of Remote Control tab of TabWindows of Main Command Window
        self.tabCartesianPosition.setObjectName("tabCartesianPosition")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.tabCartesianPosition)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_XPosition = QtWidgets.QLabel(self.tabCartesianPosition)
        self.label_XPosition.setObjectName("label_XPosition")
        self.verticalLayout_15.addWidget(self.label_XPosition)
        self.lineEditXPosition = QtWidgets.QLineEdit(self.tabCartesianPosition)
        self.lineEditXPosition.setObjectName("lineEditXPosition")
        self.verticalLayout_15.addWidget(self.lineEditXPosition)
        self.label_YPosition = QtWidgets.QLabel(self.tabCartesianPosition)
        self.label_YPosition.setObjectName("label_YPosition")
        self.verticalLayout_15.addWidget(self.label_YPosition)
        self.lineEditYPosition = QtWidgets.QLineEdit(self.tabCartesianPosition)
        self.lineEditYPosition.setObjectName("lineEditYPosition")
        self.verticalLayout_15.addWidget(self.lineEditYPosition)
        self.label_ZPosition = QtWidgets.QLabel(self.tabCartesianPosition)
        self.label_ZPosition.setObjectName("label_ZPosition")
        self.verticalLayout_15.addWidget(self.label_ZPosition)
        self.lineEditZPosition = QtWidgets.QLineEdit(self.tabCartesianPosition)
        self.lineEditZPosition.setObjectName("lineEditZPosition")
        self.verticalLayout_15.addWidget(self.lineEditZPosition)
        self.label_RxPosition = QtWidgets.QLabel(self.tabCartesianPosition)
        self.label_RxPosition.setObjectName("label_RxPosition")
        self.verticalLayout_15.addWidget(self.label_RxPosition)
        self.lineEditRxPosition = QtWidgets.QLineEdit(self.tabCartesianPosition)
        self.lineEditRxPosition.setObjectName("lineEditRxPosition")
        self.verticalLayout_15.addWidget(self.lineEditRxPosition)
        self.label_RyPosition = QtWidgets.QLabel(self.tabCartesianPosition)
        self.label_RyPosition.setObjectName("label_RyPosition")
        self.verticalLayout_15.addWidget(self.label_RyPosition)
        self.lineEditRyPosition = QtWidgets.QLineEdit(self.tabCartesianPosition)
        self.lineEditRyPosition.setObjectName("lineEditRyPosition")
        self.verticalLayout_15.addWidget(self.lineEditRyPosition)
        self.label_RzPosition = QtWidgets.QLabel(self.tabCartesianPosition)
        self.label_RzPosition.setObjectName("label_RzPosition")
        self.verticalLayout_15.addWidget(self.label_RzPosition)
        self.lineEditRzPosition = QtWidgets.QLineEdit(self.tabCartesianPosition)
        self.lineEditRzPosition.setObjectName("lineEditRzPosition")
        self.verticalLayout_15.addWidget(self.lineEditRzPosition)
        self.SendCartesianPositionBt = QtWidgets.QPushButton(self.tabCartesianPosition)
        self.SendCartesianPositionBt.setObjectName("SendCartesianPositionBt")
        self.verticalLayout_15.addWidget(self.SendCartesianPositionBt)
        self.tabWidgetPositions.addTab(self.tabCartesianPosition, "")

        #Joint tab of Tabs of Move to position tab of Remote Control tab of TabWindows of Main Command Window
        self.tabJointPoisition = QtWidgets.QWidget()
        self.tabJointPoisition.setObjectName("tabJointPoisition")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.tabJointPoisition)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.label_BaseJoint = QtWidgets.QLabel(self.tabJointPoisition)
        self.label_BaseJoint.setObjectName("label_BaseJoint")
        self.verticalLayout_17.addWidget(self.label_BaseJoint)
        self.lineEdit_BaseJoint = QtWidgets.QLineEdit(self.tabJointPoisition)
        self.lineEdit_BaseJoint.setObjectName("lineEdit_BaseJoint")
        self.verticalLayout_17.addWidget(self.lineEdit_BaseJoint)
        self.label_ShoulderJoint = QtWidgets.QLabel(self.tabJointPoisition)
        self.label_ShoulderJoint.setObjectName("label_ShoulderJoint")
        self.verticalLayout_17.addWidget(self.label_ShoulderJoint)
        self.lineEdit_ShoulderJoint = QtWidgets.QLineEdit(self.tabJointPoisition)
        self.lineEdit_ShoulderJoint.setObjectName("lineEdit_ShoulderJoint")
        self.verticalLayout_17.addWidget(self.lineEdit_ShoulderJoint)
        self.label_ElbowJoint = QtWidgets.QLabel(self.tabJointPoisition)
        self.label_ElbowJoint.setObjectName("label_ElbowJoint")
        self.verticalLayout_17.addWidget(self.label_ElbowJoint)
        self.lineEdit_ElbowJoint = QtWidgets.QLineEdit(self.tabJointPoisition)
        self.lineEdit_ElbowJoint.setObjectName("lineEdit_ElbowJoint")
        self.verticalLayout_17.addWidget(self.lineEdit_ElbowJoint)
        self.label_Wrist1Joint = QtWidgets.QLabel(self.tabJointPoisition)
        self.label_Wrist1Joint.setObjectName("label_Wrist1Joint")
        self.verticalLayout_17.addWidget(self.label_Wrist1Joint)
        self.lineEdit_WristJoint1 = QtWidgets.QLineEdit(self.tabJointPoisition)
        self.lineEdit_WristJoint1.setObjectName("lineEdit_WristJoint1")
        self.verticalLayout_17.addWidget(self.lineEdit_WristJoint1)
        self.label_Wrist2Joint = QtWidgets.QLabel(self.tabJointPoisition)
        self.label_Wrist2Joint.setObjectName("label_Wrist2Joint")
        self.verticalLayout_17.addWidget(self.label_Wrist2Joint)
        self.lineEdit_Wrist2Joint = QtWidgets.QLineEdit(self.tabJointPoisition)
        self.lineEdit_Wrist2Joint.setObjectName("lineEdit_Wrist2Joint")
        self.verticalLayout_17.addWidget(self.lineEdit_Wrist2Joint)
        self.label_Wrist3Joint = QtWidgets.QLabel(self.tabJointPoisition)
        self.label_Wrist3Joint.setObjectName("label_Wrist3Joint")
        self.verticalLayout_17.addWidget(self.label_Wrist3Joint)
        self.lineEdit_Wrist3Joint = QtWidgets.QLineEdit(self.tabJointPoisition)
        self.lineEdit_Wrist3Joint.setObjectName("lineEdit_Wrist3Joint")
        self.verticalLayout_17.addWidget(self.lineEdit_Wrist3Joint)
        self.SendJointPositionBt = QtWidgets.QPushButton(self.tabJointPoisition)
        self.SendJointPositionBt.setObjectName("SendJointPositionBt")
        self.verticalLayout_17.addWidget(self.SendJointPositionBt)
        self.tabWidgetPositions.addTab(self.tabJointPoisition, "")
        self.verticalLayout_16.addWidget(self.tabWidgetPositions)
        self.scrollArea_6.setWidget(self.scrollAreaWidgetContents_6)
        self.verticalLayout_14.addWidget(self.scrollArea_6)
        self.tabWidgetControls.addTab(self.tabMoveToPosition, "")
        self.verticalLayout_7.addWidget(self.tabWidgetControls)
        self.tabWidget.addTab(self.tabRemoteControl, "")

        #Select Robot tab of TabWindows of Main Command Window
        self.tabSelectRobot = QtWidgets.QWidget()
        self.tabSelectRobot.setObjectName("tabSelectRobot")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tabSelectRobot)
        self.gridLayout_6.setObjectName("gridLayout_6")
        spacerItem26 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem26, 1, 4, 1, 1)
        self.comboBoxRobotSelection = QtWidgets.QComboBox(self.tabSelectRobot)
        self.comboBoxRobotSelection.setMinimumSize(QtCore.QSize(260, 0))
        self.comboBoxRobotSelection.setObjectName("comboBoxRobotSelection")
        self.gridLayout_6.addWidget(self.comboBoxRobotSelection, 1, 1, 1, 1)
        spacerItem27 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem27, 1, 2, 1, 1)
        spacerItem28 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem28, 1, 0, 1, 1)
        self.labelSerialNumber = QtWidgets.QLabel(self.tabSelectRobot)
        self.labelSerialNumber.setObjectName("labelSerialNumber")
        self.gridLayout_6.addWidget(self.labelSerialNumber, 2, 1, 1, 1)
        self.labelRobotType = QtWidgets.QLabel(self.tabSelectRobot)
        self.labelRobotType.setObjectName("labelRobotType")
        self.gridLayout_6.addWidget(self.labelRobotType, 2, 3, 1, 1)
        spacerItem29 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem29, 6, 1, 1, 1)
        spacerItem30 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem30, 0, 1, 1, 1)
        self.AddNewRobotBt = QtWidgets.QPushButton(self.tabSelectRobot)
        self.AddNewRobotBt.setMinimumSize(QtCore.QSize(1, 0))
        self.AddNewRobotBt.setObjectName("AddNewRobotBt")
        self.gridLayout_6.addWidget(self.AddNewRobotBt, 4, 3, 1, 1)
        self.RobotSelectionBt = QtWidgets.QPushButton(self.tabSelectRobot)
        self.RobotSelectionBt.setMinimumSize(QtCore.QSize(179, 0))
        self.RobotSelectionBt.setObjectName("RobotSelectionBt")
        self.gridLayout_6.addWidget(self.RobotSelectionBt, 1, 3, 1, 1)
        spacerItem31 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem31, 3, 3, 1, 1)
        self.tabWidget.addTab(self.tabSelectRobot, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.stackedWidget.addWidget(self.pageMainCommands)
        self.page_RobotResponse = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.page_RobotResponse.setFont(font)
        self.page_RobotResponse.setStyleSheet("font: 16pt \"Sans Serif\";")

        #Robot Response window page
        self.page_RobotResponse.setObjectName("page_RobotResponse")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.page_RobotResponse)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.labelRobotResponse = QtWidgets.QLabel(self.page_RobotResponse)
        self.labelRobotResponse.setAlignment(QtCore.Qt.AlignCenter)
        self.labelRobotResponse.setObjectName("labelRobotResponse")
        self.verticalLayout_18.addWidget(self.labelRobotResponse)
        self.labelRobotResponseValue = QtWidgets.QLabel(self.page_RobotResponse)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.labelRobotResponseValue.setFont(font)
        self.labelRobotResponseValue.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.labelRobotResponseValue.setAlignment(QtCore.Qt.AlignCenter)
        self.labelRobotResponseValue.setObjectName("labelRobotResponseValue")
        self.verticalLayout_18.addWidget(self.labelRobotResponseValue)
        self.RobotResponseBack = QtWidgets.QPushButton(self.page_RobotResponse)
        self.RobotResponseBack.setObjectName("RobotResponseBack")
        self.verticalLayout_18.addWidget(self.RobotResponseBack)
        self.stackedWidget.addWidget(self.page_RobotResponse)

        #Robot Command to send window page
        self.pageWriteCommandToSend = QtWidgets.QWidget()
        self.pageWriteCommandToSend.setStyleSheet("font: 16pt \"Sans Serif\";")
        self.pageWriteCommandToSend.setObjectName("pageWriteCommandToSend")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.pageWriteCommandToSend)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        spacerItem32 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_19.addItem(spacerItem32)
        self.labelWriteCommandToSend = QtWidgets.QLabel(self.pageWriteCommandToSend)
        self.labelWriteCommandToSend.setAlignment(QtCore.Qt.AlignCenter)
        self.labelWriteCommandToSend.setObjectName("labelWriteCommandToSend")
        self.verticalLayout_19.addWidget(self.labelWriteCommandToSend)
        self.lineEditCommandSend = QtWidgets.QLineEdit(self.pageWriteCommandToSend)
        self.lineEditCommandSend.setMinimumSize(QtCore.QSize(500, 0))
        self.lineEditCommandSend.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.lineEditCommandSend.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditCommandSend.setObjectName("lineEditCommandSend")
        self.verticalLayout_19.addWidget(self.lineEditCommandSend, 0, QtCore.Qt.AlignHCenter)
        spacerItem33 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_19.addItem(spacerItem33)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.CommandSendBackBt = QtWidgets.QPushButton(self.pageWriteCommandToSend)
        self.CommandSendBackBt.setMaximumSize(QtCore.QSize(400, 16777215))
        self.CommandSendBackBt.setObjectName("CommandSendBackBt")
        self.horizontalLayout_9.addWidget(self.CommandSendBackBt)
        self.CommandSendSendBt = QtWidgets.QPushButton(self.pageWriteCommandToSend)
        self.CommandSendSendBt.setMaximumSize(QtCore.QSize(400, 16777215))
        self.CommandSendSendBt.setObjectName("CommandSendSendBt")
        self.horizontalLayout_9.addWidget(self.CommandSendSendBt)
        self.verticalLayout_19.addLayout(self.horizontalLayout_9)
        spacerItem34 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_19.addItem(spacerItem34)
        self.stackedWidget.addWidget(self.pageWriteCommandToSend)
        self.gridLayout.addWidget(self.stackedWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 774, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidgetControls.setCurrentIndex(2)
        self.tabWidgetPositions.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TitleNewRobot.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt;\">Assign a new Robot to Teleoperate</span></p></body></html>"))
        self.MessageRobotIP.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt;\">Insert the IP of the robot you want to teleoperate</span></p></body></html>"))
        self.ConnectRobotBt.setText(_translate("MainWindow", " Connect to Robot"))
        self.InsertIPField.setPlaceholderText(_translate("MainWindow", "Insert the robot IP"))
        self.StopRobotBt.setText(_translate("MainWindow", "Stop Robot"))
        self.StopRobotBt.setShortcut(_translate("MainWindow", "Alt+P"))
        self.ReleaseBreakesDashBt.setText(_translate("MainWindow", "Release breaks"))
        self.ClosePopUpDashBt.setText(_translate("MainWindow", "Close pop up message"))
        self.PowerOffDashBt.setText(_translate("MainWindow", "Power off"))
        self.PauseProgramDashBt.setText(_translate("MainWindow", "Pause program"))
        self.PowerOnDashBt.setText(_translate("MainWindow", "Power on "))
        self.RunProgramDashBt.setText(_translate("MainWindow", "Run program"))
        self.LoadInstallationDashBt.setText(_translate("MainWindow", "Load instalation"))
        self.ActualRobotModeBt.setText(_translate("MainWindow", "Get actual robot Mode"))
        self.CloseSafetyPopUPDashBt.setText(_translate("MainWindow", "Close safety pop up"))
        self.OpenPopUpDashBt.setText(_translate("MainWindow", "Open pop up message"))
        self.WriteLogDashBt.setText(_translate("MainWindow", "Write message to log"))
        self.ChangeOperationalModeDashBt.setText(_translate("MainWindow", "Change operational mode"))
        self.ActualProgramDashBt.setText(_translate("MainWindow", "Get actual program"))
        self.UnlockProtectiveStopDashBt.setText(_translate("MainWindow", "Unlock protective stop"))
        self.LoadProgramDashBt.setText(_translate("MainWindow", "Load program"))
        self.ActualSafetyModeDashBt.setText(_translate("MainWindow", "Get actual safety mode"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DashBoardtab), _translate("MainWindow", "DashBoard Functions"))
        self.FreeDriveTCPBt.setText(_translate("MainWindow", "Freedrive mode"))
        self.ExecuteScriptTCPBt.setText(_translate("MainWindow", "Execute sricpt"))
        self.ComandTCPText.setPlainText(_translate("MainWindow", "def program:\n"
"    #Insert here the         \n"
"    #command         \n"
"    #you want to send\n"
"end\n"
""))
        self.SendScriptTCPBt.setText(_translate("MainWindow", "Send script command"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTCPIP), _translate("MainWindow", "TCP/IP Script Functions"))
        __sortingEnabled = self.listWidgetRegisterNumber.isSortingEnabled()
        self.listWidgetRegisterNumber.setSortingEnabled(False)
        item = self.listWidgetRegisterNumber.item(0)
        item.setText(_translate("MainWindow", "Register 0"))
        item = self.listWidgetRegisterNumber.item(1)
        item.setText(_translate("MainWindow", "Register 1"))
        item = self.listWidgetRegisterNumber.item(2)
        item.setText(_translate("MainWindow", "Register 2"))
        self.listWidgetRegisterNumber.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.listWidgetRegisterDescription.isSortingEnabled()
        self.listWidgetRegisterDescription.setSortingEnabled(False)
        item = self.listWidgetRegisterDescription.item(0)
        item.setText(_translate("MainWindow", "Description 0 :  inputs signals"))
        item = self.listWidgetRegisterDescription.item(1)
        item.setText(_translate("MainWindow", "Description 1: output signals"))
        item = self.listWidgetRegisterDescription.item(2)
        item.setText(_translate("MainWindow", "Description 2 : something"))
        self.listWidgetRegisterDescription.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.listWidgetRegisterValue.isSortingEnabled()
        self.listWidgetRegisterValue.setSortingEnabled(False)
        item = self.listWidgetRegisterValue.item(0)
        item.setText(_translate("MainWindow", "Value 0 : 123184"))
        item = self.listWidgetRegisterValue.item(1)
        item.setText(_translate("MainWindow", "Value 1 : 46464684"))
        item = self.listWidgetRegisterValue.item(2)
        item.setText(_translate("MainWindow", "Value 2 : 6464646"))
        self.listWidgetRegisterValue.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabModBus), _translate("MainWindow", "ModBus Data"))
        self.JointControlDecWrist1Bt.setText(_translate("MainWindow", "-"))
        self.JointControlIncWrist1Bt.setText(_translate("MainWindow", "+"))
        self.labelJointControlShoulder.setText(_translate("MainWindow", "Shoulder joint"))
        self.labelJointControlWrist1.setText(_translate("MainWindow", "Wrist 1 joint"))
        self.progressBarJointControlWrist3.setFormat(_translate("MainWindow", "Angle %v"))
        self.labelJointControlWrist2.setText(_translate("MainWindow", "Wrist 2 joint"))
        self.JointControlDecBaseBt.setText(_translate("MainWindow", "-"))
        self.JointControlIncBaseBt.setText(_translate("MainWindow", "+"))
        self.progressBarJointControlShoulder.setFormat(_translate("MainWindow", "Angle %v"))
        self.JointControlDecWrist2Bt.setText(_translate("MainWindow", "-"))
        self.JointControlIncWrist2Bt.setText(_translate("MainWindow", "+"))
        self.progressBarJointControlWrist1.setFormat(_translate("MainWindow", "Angle %v"))
        self.labelJointControlWrist3.setText(_translate("MainWindow", "Wrist 3 joint"))
        self.progressBarJointControlBase.setFormat(_translate("MainWindow", "Angle %v"))
        self.progressBarJointControlWrist2.setFormat(_translate("MainWindow", "Angle %v"))
        self.labelJointControlElbow.setText(_translate("MainWindow", "Elbow joint"))
        self.JointControlDecWrist3Bt.setText(_translate("MainWindow", "-"))
        self.JointControlIncWrist3Bt.setText(_translate("MainWindow", "+"))
        self.JointControlDecElbowBt.setText(_translate("MainWindow", "-"))
        self.JointControlIncElbowBt.setText(_translate("MainWindow", "+"))
        self.progressBarJointControlElbow.setFormat(_translate("MainWindow", "Angle %v"))
        self.JointControlDecShoulderBt.setText(_translate("MainWindow", "-"))
        self.JointControlIncShoulderBt.setText(_translate("MainWindow", "+"))
        self.labelJointControlBase.setText(_translate("MainWindow", "Base joint"))
        self.labelDescriptionJointControl.setText(_translate("MainWindow", "Click on the button to show the actual robot position."))
        self.ActualJointAnglesBt.setText(_translate("MainWindow", "Get actual joint angles"))
        self.labelChangeVariationValue.setText(_translate("MainWindow", "Change variation value"))
        self.tabWidgetControls.setTabText(self.tabWidgetControls.indexOf(self.tabJointControl), _translate("MainWindow", "Joint control"))
        self.comboBoxCartesianControlReference.setItemText(0, _translate("MainWindow", "Base reference"))
        self.comboBoxCartesianControlReference.setItemText(1, _translate("MainWindow", "Tool reference"))
        self.groupBoxPosition.setTitle(_translate("MainWindow", "Position"))
        self.label_ActualPosition.setText(_translate("MainWindow", "x: 0mm | y: 0mm | z: 0 mm "))
        self.CartesianControlIncYBt.setText(_translate("MainWindow", "y+"))
        self.CartesianControlIncYBt.setShortcut(_translate("MainWindow", "Shift+D"))
        self.CartesianControlIncXBt.setText(_translate("MainWindow", "x+"))
        self.CartesianControlIncXBt.setShortcut(_translate("MainWindow", "Shift+W"))
        self.CartesianControlDecXBt.setText(_translate("MainWindow", "x-"))
        self.CartesianControlDecXBt.setShortcut(_translate("MainWindow", "Shift+S"))
        self.CartesianControlDecYBt.setText(_translate("MainWindow", "y-"))
        self.CartesianControlDecYBt.setShortcut(_translate("MainWindow", "Shift+A"))
        self.CartesianControlIncZBt.setText(_translate("MainWindow", "z+"))
        self.CartesianControlIncZBt.setShortcut(_translate("MainWindow", "Shift+E"))
        self.CartesianControlDecZBt.setText(_translate("MainWindow", "z-"))
        self.CartesianControlDecZBt.setShortcut(_translate("MainWindow", "Shift+Q"))
        self.groupBoxOrientation.setTitle(_translate("MainWindow", "Orientation"))
        self.label_ActualOrientation.setText(_translate("MainWindow", "rx: 0º | ry: 0º | rz: 0º"))
        self.CartesianControlIncRxBt.setText(_translate("MainWindow", "rx+"))
        self.CartesianControlIncRxBt.setShortcut(_translate("MainWindow", "Alt+W"))
        self.CartesianControlIncRyBt.setText(_translate("MainWindow", "ry+"))
        self.CartesianControlIncRyBt.setShortcut(_translate("MainWindow", "Alt+D"))
        self.CartesianControlDecRyBt.setText(_translate("MainWindow", "ry-"))
        self.CartesianControlDecRyBt.setShortcut(_translate("MainWindow", "Alt+A"))
        self.CartesianControlDecRxBt.setText(_translate("MainWindow", "rx-"))
        self.CartesianControlDecRxBt.setShortcut(_translate("MainWindow", "Alt+S"))
        self.CartesianControlIncRzBt.setText(_translate("MainWindow", "rz+"))
        self.CartesianControlIncRzBt.setShortcut(_translate("MainWindow", "Alt+E"))
        self.CartesianControlDecRzBt.setText(_translate("MainWindow", "rz-"))
        self.CartesianControlDecRzBt.setShortcut(_translate("MainWindow", "Alt+Q"))
        self.tabWidgetControls.setTabText(self.tabWidgetControls.indexOf(self.tabCartesianControl), _translate("MainWindow", "Cartesian control"))
        self.label_XPosition.setText(_translate("MainWindow", "X position mm"))
        self.label_YPosition.setText(_translate("MainWindow", "Y position mm"))
        self.label_ZPosition.setText(_translate("MainWindow", "Z position mm"))
        self.label_RxPosition.setText(_translate("MainWindow", "Rx orientation º"))
        self.label_RyPosition.setText(_translate("MainWindow", "Ry orientation º"))
        self.label_RzPosition.setText(_translate("MainWindow", "Rz orientation º"))
        self.SendCartesianPositionBt.setText(_translate("MainWindow", "Send position"))
        self.tabWidgetPositions.setTabText(self.tabWidgetPositions.indexOf(self.tabCartesianPosition), _translate("MainWindow", "Cartesian position"))
        self.label_BaseJoint.setText(_translate("MainWindow", "Base joint º"))
        self.label_ShoulderJoint.setText(_translate("MainWindow", "Shoulder joint º"))
        self.label_ElbowJoint.setText(_translate("MainWindow", "Elbow joint º"))
        self.label_Wrist1Joint.setText(_translate("MainWindow", "Wrist 1 joint º"))
        self.label_Wrist2Joint.setText(_translate("MainWindow", "Wrist 2 joint º"))
        self.label_Wrist3Joint.setText(_translate("MainWindow", "Wrist 3 joint º"))
        self.SendJointPositionBt.setText(_translate("MainWindow", "Send position"))
        self.tabWidgetPositions.setTabText(self.tabWidgetPositions.indexOf(self.tabJointPoisition), _translate("MainWindow", "Joint positions"))
        self.tabWidgetControls.setTabText(self.tabWidgetControls.indexOf(self.tabMoveToPosition), _translate("MainWindow", "Move to position"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRemoteControl), _translate("MainWindow", "Remote Control"))
        self.labelSerialNumber.setText(_translate("MainWindow", "Serial Number:"))
        self.labelRobotType.setText(_translate("MainWindow", "Robot Type:"))
        self.AddNewRobotBt.setText(_translate("MainWindow", "Add a new Robot"))
        self.RobotSelectionBt.setText(_translate("MainWindow", "Select Robot"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSelectRobot), _translate("MainWindow", "Select robot"))
        self.labelRobotResponse.setText(_translate("MainWindow", "Robot Response"))
        self.labelRobotResponseValue.setText(_translate("MainWindow", "Response"))
        self.RobotResponseBack.setText(_translate("MainWindow", "Back"))
        self.labelWriteCommandToSend.setText(_translate("MainWindow", "Write command to send"))
        self.CommandSendBackBt.setText(_translate("MainWindow", "Back"))
        self.CommandSendSendBt.setText(_translate("MainWindow", "Send"))

    def CreateConnections(self):

        self.ConnectRobotBt.clicked.connect(self.ConnectRobotBtAction)

        self.StopRobotBt.clicked.connect(self.StopRobotBtAction)

        self.PowerOnDashBt.clicked.connect(self.PowerOnDashBtAction)
        self.PowerOffDashBt.clicked.connect(self.PowerOffDashBtAction)
        self.ReleaseBreakesDashBt.clicked.connect(self.ReleaseBreakesDashBtAction)
        self.ActualProgramDashBt.clicked.connect(self.ActualProgramDashBtAction)
        self.LoadInstallationDashBt.clicked.connect(self.LoadInstallationDashBtAction)
        self.LoadProgramDashBt.clicked.connect(self.LoadProgramDashBtAction)
        self.RunProgramDashBt.clicked.connect(self.RunProgramDashBtAction)
        self.PauseProgramDashBt.clicked.connect(self.PauseProgramDashBtAction)
        self.OpenPopUpDashBt.clicked.connect(self.OpenPopUpDashBtAction)
        self.ClosePopUpDashBt.clicked.connect(self.ClosePopUpDashBtAction)
        self.WriteLogDashBt.clicked.connect(self.WriteLogDashBtAction)
        self.ActualRobotModeBt.clicked.connect(self.ActualRobotModeBtAction)
        self.ChangeOperationalModeDashBt.clicked.connect(self.ChangeOperationalModeDashBtAction)
        self.CloseSafetyPopUPDashBt.clicked.connect(self.CloseSafetyPopUPDashBtAction)
        self.ActualSafetyModeDashBt.clicked.connect(self.ActualSafetyModeDashBtAction)
        self.UnlockProtectiveStopDashBt.clicked.connect(self.UnlockProtectiveStopDashBtAction)

        self.FreeDriveTCPBt.clicked.connect(self.FreeDriveTCPBtAction)
        self.ExecuteScriptTCPBt.clicked.connect(self.ExecuteScriptTCPBtAction)
        self.SendScriptTCPBt.clicked.connect(self.SendScriptTCPBtAction)

        self.vsRN.valueChanged.connect(self.move_scrollbar)

        self.listWidgetRegisterValue.itemClicked.connect(self.listWidgetRegisterValueAction)
        self.listWidgetRegisterDescription.itemClicked.connect(self.listWidgetRegisterDescriptionAction)
        self.listWidgetRegisterValue.itemClicked.connect(self.listWidgetRegisterValueAction)

        self.ActualJointAnglesBt.clicked.connect(self.ActualJointAnglesBtAction)
        self.JointControlIncBaseBt.clicked.connect(self.JointControlIncBaseBtAction)
        self.JointControlDecBaseBt.clicked.connect(self.JointControlDecBaseBtAction)
        self.JointControlIncShoulderBt.clicked.connect(self.JointControlIncShoulderBtAction)
        self.JointControlDecShoulderBt.clicked.connect(self.JointControlDecShoulderBtAction)
        self.JointControlIncElbowBt.clicked.connect(self.JointControlIncElbowBtAction)
        self.JointControlDecElbowBt.clicked.connect(self.JointControlDecElbowBtAction)
        self.JointControlIncWrist1Bt.clicked.connect(self.JointControlIncWrist1BtAction)
        self.JointControlDecWrist1Bt.clicked.connect(self.JointControlDecWrist1BtAction)
        self.JointControlIncWrist2Bt.clicked.connect(self.JointControlIncWrist2BtAction)
        self.JointControlDecWrist2Bt.clicked.connect(self.JointControlDecWrist2BtAction)
        self.JointControlIncWrist3Bt.clicked.connect(self.JointControlIncWrist3BtAction)
        self.JointControlDecWrist3Bt.clicked.connect(self.JointControlDecWrist3BtAction)

        self.CartesianControlIncXBt.clicked.connect(self.CartesianControlIncXBtAction)
        self.CartesianControlDecXBt.clicked.connect(self.CartesianControlDecXBtAction)
        self.CartesianControlIncYBt.clicked.connect(self.CartesianControlIncYBtAction)
        self.CartesianControlDecYBt.clicked.connect(self.CartesianControlDecYBtAction)
        self.CartesianControlIncZBt.clicked.connect(self.CartesianControlIncZBtAction)
        self.CartesianControlDecZBt.clicked.connect(self.CartesianControlDecZBtAction)
        self.CartesianControlIncRxBt.clicked.connect(self.CartesianControlIncRxBtAction)
        self.CartesianControlDecRxBt.clicked.connect(self.CartesianControlDecRxBtAction)
        self.CartesianControlIncRyBt.clicked.connect(self.CartesianControlIncRyBtAction)
        self.CartesianControlDecRyBt.clicked.connect(self.CartesianControlDecRyBtAction)
        self.CartesianControlIncRzBt.clicked.connect(self.CartesianControlIncRzBtAction)
        self.CartesianControlDecRzBt.clicked.connect(self.CartesianControlDecRzBtAction)

        self.SendCartesianPositionBt.clicked.connect(self.SendCartesianPositionBtAction)
        self.SendJointPositionBt.clicked.connect(self.SendJointPositionBtAction)

        self.RobotSelectionBt.clicked.connect(self.RobotSelectionBtAction)
        self.AddNewRobotBt.clicked.connect(self.AddNewRobotBtAction)

        self.RobotResponseBack.clicked.connect(self.RobotResponseBackAction)
        self.CommandSendBackBt.clicked.connect(self.CommandSendBackBtAction)
        self.CommandSendSendBt.clicked.connect(self.CommandSendSendBtAction)


    #Create new robot actions
    def ConnectRobotBtAction(self):
        print("connect pressed")
        value_ip = self.InsertIPField.text()
        print(value_ip)
        if(value_ip.count(".") != 3):
            msg = QMessageBox()
            msg.setWindowTitle("Wrong IP dirrection introduced")
            msg.setText("Check the IP introduced, it doesn't have 3 \".\" ")
            retval = msg.exec_()
        else:
            #Check the connection
            robot = UR_Communication(value_ip)
            if( (robot.DashBoard_Connected == False) or (robot.URScript_Connected == False) or (robot.Modbus_Connected == False) ):
                if ( (robot.DashBoard_Connected == False) and (robot.URScript_Connected == False) and (robot.Modbus_Connected == False) ):
                    msg = QMessageBox()
                    msg.setWindowTitle("Connection with the robot failed")
                    msg.setText("DashBoard, URScript TCP/IP and Modbus connection failed, check that the IP it's right and you are in the same network")
                    retval = msg.exec_()

                    creation = False if (self.RobotConnectionRequired == True) else True

                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Connection with the robot failed")
                    msg.setText("""There is some connection which failed, if even though you want to continue click on Ok
                    Dashboard connection = """+str(robot.DashBoard_Connected))+"""
                    URscript connection = """+str(robot.URScript_Connected)+"""
                    ModBus connection = """+str(robot.Modbus_Connected)

                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    retval = msg.exec_()
                    if(retval == QMessageBox.Ok):
                        creation = True
                    else:
                        creation = False
            else:
                #Everything connected well
                creation = True

            if(creation):
                #Delete message for the following creation
                self.InsertIPField.setText("")

                #Check if ip is already on the list

                if(value_ip in self.Robots_ip):
                    add_Robot = False
                else:
                    add_Robot = True

                if(add_Robot == True):

                    #add it to the list of robots
                    self.Robots.append(robot)
                    self.Robots_ip.append(value_ip)
                    if(robot.DashBoard_Connected==True):
                        aux = robot.DashBoard_GetData() # to clean the buffer
                        robot.DashBoard_SerialNumber()
                        self.Robots_serial.append(robot.DashBoard_GetData().decode())
                        robot.DashBoard_Model()
                        self.Robots_type.append(robot.DashBoard_GetData().decode())
                    else:
                        self.Robots_serial.append("Unknown")
                        self.Robots_type.append("Unknown")

                    #Modify Robot selection combo box
                    #self.comboBoxRobotSelection.addItem("Robot " +str(self.comboBoxRobotSelection.count()) )
                    self.comboBoxRobotSelection.clear()
                    for i in range (len(self.Robots_ip)):
                        self.comboBoxRobotSelection.addItem("Robot " +str(i) )

                    #select the robot to teleoperate it
                    index_robot = self.Robots_ip.index(value_ip)
                    #I change the selected robot through the robot selection button action to avoid, duplicated code
                    self.comboBoxRobotSelection.setCurrentIndex(index_robot)
                    self.RobotSelectionBtAction()


                self.stackedWidget.setCurrentIndex(1)


    def StopRobotBtAction(self):
        self.SelectedRobot.URScript_StopJoints(a=2)
        self.SelectedRobot.DashBoard_PopUp("Robot stopped")
        #To don't fill the buffer
        print(self.SelectedRobot.DashBoard_GetData().decode())

    def ShowResponse(self,Title="Response",Value="No Response"):
        self.stackedWidget.setCurrentIndex(2)
        self.labelRobotResponse.setText(Title)
        self.labelRobotResponseValue.setText(Value)

    #Dashboard Actions
    def PowerOnDashBtAction(self):
        self.SelectedRobot.DashBoard_PowerOn()
        text = self.SelectedRobot.DashBoard_GetData().decode()
        self.ShowResponse(Value=text)


    def PowerOffDashBtAction(self):
        self.SelectedRobot.DashBoard_PowerOff()

        text = self.SelectedRobot.DashBoard_GetData().decode()
        self.ShowResponse(Value=text)

    def ReleaseBreakesDashBtAction(self):
        self.SelectedRobot.DashBoard_BrakeRelease()

        text = self.SelectedRobot.DashBoard_GetData().decode()
        self.ShowResponse(Value=text)

    def ActualProgramDashBtAction(self):
        self.SelectedRobot.DashBoard_ProgramLoaded()

        text = self.SelectedRobot.DashBoard_GetData().decode()
        self.ShowResponse(Value=text,Title="Actual Program Loaded")

    def LoadInstallationDashBtAction(self):

        self.stackedWidget.setCurrentIndex(3)

        self.ActionCommandSendSend = "LoadInstallationDash"
        self.labelWriteCommandToSend.setText("Introduce the installation file to load")
        #text = self.lineEditCommandSend.text()

    def LoadProgramDashBtAction(self):

        self.stackedWidget.setCurrentIndex(3)

        self.ActionCommandSendSend = "LoadProgramDash"
        self.labelWriteCommandToSend.setText("Introduce the program file to load")
        #text = self.lineEditCommandSend.text()

    def RunProgramDashBtAction(self):
        self.SelectedRobot.DashBoard_RunProgram()

        text = self.SelectedRobot.DashBoard_GetData().decode()
        self.ShowResponse(Value=text)

    def PauseProgramDashBtAction(self):
        self.SelectedRobot.DashBoard_PauseProgram()

        text = self.SelectedRobot.DashBoard_GetData().decode()
        self.ShowResponse(Value=text)

    def OpenPopUpDashBtAction(self):

        self.stackedWidget.setCurrentIndex(3)

        self.ActionCommandSendSend = "OpenPopUpDash"
        self.labelWriteCommandToSend.setText("Introduce the message to show")
        text = self.lineEditCommandSend.text()

    def ClosePopUpDashBtAction(self):
        self.SelectedRobot.DashBoard_ClosePopUp()

        text = self.SelectedRobot.DashBoard_GetData().decode()
        self.ShowResponse(Value=text)

    def WriteLogDashBtAction(self):

        self.stackedWidget.setCurrentIndex(3)

        self.ActionCommandSendSend = "WriteLogDash"
        self.labelWriteCommandToSend.setText("Introduce the message to write")
        text = self.lineEditCommandSend.text()

    def ActualRobotModeBtAction(self):
        self.SelectedRobot.DashBoard_RobotState()

        text = self.SelectedRobot.DashBoard_GetData().decode()
        self.ShowResponse(Value=text,Title="Actual Robot Mode")

    def ChangeOperationalModeDashBtAction(self):
        self.Robot_OperationMode ^= 1 # Xor operation if 1 pass 0 else 1
        mode = self.Robot_OperationMode
        self.SelectedRobot.DashBoard_SetUserRole(mode)

        text = self.SelectedRobot.DashBoard_GetData().decode()
        self.ShowResponse(Value=text)

    def CloseSafetyPopUPDashBtAction(self):
        self.SelectedRobot.DashBoard_ClosePopUp()

        text = self.SelectedRobot.DashBoard_GetData().decode()
        self.ShowResponse(Value=text)

    def ActualSafetyModeDashBtAction(self):
        self.SelectedRobot.DashBoard_CheckSafetyMode()

        text = self.SelectedRobot.DashBoard_GetData().decode()
        self.ShowResponse(Value=text,Title="Actual Safety Mode")

    def UnlockProtectiveStopDashBtAction(self):
        self.SelectedRobot.DashBoard_UnlockProtectiveStop()
        self.SelectedRobot.DashBoard_RestartSafety()

        text = self.SelectedRobot.DashBoard_GetData().decode()
        self.ShowResponse(Value=text)

    #TCP IP
    def FreeDriveTCPBtAction(self):

        self.SelectedRobot.URScript_SetFreeDrive() if self.Robot_Freedrive == True \
        else self.SelectedRobot.URScript_StopFreeDrive()

        self.Robot_Freedrive ^= True

    def ExecuteScriptTCPBtAction(self):
        fname = QFileDialog.getOpenFileName(self.MainWindow, 'Open file', "","All Files (*)")
        print(fname[0])
        file = open(str(fname[0]))
        text = ""
        for line in file:
            text = text + line
        self.ComandTCPText.setPlainText(text)
        file.close()

    def SendScriptTCPBtAction(self):
        command = self.ComandTCPText.toPlainText()
        self.SelectedRobot.URScript_SendCommand(command)

    #ModBus
    def StartModbusDataThread(self):
        print("Refresh")

        if(self.threadpool.activeThreadCount()<1):
            ModbusThread = Get_Modbus_data_from_robot(self.SelectedRobot)
            ModbusThread.signals.result.connect(self.UpdateModbusData)
            self.threadpool.start(ModbusThread)
        else:
            print(self.threadpool.activeThreadCount())

        self.timer_Modbus.singleShot(self.time_refresh_Modbus,self.StartModbusDataThread)
        self.times_run_Modbus += 1
        print("Refresh Number "+str(self.times_run_Modbus))

        #self.timer_Modbus.stop()

    def UpdateModbusData(self,s):

        self.listWidgetRegisterNumber.clear()
        self.listWidgetRegisterDescription.clear()
        self.listWidgetRegisterValue.clear()

        self.SelectedRobot.Modbus_df_reg = s

        Address = list(self.SelectedRobot.Modbus_df_reg["Address"])
        Description = list(self.SelectedRobot.Modbus_df_reg["Description"])
        Data = list(self.SelectedRobot.Modbus_df_reg["Data"])

        #Convert it to string all
        Address_str=[]
        Data_str=[]
        for i in range(len(Address)):
            Address_str.append(str(Address[i]))
            Data_str.append(str(Data[i]))

        #Create items
        self.listWidgetRegisterNumber.addItems(Address_str)
        self.listWidgetRegisterDescription.addItems(Description)
        self.listWidgetRegisterValue.addItems(Data_str)

    def move_scrollbar(self):
        value = self.vsRN.value()

        self.vsRD.blockSignals(True)
        self.vsRD.setValue(value)
        self.vsRD.blockSignals(False)

        self.vsRV.blockSignals(True)
        self.vsRV.setValue(value)
        self.vsRV.blockSignals(False)

    def listWidgetRegisterNumberAction(self):
        Widgetindex = self.listWidgetRegisterNumber.currentIndex()
        index = Widgetindex.row()

        if(index in self.SelectedRobot.Modbus_registers_write_ind):
            self.RegisterIndexToWrite = self.SelectedRobot.Modbus_registers_write_ind.index(index)

            self.stackedWidget.setCurrentIndex(3)

            self.ActionCommandSendSend = "WriteToRegister"
            self.labelWriteCommandToSend.setText("Introduce an integer from 0 to 65536 ")
            text = self.lineEditCommandSend.text()

    def listWidgetRegisterDescriptionAction(self):
        Widgetindex = self.listWidgetRegisterDescription.currentIndex()
        index = Widgetindex.row()
        if(index in self.SelectedRobot.Modbus_registers_write_ind):
            self.RegisterIndexToWrite = self.SelectedRobot.Modbus_registers_write_ind.index(index)

            self.stackedWidget.setCurrentIndex(3)

            self.ActionCommandSendSend = "WriteToRegister"
            self.labelWriteCommandToSend.setText("Introduce an integer from 0 to 65536 ")
            text = self.lineEditCommandSend.text()

    def listWidgetRegisterValueAction(self):
        Widgetindex = self.listWidgetRegisterValue.currentIndex()
        index = Widgetindex.row()
        if(index in self.SelectedRobot.Modbus_registers_write_ind):
            self.RegisterIndexToWrite = self.SelectedRobot.Modbus_registers_write_ind.index(index)

            self.stackedWidget.setCurrentIndex(3)

            self.ActionCommandSendSend = "WriteToRegister"
            self.labelWriteCommandToSend.setText("Introduce an integer from 0 to 65536 ")
            text = self.lineEditCommandSend.text()


    #Remote control

    #JointControl
    def ActualJointAnglesBtAction(self):

        #Get joint angles values
        if(self.SelectedRobot.Modbus_Connected==True):
            jointAngles = self.SelectedRobot.Modbus_get_joint_angles()
            print(jointAngles)
        else:
            jointAngles = [0]*6


        #Set the values in the progress bars
        self.progressBarJointControlBase.setValue(jointAngles[0])
        self.progressBarJointControlShoulder.setValue(jointAngles[1])
        self.progressBarJointControlElbow.setValue(jointAngles[2])
        self.progressBarJointControlWrist1.setValue(jointAngles[3])
        self.progressBarJointControlWrist2.setValue(jointAngles[4])
        self.progressBarJointControlWrist3.setValue(jointAngles[5])

    def MoveJoints(self):
        to_rad = 3.14/180.0
        joints_target = [self.progressBarJointControlBase.value()*to_rad,\
                        self.progressBarJointControlShoulder.value()*to_rad,\
                        self.progressBarJointControlElbow.value()*to_rad,\
                        self.progressBarJointControlWrist1.value()*to_rad,\
                        self.progressBarJointControlWrist2.value()*to_rad,\
                        self.progressBarJointControlWrist3.value()*to_rad]

        self.SelectedRobot.URScript_RemoteJointControl(joints_target)

    def JointControlIncBaseBtAction(self):

        value = self.progressBarJointControlBase.value()
        value += self.doubleSpinBoxVariationAngle.value()
        self.progressBarJointControlBase.setValue(value)

        self.MoveJoints()

    def JointControlDecBaseBtAction(self):

        value = self.progressBarJointControlBase.value()
        value -= self.doubleSpinBoxVariationAngle.value()
        self.progressBarJointControlBase.setValue(value)

        self.MoveJoints()

    def JointControlIncShoulderBtAction(self):

        value = self.progressBarJointControlShoulder.value()
        value += self.doubleSpinBoxVariationAngle.value()
        self.progressBarJointControlShoulder.setValue(value)

        self.MoveJoints()

    def JointControlDecShoulderBtAction(self):

        value = self.progressBarJointControlShoulder.value()
        value -= self.doubleSpinBoxVariationAngle.value()
        self.progressBarJointControlShoulder.setValue(value)

        self.MoveJoints()

    def JointControlIncElbowBtAction(self):

        value = self.progressBarJointControlElbow.value()
        value += self.doubleSpinBoxVariationAngle.value()
        self.progressBarJointControlElbow.setValue(value)

        self.MoveJoints()

    def JointControlDecElbowBtAction(self):

        value = self.progressBarJointControlElbow.value()
        value -= self.doubleSpinBoxVariationAngle.value()
        self.progressBarJointControlElbow.setValue(value)

        self.MoveJoints()

    def JointControlIncWrist1BtAction(self):

        value = self.progressBarJointControlWrist1.value()
        value += self.doubleSpinBoxVariationAngle.value()
        self.progressBarJointControlWrist1.setValue(value)

        self.MoveJoints()

    def JointControlDecWrist1BtAction(self):

        value = self.progressBarJointControlWrist1.value()
        value -= self.doubleSpinBoxVariationAngle.value()
        self.progressBarJointControlWrist1.setValue(value)

        self.MoveJoints()
    def JointControlIncWrist2BtAction(self):

        value = self.progressBarJointControlWrist2.value()
        value += self.doubleSpinBoxVariationAngle.value()
        self.progressBarJointControlWrist2.setValue(value)

        self.MoveJoints()

    def JointControlDecWrist2BtAction(self):

        value = self.progressBarJointControlWrist2.value()
        value -= self.doubleSpinBoxVariationAngle.value()
        self.progressBarJointControlWrist2.setValue(value)

        self.MoveJoints()

    def JointControlIncWrist3BtAction(self):

        value = self.progressBarJointControlWrist3.value()
        value += self.doubleSpinBoxVariationAngle.value()
        self.progressBarJointControlWrist3.setValue(value)

        self.MoveJoints()

    def JointControlDecWrist3BtAction(self):

        value = self.progressBarJointControlWrist3.value()
        value -= self.doubleSpinBoxVariationAngle.value()
        self.progressBarJointControlWrist3.setValue(value)

        self.MoveJoints()

    #Cartesian control
    def CartesianControlIncXBtAction(self):

        poseinc = [0]*6
        poseinc[0] += (self.spinBoxVariationPosition.value())/(10**3)

        if(self.comboBoxCartesianControlReference.currentIndex() == 0):
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=False)
        else:
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=True)


    def CartesianControlDecXBtAction(self):

        poseinc = [0]*6
        poseinc[0] -= (self.spinBoxVariationPosition.value())/(10**3)

        if(self.comboBoxCartesianControlReference.currentIndex() == 0):
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=False)
        else:
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=True)

    def CartesianControlIncYBtAction(self):

        poseinc = [0]*6
        poseinc[1] += (self.spinBoxVariationPosition.value())/(10**3)

        if(self.comboBoxCartesianControlReference.currentIndex() == 0):
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=False)
        else:
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=True)

    def CartesianControlDecYBtAction(self):

        poseinc = [0]*6
        poseinc[1] -= (self.spinBoxVariationPosition.value())/(10**3)

        if(self.comboBoxCartesianControlReference.currentIndex() == 0):
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=False)
        else:
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=True)

    def CartesianControlIncZBtAction(self):

        poseinc = [0]*6
        poseinc[2] += (self.spinBoxVariationPosition.value())/(10**3)

        if(self.comboBoxCartesianControlReference.currentIndex() == 0):
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=False)
        else:
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=True)

    def CartesianControlDecZBtAction(self):

        poseinc = [0]*6
        poseinc[2] -= (self.spinBoxVariationPosition.value())/(10**3)

        if(self.comboBoxCartesianControlReference.currentIndex() == 0):
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=False)
        else:
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=True)

    def CartesianControlIncRxBtAction(self):

        poseinc = [0]*6
        poseinc[3] += (self.doubleSpinBoxVariationOrientation.value())*(3.14/180)

        if(self.comboBoxCartesianControlReference.currentIndex() == 0):
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=False)
        else:
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=True)

    def CartesianControlDecRxBtAction(self):

        poseinc = [0]*6
        poseinc[3] -= (self.doubleSpinBoxVariationOrientation.value())*(3.14/180)

        if(self.comboBoxCartesianControlReference.currentIndex() == 0):
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=False)
        else:
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=True)

    def CartesianControlIncRyBtAction(self):

        poseinc = [0]*6
        poseinc[4] += (self.doubleSpinBoxVariationOrientation.value())*(3.14/180)

        if(self.comboBoxCartesianControlReference.currentIndex() == 0):
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=False)
        else:
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=True)

    def CartesianControlDecRyBtAction(self):

        poseinc = [0]*6
        poseinc[4] -= (self.doubleSpinBoxVariationOrientation.value())*(3.14/180)

        if(self.comboBoxCartesianControlReference.currentIndex() == 0):
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=False)
        else:
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=True)

    def CartesianControlIncRzBtAction(self):

        poseinc = [0]*6
        poseinc[5] += (self.doubleSpinBoxVariationOrientation.value())*(3.14/180)

        if(self.comboBoxCartesianControlReference.currentIndex() == 0):
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=False)
        else:
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=True)

    def CartesianControlDecRzBtAction(self):

        poseinc = [0]*6
        poseinc[5] -= (self.doubleSpinBoxVariationOrientation.value())*(3.14/180)

        if(self.comboBoxCartesianControlReference.currentIndex() == 0):
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=False)
        else:
            self.SelectedRobot.URScript_RemoteCartesianControl_offset(poseinc,tool=True)


    #Move to position
    def SendCartesianPositionBtAction(self):

        Pose = [0]*6

        try:

            Pose [0] = float(self.lineEditXPosition.text())/(10**3)
            Pose [1] = float(self.lineEditYPosition.text())/(10**3)
            Pose [2] = float(self.lineEditZPosition.text())/(10**3)

            Pose [3] = float(self.lineEditRxPosition.text())*(3.14/180)
            Pose [4] = float(self.lineEditRyPosition.text())*(3.14/180)
            Pose [5] = float(self.lineEditRzPosition.text())*(3.14/180)

            self.SelectedRobot.URScript_MoveToPoseJointSpaceBaseFrame(Pose)

        except:


            print(sys.exc_info()[0])
            msg = QMessageBox()
            msg.setWindowTitle("An introduced value it's not a float")
            msg.setText("An introduced value it's not a float, change it to move")
            x = msg.exec_()






    def SendJointPositionBtAction(self):

        Joint = [0]*6

        try:

            Joint [0] = float(self.lineEdit_BaseJoint.text())*(3.14/180)
            Joint [1] = float(self.lineEdit_ShoulderJoint.text())*(3.14/180)
            Joint [2] = float(self.lineEdit_ElbowJoint.text())*(3.14/180)

            Joint [3] = float(self.lineEdit_WristJoint1.text())*(3.14/180)
            Joint [4] = float(self.lineEdit_Wrist2Joint.text())*(3.14/180)
            Joint [5] = float(self.lineEdit_Wrist3Joint.text())*(3.14/180)

            self.SelectedRobot.URScript_MoveJoints(Joint)

        except:


            msg = QMessageBox()
            msg.setWindowTitle("An introduced value it's not a float")
            msg.setText("An introduced value it's not a float, change it to move")
            x = msg.exec_()

    def RobotSelectionBtAction(self):
        Index = self.comboBoxRobotSelection.currentIndex()


        if(self.SelectedRobotOld != None):
            self.SelectedRobotOld.Disconnect()
        if(self.SelectedRobot!= None):
            self.SelectedRobotOld = self.SelectedRobot

        #Get info of the selected index
        self.SelectedRobot = self.Robots[Index]
        SerialNumber = self.Robots_serial[Index]
        Type = self.Robots_type[Index]

        self.labelSerialNumber.setText("Serial Number:"+SerialNumber)
        self.labelRobotType.setText("Robot Type:"+Type)

        #Start timer if Modbus connection it's able
        if(self.SelectedRobot.Modbus_Connected==True):
            #self.timer_Modbus.start(self.time_refresh_Modbus)
            #self.timer_Modbus.timeout.connect(self.StartModbusDataThread)
            self.timer_Modbus.singleShot(self.time_refresh_Modbus,self.StartModbusDataThread)
            self.times_run_Modbus = 0
        else:
            self.SelectedRobot.Modbus_Connect()



    def AddNewRobotBtAction(self):

        self.stackedWidget.setCurrentIndex(0)


    #Extra pages

    def RobotResponseBackAction(self):

        self.stackedWidget.setCurrentIndex(1)

    def CommandSendBackBtAction(self):

        self.stackedWidget.setCurrentIndex(1)

    def CommandSendSendBtAction(self):

        value = self.lineEditCommandSend.text()
        print(value)
        self.lineEditCommandSend.setText("")

        if(self.ActionCommandSendSend == "WriteLogDash"):
            self.SelectedRobot.DashBoard_WriteToLog(value)
        elif(self.ActionCommandSendSend == "LoadProgramDash"):
            self.SelectedRobot.DashBoard_LoadProgram(value)
        elif(self.ActionCommandSendSend == "LoadInstallationDash"):
            self.SelectedRobot.DashBoard_LoadInstallation(value)
        elif(self.ActionCommandSendSend == "OpenPopUpDash"):
            self.SelectedRobot.DashBoard_PopUp(value)
        elif(self.ActionCommandSendSend == "WriteToRegister"):
            Adrres_dec=self.SelectedRobot.Modbus_registers_write[self.RegisterIndexToWrite]
            try:
                Value_to_write_dec = int(value)
                self.SelectedRobot.Modbus_Request_to_write(Adrres_dec,Value_to_write_dec,printb = False)
            except:
                msg = QMessageBox()
                msg.setWindowTitle("Data not send")
                msg.setText("Data not send due to the value introduced is not an integer, or the connection failed \n Modbus_Connected " + str(self.SelectedRobot.Modbus_Connected))
                #msg.setText(str(sys.exc_info()[0]))
                retval = msg.exec_()
        else:
            print("Action "+self.ActionCommandSendSend + "not especified")

        if(self.ActionCommandSendSend != "WriteToRegister"):
            text = self.SelectedRobot.DashBoard_GetData().decode()
            self.ShowResponse(Value=text)
        else:
            self.stackedWidget.setCurrentIndex(1)






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)



    MainWindow.show()
    sys.exit(app.exec_())
