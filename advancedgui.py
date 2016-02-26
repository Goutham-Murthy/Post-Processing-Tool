# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class UiMainWindow(object):
    def setupUi(self, rtrtjrtj):
        rtrtjrtj.setObjectName(_fromUtf8("rtrtjrtj"))
        rtrtjrtj.resize(914, 470)
        rtrtjrtj.setAcceptDrops(True)
        rtrtjrtj.setDocumentMode(False)
        self.centralwidget = QtGui.QWidget(rtrtjrtj)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(40, 10, 781, 281))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabTechnologies = QtGui.QWidget()
        self.tabTechnologies.setObjectName(_fromUtf8("tabTechnologies"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tabTechnologies)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label1 = QtGui.QLabel(self.tabTechnologies)
        self.label1.setTextFormat(QtCore.Qt.RichText)
        self.label1.setWordWrap(True)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.verticalLayout.addWidget(self.label1)
        self.CHP1 = QtGui.QCheckBox(self.tabTechnologies)
        self.CHP1.setObjectName(_fromUtf8("CHP1"))
        self.verticalLayout.addWidget(self.CHP1)
        self.boiler1 = QtGui.QCheckBox(self.tabTechnologies)
        self.boiler1.setObjectName(_fromUtf8("boiler1"))
        self.verticalLayout.addWidget(self.boiler1)
        self.thermalstorage = QtGui.QCheckBox(self.tabTechnologies)
        self.thermalstorage.setObjectName(_fromUtf8("thermalstorage"))
        self.verticalLayout.addWidget(self.thermalstorage)
        self.solarthermal = QtGui.QCheckBox(self.tabTechnologies)
        self.solarthermal.setObjectName(_fromUtf8("solarthermal"))
        self.verticalLayout.addWidget(self.solarthermal)
        self.electricheater1 = QtGui.QCheckBox(self.tabTechnologies)
        self.electricheater1.setObjectName(_fromUtf8("electricheater1"))
        self.verticalLayout.addWidget(self.electricheater1)
        self.photovoltaics1 = QtGui.QCheckBox(self.tabTechnologies)
        self.photovoltaics1.setObjectName(_fromUtf8("photovoltaics1"))
        self.verticalLayout.addWidget(self.photovoltaics1)
        self.electricstorage1 = QtGui.QCheckBox(self.tabTechnologies)
        self.electricstorage1.setObjectName(_fromUtf8("electricstorage1"))
        self.verticalLayout.addWidget(self.electricstorage1)
        self.tabWidget.addTab(self.tabTechnologies, _fromUtf8(""))
        self.tabFolders = QtGui.QWidget()
        self.tabFolders.setObjectName(_fromUtf8("tabFolders"))
        self.gridLayout = QtGui.QGridLayout(self.tabFolders)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.OutputFolderLineEdit = QtGui.QLineEdit(self.tabFolders)
        self.OutputFolderLineEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.OutputFolderLineEdit.setObjectName(_fromUtf8("OutputFolderLineEdit"))
        self.gridLayout.addWidget(self.OutputFolderLineEdit, 0, 0, 1, 1)
        self.btnOutputBrowse = QtGui.QPushButton(self.tabFolders)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnOutputBrowse.sizePolicy().hasHeightForWidth())
        self.btnOutputBrowse.setSizePolicy(sizePolicy)
        self.btnOutputBrowse.setDefault(False)
        self.btnOutputBrowse.setObjectName(_fromUtf8("btnOutputBrowse"))
        self.gridLayout.addWidget(self.btnOutputBrowse, 0, 1, 1, 1)
        self.WeatherDataLineEdit = QtGui.QLineEdit(self.tabFolders)
        self.WeatherDataLineEdit.setObjectName(_fromUtf8("WeatherDataLineEdit"))
        self.gridLayout.addWidget(self.WeatherDataLineEdit, 1, 0, 1, 1)
        self.btnWeathreBrowse = QtGui.QPushButton(self.tabFolders)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnWeathreBrowse.sizePolicy().hasHeightForWidth())
        self.btnWeathreBrowse.setSizePolicy(sizePolicy)
        self.btnWeathreBrowse.setObjectName(_fromUtf8("btnWeathreBrowse"))
        self.gridLayout.addWidget(self.btnWeathreBrowse, 1, 1, 1, 1)
        self.ElProfileLineEdit = QtGui.QLineEdit(self.tabFolders)
        self.ElProfileLineEdit.setObjectName(_fromUtf8("ElProfileLineEdit"))
        self.gridLayout.addWidget(self.ElProfileLineEdit, 2, 0, 1, 1)
        self.btnHeatprofilesBrowse = QtGui.QPushButton(self.tabFolders)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnHeatprofilesBrowse.sizePolicy().hasHeightForWidth())
        self.btnHeatprofilesBrowse.setSizePolicy(sizePolicy)
        self.btnHeatprofilesBrowse.setObjectName(_fromUtf8("btnHeatprofilesBrowse"))
        self.gridLayout.addWidget(self.btnHeatprofilesBrowse, 2, 1, 1, 1)
        self.HProfileLineEdit = QtGui.QLineEdit(self.tabFolders)
        self.HProfileLineEdit.setObjectName(_fromUtf8("HProfileLineEdit"))
        self.gridLayout.addWidget(self.HProfileLineEdit, 3, 0, 1, 1)
        self.btnElProfileBrowse = QtGui.QPushButton(self.tabFolders)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnElProfileBrowse.sizePolicy().hasHeightForWidth())
        self.btnElProfileBrowse.setSizePolicy(sizePolicy)
        self.btnElProfileBrowse.setObjectName(_fromUtf8("btnElProfileBrowse"))
        self.gridLayout.addWidget(self.btnElProfileBrowse, 3, 1, 1, 1)
        self.radioButton = QtGui.QRadioButton(self.tabFolders)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.gridLayout.addWidget(self.radioButton, 4, 0, 1, 1)
        self.tabWidget.addTab(self.tabFolders, _fromUtf8(""))
        self.tabGDetails = QtGui.QWidget()
        self.tabGDetails.setObjectName(_fromUtf8("tabGDetails"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabGDetails)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.labelElPrice = QtGui.QLabel(self.tabGDetails)
        self.labelElPrice.setObjectName(_fromUtf8("labelElPrice"))
        self.gridLayout_2.addWidget(self.labelElPrice, 0, 0, 1, 1)
        self.lineEditElPrice = QtGui.QLineEdit(self.tabGDetails)
        self.lineEditElPrice.setObjectName(_fromUtf8("lineEditElPrice"))
        self.gridLayout_2.addWidget(self.lineEditElPrice, 0, 1, 1, 1)
        self.labelGprice = QtGui.QLabel(self.tabGDetails)
        self.labelGprice.setObjectName(_fromUtf8("labelGprice"))
        self.gridLayout_2.addWidget(self.labelGprice, 1, 0, 1, 1)
        self.lineEditGPrice = QtGui.QLineEdit(self.tabGDetails)
        self.lineEditGPrice.setObjectName(_fromUtf8("lineEditGPrice"))
        self.gridLayout_2.addWidget(self.lineEditGPrice, 1, 1, 1, 1)
        self.tabWidget.addTab(self.tabGDetails, _fromUtf8(""))
        self.tabCHP = QtGui.QWidget()
        self.tabCHP.setObjectName(_fromUtf8("tabCHP"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabCHP)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.labelCHPModelFix = QtGui.QLabel(self.tabCHP)
        self.labelCHPModelFix.setObjectName(_fromUtf8("labelCHPModelFix"))
        self.gridLayout_3.addWidget(self.labelCHPModelFix, 7, 0, 1, 1)
        self.pushButtonAddCHP = QtGui.QPushButton(self.tabCHP)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAddCHP.sizePolicy().hasHeightForWidth())
        self.pushButtonAddCHP.setSizePolicy(sizePolicy)
        self.pushButtonAddCHP.setObjectName(_fromUtf8("pushButtonAddCHP"))
        self.gridLayout_3.addWidget(self.pushButtonAddCHP, 5, 0, 1, 2)
        self.lineEditCHPFIT = QtGui.QLineEdit(self.tabCHP)
        self.lineEditCHPFIT.setObjectName(_fromUtf8("lineEditCHPFIT"))
        self.gridLayout_3.addWidget(self.lineEditCHPFIT, 3, 1, 1, 1)
        self.pushButtonAdvAnnuityCHP = QtGui.QPushButton(self.tabCHP)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAdvAnnuityCHP.sizePolicy().hasHeightForWidth())
        self.pushButtonAdvAnnuityCHP.setSizePolicy(sizePolicy)
        self.pushButtonAdvAnnuityCHP.setObjectName(_fromUtf8("pushButtonAdvAnnuityCHP"))
        self.gridLayout_3.addWidget(self.pushButtonAdvAnnuityCHP, 4, 0, 1, 2)
        self.radioButtonContCHP = QtGui.QRadioButton(self.tabCHP)
        self.radioButtonContCHP.setObjectName(_fromUtf8("radioButtonContCHP"))
        self.gridLayout_3.addWidget(self.radioButtonContCHP, 2, 0, 1, 1)
        self.radioButtonONOFFCHP = QtGui.QRadioButton(self.tabCHP)
        self.radioButtonONOFFCHP.setObjectName(_fromUtf8("radioButtonONOFFCHP"))
        self.gridLayout_3.addWidget(self.radioButtonONOFFCHP, 0, 0, 1, 1)
        self.lineEditCHPModelFix = QtGui.QLineEdit(self.tabCHP)
        self.lineEditCHPModelFix.setObjectName(_fromUtf8("lineEditCHPModelFix"))
        self.gridLayout_3.addWidget(self.lineEditCHPModelFix, 7, 1, 1, 1)
        self.labelCHPFIT = QtGui.QLabel(self.tabCHP)
        self.labelCHPFIT.setObjectName(_fromUtf8("labelCHPFIT"))
        self.gridLayout_3.addWidget(self.labelCHPFIT, 3, 0, 1, 1)
        self.radioButtonModCHP = QtGui.QRadioButton(self.tabCHP)
        self.radioButtonModCHP.setObjectName(_fromUtf8("radioButtonModCHP"))
        self.gridLayout_3.addWidget(self.radioButtonModCHP, 1, 0, 1, 1)
        self.checkBoxFixCHP = QtGui.QCheckBox(self.tabCHP)
        self.checkBoxFixCHP.setObjectName(_fromUtf8("checkBoxFixCHP"))
        self.gridLayout_3.addWidget(self.checkBoxFixCHP, 6, 0, 1, 1)
        self.tabWidget.addTab(self.tabCHP, _fromUtf8(""))
        self.tabBoiler = QtGui.QWidget()
        self.tabBoiler.setObjectName(_fromUtf8("tabBoiler"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tabBoiler)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.pushButtonAddBoiler = QtGui.QPushButton(self.tabBoiler)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAddBoiler.sizePolicy().hasHeightForWidth())
        self.pushButtonAddBoiler.setSizePolicy(sizePolicy)
        self.pushButtonAddBoiler.setObjectName(_fromUtf8("pushButtonAddBoiler"))
        self.gridLayout_4.addWidget(self.pushButtonAddBoiler, 1, 0, 1, 2)
        self.lineEditBoilerModelFix = QtGui.QLineEdit(self.tabBoiler)
        self.lineEditBoilerModelFix.setObjectName(_fromUtf8("lineEditBoilerModelFix"))
        self.gridLayout_4.addWidget(self.lineEditBoilerModelFix, 3, 1, 1, 1)
        self.pushButtonAdvAnnuityBoiler = QtGui.QPushButton(self.tabBoiler)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAdvAnnuityBoiler.sizePolicy().hasHeightForWidth())
        self.pushButtonAdvAnnuityBoiler.setSizePolicy(sizePolicy)
        self.pushButtonAdvAnnuityBoiler.setObjectName(_fromUtf8("pushButtonAdvAnnuityBoiler"))
        self.gridLayout_4.addWidget(self.pushButtonAdvAnnuityBoiler, 0, 0, 1, 2)
        self.labelBoilerModelFix = QtGui.QLabel(self.tabBoiler)
        self.labelBoilerModelFix.setObjectName(_fromUtf8("labelBoilerModelFix"))
        self.gridLayout_4.addWidget(self.labelBoilerModelFix, 3, 0, 1, 1)
        self.checkBox = QtGui.QCheckBox(self.tabBoiler)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout_4.addWidget(self.checkBox, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tabBoiler, _fromUtf8(""))
        self.tabThSt = QtGui.QWidget()
        self.tabThSt.setObjectName(_fromUtf8("tabThSt"))
        self.gridLayout_5 = QtGui.QGridLayout(self.tabThSt)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.pushButtonAdvAnnuityThSt = QtGui.QPushButton(self.tabThSt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAdvAnnuityThSt.sizePolicy().hasHeightForWidth())
        self.pushButtonAdvAnnuityThSt.setSizePolicy(sizePolicy)
        self.pushButtonAdvAnnuityThSt.setObjectName(_fromUtf8("pushButtonAdvAnnuityThSt"))
        self.gridLayout_5.addWidget(self.pushButtonAdvAnnuityThSt, 0, 0, 1, 2)
        self.pushButtonAddThSt = QtGui.QPushButton(self.tabThSt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAddThSt.sizePolicy().hasHeightForWidth())
        self.pushButtonAddThSt.setSizePolicy(sizePolicy)
        self.pushButtonAddThSt.setObjectName(_fromUtf8("pushButtonAddThSt"))
        self.gridLayout_5.addWidget(self.pushButtonAddThSt, 1, 0, 1, 2)
        self.checkBoxFixThSt = QtGui.QCheckBox(self.tabThSt)
        self.checkBoxFixThSt.setObjectName(_fromUtf8("checkBoxFixThSt"))
        self.gridLayout_5.addWidget(self.checkBoxFixThSt, 2, 0, 1, 2)
        self.labelThStModelFix = QtGui.QLabel(self.tabThSt)
        self.labelThStModelFix.setObjectName(_fromUtf8("labelThStModelFix"))
        self.gridLayout_5.addWidget(self.labelThStModelFix, 3, 0, 1, 1)
        self.lineEditThStModelFix = QtGui.QLineEdit(self.tabThSt)
        self.lineEditThStModelFix.setObjectName(_fromUtf8("lineEditThStModelFix"))
        self.gridLayout_5.addWidget(self.lineEditThStModelFix, 3, 1, 1, 1)
        self.tabWidget.addTab(self.tabThSt, _fromUtf8(""))
        self.tabSolTh = QtGui.QWidget()
        self.tabSolTh.setObjectName(_fromUtf8("tabSolTh"))
        self.gridLayout_6 = QtGui.QGridLayout(self.tabSolTh)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.pushButtonAddSolTh = QtGui.QPushButton(self.tabSolTh)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAddSolTh.sizePolicy().hasHeightForWidth())
        self.pushButtonAddSolTh.setSizePolicy(sizePolicy)
        self.pushButtonAddSolTh.setObjectName(_fromUtf8("pushButtonAddSolTh"))
        self.gridLayout_6.addWidget(self.pushButtonAddSolTh, 1, 0, 1, 2)
        self.pushButtonAdvAnnuitySolTh = QtGui.QPushButton(self.tabSolTh)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAdvAnnuitySolTh.sizePolicy().hasHeightForWidth())
        self.pushButtonAdvAnnuitySolTh.setSizePolicy(sizePolicy)
        self.pushButtonAdvAnnuitySolTh.setObjectName(_fromUtf8("pushButtonAdvAnnuitySolTh"))
        self.gridLayout_6.addWidget(self.pushButtonAdvAnnuitySolTh, 0, 0, 1, 2)
        self.labelSolThArea = QtGui.QLabel(self.tabSolTh)
        self.labelSolThArea.setObjectName(_fromUtf8("labelSolThArea"))
        self.gridLayout_6.addWidget(self.labelSolThArea, 2, 0, 1, 1)
        self.lineEditSolThModelFix = QtGui.QLineEdit(self.tabSolTh)
        self.lineEditSolThModelFix.setObjectName(_fromUtf8("lineEditSolThModelFix"))
        self.gridLayout_6.addWidget(self.lineEditSolThModelFix, 2, 1, 1, 1)
        self.tabWidget.addTab(self.tabSolTh, _fromUtf8(""))
        self.tabElHe = QtGui.QWidget()
        self.tabElHe.setObjectName(_fromUtf8("tabElHe"))
        self.gridLayout_7 = QtGui.QGridLayout(self.tabElHe)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.pushButtonAdvAnnuityElHe = QtGui.QPushButton(self.tabElHe)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAdvAnnuityElHe.sizePolicy().hasHeightForWidth())
        self.pushButtonAdvAnnuityElHe.setSizePolicy(sizePolicy)
        self.pushButtonAdvAnnuityElHe.setObjectName(_fromUtf8("pushButtonAdvAnnuityElHe"))
        self.gridLayout_7.addWidget(self.pushButtonAdvAnnuityElHe, 0, 0, 1, 2)
        self.pushButtonAddElHe = QtGui.QPushButton(self.tabElHe)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAddElHe.sizePolicy().hasHeightForWidth())
        self.pushButtonAddElHe.setSizePolicy(sizePolicy)
        self.pushButtonAddElHe.setObjectName(_fromUtf8("pushButtonAddElHe"))
        self.gridLayout_7.addWidget(self.pushButtonAddElHe, 1, 0, 1, 2)
        self.checkBoxFixElHe = QtGui.QCheckBox(self.tabElHe)
        self.checkBoxFixElHe.setObjectName(_fromUtf8("checkBoxFixElHe"))
        self.gridLayout_7.addWidget(self.checkBoxFixElHe, 2, 0, 1, 1)
        self.labelElHeModelFix = QtGui.QLabel(self.tabElHe)
        self.labelElHeModelFix.setObjectName(_fromUtf8("labelElHeModelFix"))
        self.gridLayout_7.addWidget(self.labelElHeModelFix, 3, 0, 1, 1)
        self.lineEditElHeModelFix = QtGui.QLineEdit(self.tabElHe)
        self.lineEditElHeModelFix.setObjectName(_fromUtf8("lineEditElHeModelFix"))
        self.gridLayout_7.addWidget(self.lineEditElHeModelFix, 3, 1, 1, 1)
        self.tabWidget.addTab(self.tabElHe, _fromUtf8(""))
        self.tabPV = QtGui.QWidget()
        self.tabPV.setObjectName(_fromUtf8("tabPV"))
        self.gridLayout_8 = QtGui.QGridLayout(self.tabPV)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.pushButtonAddPV = QtGui.QPushButton(self.tabPV)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAddPV.sizePolicy().hasHeightForWidth())
        self.pushButtonAddPV.setSizePolicy(sizePolicy)
        self.pushButtonAddPV.setObjectName(_fromUtf8("pushButtonAddPV"))
        self.gridLayout_8.addWidget(self.pushButtonAddPV, 1, 0, 1, 2)
        self.pushButtonAdvAnnuityPV = QtGui.QPushButton(self.tabPV)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAdvAnnuityPV.sizePolicy().hasHeightForWidth())
        self.pushButtonAdvAnnuityPV.setSizePolicy(sizePolicy)
        self.pushButtonAdvAnnuityPV.setObjectName(_fromUtf8("pushButtonAdvAnnuityPV"))
        self.gridLayout_8.addWidget(self.pushButtonAdvAnnuityPV, 0, 0, 1, 2)
        self.lineEditPVModelFix = QtGui.QLineEdit(self.tabPV)
        self.lineEditPVModelFix.setObjectName(_fromUtf8("lineEditPVModelFix"))
        self.gridLayout_8.addWidget(self.lineEditPVModelFix, 2, 1, 1, 1)
        self.labelPVArea = QtGui.QLabel(self.tabPV)
        self.labelPVArea.setObjectName(_fromUtf8("labelPVArea"))
        self.gridLayout_8.addWidget(self.labelPVArea, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tabPV, _fromUtf8(""))
        self.tabElSt = QtGui.QWidget()
        self.tabElSt.setObjectName(_fromUtf8("tabElSt"))
        self.gridLayout_9 = QtGui.QGridLayout(self.tabElSt)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.pushButtonAdvAnnuityElSt = QtGui.QPushButton(self.tabElSt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAdvAnnuityElSt.sizePolicy().hasHeightForWidth())
        self.pushButtonAdvAnnuityElSt.setSizePolicy(sizePolicy)
        self.pushButtonAdvAnnuityElSt.setObjectName(_fromUtf8("pushButtonAdvAnnuityElSt"))
        self.gridLayout_9.addWidget(self.pushButtonAdvAnnuityElSt, 0, 0, 1, 2)
        self.pushButtonAddElSt = QtGui.QPushButton(self.tabElSt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAddElSt.sizePolicy().hasHeightForWidth())
        self.pushButtonAddElSt.setSizePolicy(sizePolicy)
        self.pushButtonAddElSt.setObjectName(_fromUtf8("pushButtonAddElSt"))
        self.gridLayout_9.addWidget(self.pushButtonAddElSt, 1, 0, 1, 2)
        self.checkBoxFixElSt = QtGui.QCheckBox(self.tabElSt)
        self.checkBoxFixElSt.setObjectName(_fromUtf8("checkBoxFixElSt"))
        self.gridLayout_9.addWidget(self.checkBoxFixElSt, 2, 0, 1, 1)
        self.labelElStModelFix = QtGui.QLabel(self.tabElSt)
        self.labelElStModelFix.setObjectName(_fromUtf8("labelElStModelFix"))
        self.gridLayout_9.addWidget(self.labelElStModelFix, 3, 0, 1, 1)
        self.lineEditElStModelFix = QtGui.QLineEdit(self.tabElSt)
        self.lineEditElStModelFix.setObjectName(_fromUtf8("lineEditElStModelFix"))
        self.gridLayout_9.addWidget(self.lineEditElStModelFix, 3, 1, 1, 1)
        self.tabWidget.addTab(self.tabElSt, _fromUtf8(""))
        self.buttonBox_2 = QtGui.QDialogButtonBox(self.centralwidget)
        self.buttonBox_2.setGeometry(QtCore.QRect(60, 350, 156, 23))
        self.buttonBox_2.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox_2.setObjectName(_fromUtf8("buttonBox_2"))
        rtrtjrtj.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(rtrtjrtj)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 914, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        rtrtjrtj.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(rtrtjrtj)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        rtrtjrtj.setStatusBar(self.statusbar)

        self.retranslateUi(rtrtjrtj)
        self.tabWidget.setCurrentIndex(9)
        QtCore.QMetaObject.connectSlotsByName(rtrtjrtj)

    def retranslateUi(self, rtrtjrtj):
        rtrtjrtj.setWindowTitle(_translate("rtrtjrtj", "Welcome to the SGT UI", None))
        self.label1.setText(_translate("rtrtjrtj", "Choose technologies that can be present in the system:", None))
        self.CHP1.setText(_translate("rtrtjrtj", "CHP", None))
        self.boiler1.setText(_translate("rtrtjrtj", "Boiler", None))
        self.thermalstorage.setText(_translate("rtrtjrtj", "Thermal Storage", None))
        self.solarthermal.setText(_translate("rtrtjrtj", "Solar Thermal", None))
        self.electricheater1.setText(_translate("rtrtjrtj", "Electric Heater", None))
        self.photovoltaics1.setText(_translate("rtrtjrtj", "Photovoltaics", None))
        self.electricstorage1.setText(_translate("rtrtjrtj", "Electric Storage", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTechnologies), _translate("rtrtjrtj", "Technologies", None))
        self.OutputFolderLineEdit.setPlaceholderText(_translate("rtrtjrtj", "Choose Output folder", None))
        self.btnOutputBrowse.setText(_translate("rtrtjrtj", "Browse..", None))
        self.WeatherDataLineEdit.setPlaceholderText(_translate("rtrtjrtj", "Choose TRY weather file", None))
        self.btnWeathreBrowse.setText(_translate("rtrtjrtj", "Browse..", None))
        self.ElProfileLineEdit.setPlaceholderText(_translate("rtrtjrtj", "Choose electrical profile", None))
        self.btnHeatprofilesBrowse.setText(_translate("rtrtjrtj", "Browse..", None))
        self.HProfileLineEdit.setPlaceholderText(_translate("rtrtjrtj", "Choose heat profile", None))
        self.btnElProfileBrowse.setText(_translate("rtrtjrtj", "Browse..", None))
        self.radioButton.setText(_translate("rtrtjrtj", "Hourly excels required?", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFolders), _translate("rtrtjrtj", "Source and destination Folders", None))
        self.labelElPrice.setText(_translate("rtrtjrtj", "Electricity price", None))
        self.labelGprice.setText(_translate("rtrtjrtj", "Gas price", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabGDetails), _translate("rtrtjrtj", "General Details", None))
        self.labelCHPModelFix.setText(_translate("rtrtjrtj", "Choose Model", None))
        self.pushButtonAddCHP.setText(_translate("rtrtjrtj", "Add/Modify Models in database", None))
        self.pushButtonAdvAnnuityCHP.setText(_translate("rtrtjrtj", "Modify Annuity Factors", None))
        self.radioButtonContCHP.setText(_translate("rtrtjrtj", "Continuous CHP", None))
        self.radioButtonONOFFCHP.setText(_translate("rtrtjrtj", "ON/OFF CHP", None))
        self.labelCHPFIT.setText(_translate("rtrtjrtj", "CHP FIT in Euro Cents", None))
        self.radioButtonModCHP.setText(_translate("rtrtjrtj", "Modulating CHP", None))
        self.checkBoxFixCHP.setText(_translate("rtrtjrtj", "Fix CHP model", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCHP), _translate("rtrtjrtj", "CHP", None))
        self.pushButtonAddBoiler.setText(_translate("rtrtjrtj", "Add/Modify Models in database", None))
        self.pushButtonAdvAnnuityBoiler.setText(_translate("rtrtjrtj", "Modify Annuity Factors", None))
        self.labelBoilerModelFix.setText(_translate("rtrtjrtj", "Choose Model", None))
        self.checkBox.setText(_translate("rtrtjrtj", "Fix Boiler model", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBoiler), _translate("rtrtjrtj", "Boiler", None))
        self.pushButtonAdvAnnuityThSt.setText(_translate("rtrtjrtj", "Modify Annuity Factors", None))
        self.pushButtonAddThSt.setText(_translate("rtrtjrtj", "Add/Modify Models in database", None))
        self.checkBoxFixThSt.setText(_translate("rtrtjrtj", "Fix Thermal Storage model", None))
        self.labelThStModelFix.setText(_translate("rtrtjrtj", "Choose Model", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabThSt), _translate("rtrtjrtj", "Thermal Storage", None))
        self.pushButtonAddSolTh.setText(_translate("rtrtjrtj", "Add/Modify Models in database", None))
        self.pushButtonAdvAnnuitySolTh.setText(_translate("rtrtjrtj", "Modify Annuity Factors", None))
        self.labelSolThArea.setText(_translate("rtrtjrtj", "Area", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSolTh), _translate("rtrtjrtj", "Solar Thermal", None))
        self.pushButtonAdvAnnuityElHe.setText(_translate("rtrtjrtj", "Modify Annuity Factors", None))
        self.pushButtonAddElHe.setText(_translate("rtrtjrtj", "Add/Modify Models in database", None))
        self.checkBoxFixElHe.setText(_translate("rtrtjrtj", "Fix Electric Heater model", None))
        self.labelElHeModelFix.setText(_translate("rtrtjrtj", "Choose Model", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabElHe), _translate("rtrtjrtj", "Electric Heater", None))
        self.pushButtonAddPV.setText(_translate("rtrtjrtj", "Add/Modify Models in database", None))
        self.pushButtonAdvAnnuityPV.setText(_translate("rtrtjrtj", "Modify Annuity Factors", None))
        self.labelPVArea.setText(_translate("rtrtjrtj", "PV Area", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPV), _translate("rtrtjrtj", "PV", None))
        self.pushButtonAdvAnnuityElSt.setText(_translate("rtrtjrtj", "Modify Annuity Factors", None))
        self.pushButtonAddElSt.setText(_translate("rtrtjrtj", "Add/Modify Models in database", None))
        self.checkBoxFixElSt.setText(_translate("rtrtjrtj", "Fix Electric Storage model", None))
        self.labelElStModelFix.setText(_translate("rtrtjrtj", "Choose Model", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabElSt), _translate("rtrtjrtj", "Electric Storage", None))

