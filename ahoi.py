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
        self.el_technologies_user = []


    def setupUi(self, MainWindow):

        MainWindow.setObjectName("SGT!!!!!!!!!!!!!")
        MainWindow.resize(555, 389)
        MainWindow.setAcceptDrops(True)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 161, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label1 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label1.setTextFormat(QtCore.Qt.RichText)
        self.label1.setWordWrap(True)
        self.label1.setObjectName("label1")
        self.verticalLayout.addWidget(self.label1)
        self.CHP1 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.CHP1.setObjectName("CHP1")
        self.verticalLayout.addWidget(self.CHP1)
        self.boiler1 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.boiler1.setObjectName("boiler1")
        self.verticalLayout.addWidget(self.boiler1)
        self.thermalstorage1 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.thermalstorage1.setObjectName("thermalstorage")
        self.verticalLayout.addWidget(self.thermalstorage1)
        self.solarthermal1 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.solarthermal1.setObjectName("solarthermal")
        self.verticalLayout.addWidget(self.solarthermal1)
        self.electricheater1 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.electricheater1.setObjectName("electricheater1")
        self.verticalLayout.addWidget(self.electricheater1)
        self.photovoltaics1 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.photovoltaics1.setObjectName("photovoltaics1")
        self.verticalLayout.addWidget(self.photovoltaics1)
        self.electricstorage1 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.electricstorage1.setObjectName("electricstorage1")
        self.verticalLayout.addWidget(self.electricstorage1)
        self.buttonBox = QtGui.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(QtCore.QRect(200, 250, 159, 31))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.radioButton = QtGui.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(180, 220, 171, 16))
        self.radioButton.setObjectName("radioButton")
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(427, 30, 77, 154))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btnOutputBrowse = QtGui.QPushButton(self.layoutWidget)
        self.btnOutputBrowse.setObjectName("btnOutputBrowse")
        self.verticalLayout_3.addWidget(self.btnOutputBrowse)
        self.btnWeathreBrowse = QtGui.QPushButton(self.layoutWidget)
        self.btnWeathreBrowse.setObjectName("btnWeathreBrowse")
        self.verticalLayout_3.addWidget(self.btnWeathreBrowse)
        self.btnHeatprofilesBrowse = QtGui.QPushButton(self.layoutWidget)
        self.btnHeatprofilesBrowse.setObjectName("btnHeatprofilesBrowse")
        self.verticalLayout_3.addWidget(self.btnHeatprofilesBrowse)
        self.btnElProfileBrowse = QtGui.QPushButton(self.layoutWidget)
        self.btnElProfileBrowse.setObjectName("btnElProfileBrowse")
        self.verticalLayout_3.addWidget(self.btnElProfileBrowse)
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(210, 30, 211, 151))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.OutputFolderLineEdit = QtGui.QLineEdit(self.widget)
        self.OutputFolderLineEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.OutputFolderLineEdit.setObjectName("OutputFolderLineEdit")
        self.verticalLayout_2.addWidget(self.OutputFolderLineEdit)
        self.WeatherDataLineEdit = QtGui.QLineEdit(self.widget)
        self.WeatherDataLineEdit.setObjectName("WeatherDataLineEdit")
        self.verticalLayout_2.addWidget(self.WeatherDataLineEdit)
        self.HProfileLineEdit = QtGui.QLineEdit(self.widget)
        self.HProfileLineEdit.setObjectName("HProfileLineEdit")
        self.verticalLayout_2.addWidget(self.HProfileLineEdit)
        self.ElProfileLineEdit = QtGui.QLineEdit(self.widget)
        self.ElProfileLineEdit.setObjectName("ElProfileLineEdit")
        self.verticalLayout_2.addWidget(self.ElProfileLineEdit)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 555, 21))
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
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.update)
        QtCore.QObject.connect(self.btnOutputBrowse, QtCore.SIGNAL("clicked()"), self.output_folder)
        QtCore.QObject.connect(self.btnWeathreBrowse, QtCore.SIGNAL("clicked()"), self.weather_file1)
        QtCore.QObject.connect(self.btnHeatprofilesBrowse, QtCore.SIGNAL("clicked()"), self.heat_profiles_file)
        QtCore.QObject.connect(self.btnElProfileBrowse, QtCore.SIGNAL("clicked()"), self.el_profiles_file)
        QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL("clicked(bool)"), self.radioButton.setChecked)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Welcome to the SGT UI", None, QtGui.QApplication.UnicodeUTF8))
        self.label1.setText(QtGui.QApplication.translate("MainWindow", "Choose technologies that can be present in the system:", None, QtGui.QApplication.UnicodeUTF8))
        self.CHP1.setText(QtGui.QApplication.translate("MainWindow", "CHP", None, QtGui.QApplication.UnicodeUTF8))
        self.boiler1.setText(QtGui.QApplication.translate("MainWindow", "Boiler", None, QtGui.QApplication.UnicodeUTF8))
        self.thermalstorage1.setText(QtGui.QApplication.translate("MainWindow", "Thermal Storage", None, QtGui.QApplication.UnicodeUTF8))
        self.solarthermal1.setText(QtGui.QApplication.translate("MainWindow", "Solar Thermal", None, QtGui.QApplication.UnicodeUTF8))
        self.electricheater1.setText(QtGui.QApplication.translate("MainWindow", "Electric Heater", None, QtGui.QApplication.UnicodeUTF8))
        self.photovoltaics1.setText(QtGui.QApplication.translate("MainWindow", "Photovoltaics", None, QtGui.QApplication.UnicodeUTF8))
        self.electricstorage1.setText(QtGui.QApplication.translate("MainWindow", "Electric Storage", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("MainWindow", "Hourly excels required?", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOutputBrowse.setText(QtGui.QApplication.translate("MainWindow", "Browse..", None, QtGui.QApplication.UnicodeUTF8))
        self.btnWeathreBrowse.setText(QtGui.QApplication.translate("MainWindow", "Browse..", None, QtGui.QApplication.UnicodeUTF8))
        self.btnHeatprofilesBrowse.setText(QtGui.QApplication.translate("MainWindow", "Browse..", None, QtGui.QApplication.UnicodeUTF8))
        self.btnElProfileBrowse.setText(QtGui.QApplication.translate("MainWindow", "Browse..", None, QtGui.QApplication.UnicodeUTF8))

    def update(self):
        self.CHP1.setChecked(False)
        self.boiler1.setChecked(False)
        self.thermalstorage1.setChecked(False)
        self.solarthermal1.setChecked(False)
        self.electricheater1.setChecked(False)
        self.photovoltaics1.setChecked(False)
        self.electricstorage1.setChecked(False)
        self.OutputFolderLineEdit.clear()
        self.WeatherDataLineEdit.clear()
        self.ElProfileLineEdit.clear()
        self.HProfileLineEdit.clear()
        self.radioButton.setChecked(False)


    def output_folder(self):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        self.output_folder_name = dialog.getExistingDirectory(dialog, 'Choose Directory',os.path.curdir)
        self.OutputFolderLineEdit.insert(self.output_folder_name)
        return

    def weather_file1(self):
        dialog = QtGui.QFileDialog()
        # self.weather_file_location = dialog.getExistingDirectory(dialog, 'Choose Directory', os.path.curdir)
        self.weather_file_name, discard = dialog.getOpenFileName(caption="Choose TRY weather File",
                                                                 filter=".csv files(*.csv)")
        self.WeatherDataLineEdit.insert(self.weather_file_name)
        return

    def el_profiles_file(self):
        dialog = QtGui.QFileDialog()
        # self.weather_file_location = dialog.getExistingDirectory(dialog, 'Choose Directory', os.path.curdir)
        self.electrical_profiles_name, discard = dialog.getOpenFileName(caption="Choose file with electrical profiles",
                                                                        filter="Excel files(*.xlsx *.xls)",
                                                                        )
        self.ElProfileLineEdit.insert(self.electrical_profiles_name)
        return

    def heat_profiles_file(self):
        dialog = QtGui.QFileDialog()
        # self.weather_file_location = dialog.getExistingDirectory(dialog, 'Choose Directory', os.path.curdir)
        self.heat_profiles_name, discard = dialog.getOpenFileName(caption="Choose file with heat profiles",
                                                                   filter="Excel files(*.xlsx *.xls)",
                                                                  )
        self.HProfileLineEdit.insert(self.heat_profiles_name)
        return

    def run_ppt(self):
        print self.weather_file_name
        global_radiation = loaddata.get_weather_data(self.weather_file_name)
        heat_profiles, building_ids = loaddata.get_heat_profiles(self.heat_profiles_name)
        el_profiles, building_ids = loaddata.get_el_profiles(self.electrical_profiles_name)

        if self.CHP1.isChecked():
            self.th_technologies_user.append('CHP')
        if self.boiler1.isChecked():
            self.th_technologies_user.append('B')
        if self.thermalstorage1.isChecked():
            self.th_technologies_user.append('ThSt')
        if self.solarthermal1.isChecked():
            self.th_technologies_user.append('SolTh')
        if self.electricheater1.isChecked():
            self.th_technologies_user.append('ElHe')
        if self.electricstorage1.isChecked():
            self.el_technologies_user.append('ElSt')
        if self.photovoltaics1.isChecked():
            self.el_technologies_user.append('PV')
        print self.th_technologies_user, self.el_technologies_user

        if self.radioButton.isChecked():
            hourly_excels = True
        else:
            hourly_excels = False

        for i in range(0, len(building_ids)):
            building_id = building_ids[i]
            thermal_profile = heat_profiles[i]
            electrical_profile = el_profiles[i]
            building_number = preprocessingtool.PreProcessingTool(building_id=building_id,
                                                                  thermal_profile=thermal_profile,
                                                                  electrical_profile=electrical_profile,
                                                                  global_radiation=global_radiation,
                                                                  th_technologies=self.th_technologies_user,
                                                                  el_technologies=self.el_technologies_user,
                                                                  location=self.output_folder_name,
                                                                  hourly_excels=hourly_excels)
            building_number.generate_cases()

        os.chdir("D:/aja-gmu/Simulation_Files")