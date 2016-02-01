# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created: Mon Feb 01 14:59:26 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import loaddata
import preprocessingtool
import os


class Ui_MainWindow(object):
    def __init__(self):
        self.th_technologies_user = []

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(206, 313)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 161, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.CHP1 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.CHP1.setObjectName("CHP")
        self.verticalLayout.addWidget(self.CHP1)
        self.boiler1 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.boiler1.setObjectName("boiler")
        self.verticalLayout.addWidget(self.boiler1)
        self.thermalstorage1 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.thermalstorage1.setObjectName("thermalstorage")
        self.verticalLayout.addWidget(self.thermalstorage1)
        self.solarthermal1 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.solarthermal1.setObjectName("solarthermal")
        self.verticalLayout.addWidget(self.solarthermal1)
        self.electricheater1 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.electricheater1.setObjectName("electricheater")
        self.verticalLayout.addWidget(self.electricheater1)
        self.photovoltaics1 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.photovoltaics1.setObjectName("photovoltaics")
        self.verticalLayout.addWidget(self.photovoltaics1)
        self.electricstorage1 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.electricstorage1.setObjectName("electricstorage")
        self.verticalLayout.addWidget(self.electricstorage1)
        self.buttonBox = QtGui.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 206, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.CHP1, QtCore.SIGNAL("clicked(bool)"), self.CHP1.setChecked)
        QtCore.QObject.connect(self.boiler1, QtCore.SIGNAL("clicked(bool)"), self.boiler1.setChecked)
        QtCore.QObject.connect(self.electricheater1, QtCore.SIGNAL("clicked(bool)"), self.electricheater1.setChecked)
        QtCore.QObject.connect(self.electricstorage1, QtCore.SIGNAL("clicked(bool)"), self.electricstorage1.setChecked)
        QtCore.QObject.connect(self.photovoltaics1, QtCore.SIGNAL("clicked(bool)"), self.photovoltaics1.setChecked)
        QtCore.QObject.connect(self.solarthermal1, QtCore.SIGNAL("clicked(bool)"), self.solarthermal1.setChecked)
        QtCore.QObject.connect(self.thermalstorage1, QtCore.SIGNAL("clicked(bool)"), self.thermalstorage1.setChecked)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.run_ppt)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.buttonBox.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.CHP1.setText(QtGui.QApplication.translate("MainWindow", "CHP", None, QtGui.QApplication.UnicodeUTF8))
        self.boiler1.setText(QtGui.QApplication.translate("MainWindow", "Boiler", None, QtGui.QApplication.UnicodeUTF8))
        self.thermalstorage1.setText(QtGui.QApplication.translate("MainWindow", "Thermal Storage", None, QtGui.QApplication.UnicodeUTF8))
        self.solarthermal1.setText(QtGui.QApplication.translate("MainWindow", "Solar Thermal", None, QtGui.QApplication.UnicodeUTF8))
        self.electricheater1.setText(QtGui.QApplication.translate("MainWindow", "Electric Heater", None, QtGui.QApplication.UnicodeUTF8))
        self.photovoltaics1.setText(QtGui.QApplication.translate("MainWindow", "Photovoltaics", None, QtGui.QApplication.UnicodeUTF8))
        self.electricstorage1.setText(QtGui.QApplication.translate("MainWindow", "Electric Storage", None, QtGui.QApplication.UnicodeUTF8))


    def run_ppt(self):
        global_radiation = loaddata.get_weather_data("D:/aja-gmu/Simulation_Files")
        heat_profiles, building_ids = loaddata.get_heat_profiles("D:/aja-gmu/Simulation_Files")
        el_profiles, building_ids = loaddata.get_el_profiles("D:/aja-gmu/Simulation_Files")

        if self.CHP1.isChecked():
            self.th_technologies_user.append('CHP')
        if self.boiler1.isChecked():
            self.th_technologies_user.append('B')
        if self.thermalstorage1.isChecked():
            self.th_technologies_user.append('ThSt')
        if self.electricheater1.isChecked():
            self.th_technologies_user.append('ElHe')
        if self.electricstorage1.isChecked():
            self.th_technologies_user.append('ElSt')
        if self.solarthermal1.isChecked():
            self.th_technologies_user.append('SolTh')
        if self.photovoltaics1.isChecked():
            self.th_technologies_user.append('PV')
        print self.th_technologies_user

        for i in range(0, len(building_ids)):
            building_id = building_ids[i]
            thermal_profile = heat_profiles[i]
            electrical_profile = el_profiles[i]
            building_number = preprocessingtool.PreProcessingTool(building_id=building_id,
                                                                  thermal_profile=thermal_profile,
                                                                  electrical_profile=electrical_profile,
                                                                  global_radiation=global_radiation,
                                                                  th_technologies=self.th_technologies_user)
            building_number.generate_cases()

        os.chdir("D:/aja-gmu/Simulation_Files")