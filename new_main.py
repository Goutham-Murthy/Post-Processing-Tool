from PySide import QtGui
from PySide import QtCore
import sys
import NewGUI
import loaddata
import os
import preprocessingtool
import annuity_window
import database
import model_window
import ast


class ControlMainWindow(QtGui.QMainWindow):
    """
    Class for GUI implementation

    Attributes:
        ui: User interface inherited from UiMainWindow in gui.py
        th_technologies: List of thermal technologies to be analysed.
        el_technologies: List of electrical technologies to be analysed.
    Extends:
        QtGui.QtMainWindow
    """
    def __init__(self, parent=None):
        """
        Constructor class for ControlMainWindow
        :param: none.
        :return: none.
        """
        super(ControlMainWindow, self).__init__(parent)
        self.ui = NewGUI.UiMainWindow()
        self.ui.setup_gui(self)
        self.factors = {
                        'CHP': (15.0, 10.0, 1.0, 1.0, 1.07, 1.03),
                        'B': (18.0, 10.0, 1.5, 1.5, 1.07, 1.03),
                        'ThSt': (15.0, 0.0, 1.0, 2.0, 1.07, 1.03),
                        'SolTh': (20.0, 5.0, 1.0, 0.5, 1.07, 1.03),
                        'ElHe': (15.0, 5.0, 1.0, 1.0, 1.07, 1.03),
                        'PV': (25.0, 5.0, 1.0, 0.5, 1.07, 1.03),
                        'ElSt': (5.0, 0.0, 1.0, 0.5, 1.07, 1.03)
                        }

        # Connect statements for the Tab1: technologies selection
        self.ui.check_box_chp.clicked.connect(self.disable_tab)
        self.ui.check_box_boiler.clicked.connect(self.disable_tab)
        self.ui.check_box_thst.clicked.connect(self.disable_tab)
        self.ui.check_box_solth.clicked.connect(self.disable_tab)
        self.ui.check_box_elhe.clicked.connect(self.disable_tab)
        self.ui.check_box_pv.clicked.connect(self.disable_tab)
        self.ui.check_box_elst.clicked.connect(self.disable_tab)

        # Connect statements for Tab2: Folder selection
        self.ui.buttonBox.accepted.connect(self.process_data)
        self.ui.buttonBox.rejected.connect(self.reset_all)
        self.ui.btnOutputBrowse.clicked.connect(self.get_output_folder)
        self.ui.btnWeathreBrowse.clicked.connect(self.get_weather_file)
        self.ui.btnHeatprofilesBrowse.clicked.connect(self.get_heat_profiles)
        self.ui.btnElProfileBrowse.clicked.connect(self.get_electrical_profiles)

        # Connect statements for CHP tab
        self.ui.pushButtonAdvAnnuityCHP.clicked.connect(self.get_annuity_factors)
        self.ui.pushButtonAddCHP.clicked.connect(self.add_model)

        # Connect statements for boiler tab
        self.ui.pushButtonAdvAnnuityBoiler.clicked.connect(self.get_annuity_factors)
        self.ui.pushButtonAddCHP.clicked.connect(self.add_model)

        # Connect statements for thermal storage tab
        self.ui.pushButtonAdvAnnuityThSt.clicked.connect(self.get_annuity_factors)
        self.ui.pushButtonAddCHP.clicked.connect(self.add_model)

        # Connect statements for Solar thermal tab
        self.ui.pushButtonAdvAnnuitySolTh.clicked.connect(self.get_annuity_factors)

        # Connect statements for electric heater tab
        self.ui.pushButtonAdvAnnuityElHe.clicked.connect(self.get_annuity_factors)

        # Connect statements for PV tab
        self.ui.pushButtonAdvAnnuityPV.clicked.connect(self.get_annuity_factors)

        # Connect statements for electric storage tab
        self.ui.pushButtonAdvAnnuityElSt.clicked.connect(self.get_annuity_factors)

        self.th_technologies = []
        self.el_technologies = []

    def add_model(self):
        index = self.ui.tabWidget.currentIndex()
        technology = self.get_technology_from_index(index)
        if technology is 'CHP':
            db = database.CHP_database
        elif technology is 'B':
            db = database.B_database
        elif technology is 'ThSt':
            db = database.ThSt_database
        form = QtGui.QDialog()
        ui_form = model_window.Ui_Dialog()
        ui_form.setupUi(form, db)
        form.exec_()
        if technology is 'CHP':
            print ui_form.textEdit.toPlainText()
            database.CHP_database = ast.literal_eval(ui_form.textEdit.toPlainText())
        elif technology is 'B':
            database.B_database = ast.literal_eval(ui_form.textEdit.toPlainText())
        elif technology is 'ThSt':
            database.ThSt_database = ast.literal_eval(ui_form.textEdit.toPlainText())

    def get_annuity_factors(self):
        index = self.ui.tabWidget.currentIndex()
        technology = self.get_technology_from_index(index)
        form = QtGui.QDialog()
        ui_form = annuity_window.Ui_Dialog()
        ui_form.setupUi(form, self.factors[technology])
        form.exec_()
        self.factors[technology] = [float(ui_form.lineEditDePe.text()), float(ui_form.lineEditEffop.text()),
                                    float(ui_form.lineEditfwins.text()), float(ui_form.lineEditfinst.text()),
                                    float(ui_form.lineEditq.text()), float(ui_form.lineEditr.text())]

    @staticmethod
    def get_technology_from_index(index):
        technology = ''
        if index == 3:
            technology = 'CHP'
        elif index == 4:
            technology = 'B'
        elif index == 5:
            technology = 'ThSt'
        elif index == 6:
            technology = 'SolTh'
        elif index == 7:
            technology = 'ElHe'
        elif index == 8:
            technology = 'PV'
        elif index == 9:
            technology = 'ElSt'
        return technology

    def disable_tab(self):
        if self.ui.check_box_chp.isChecked():
            self.ui.tabWidget.setTabEnabled(3, True)
        else:
            self.ui.tabWidget.setTabEnabled(3, False)

        if self.ui.check_box_boiler.isChecked():
            self.ui.tabWidget.setTabEnabled(4, True)
        else:
            self.ui.tabWidget.setTabEnabled(4, False)

        if self.ui.check_box_thst.isChecked():
            self.ui.tabWidget.setTabEnabled(5, True)
        else:
            self.ui.tabWidget.setTabEnabled(5, False)

        if self.ui.check_box_solth.isChecked():
            self.ui.tabWidget.setTabEnabled(6, True)
        else:
            self.ui.tabWidget.setTabEnabled(6, False)

        if self.ui.check_box_elhe.isChecked():
            self.ui.tabWidget.setTabEnabled(7, True)
        else:
            self.ui.tabWidget.setTabEnabled(7, False)

        if self.ui.check_box_pv.isChecked():
            self.ui.tabWidget.setTabEnabled(8, True)
        else:
            self.ui.tabWidget.setTabEnabled(8, False)

        if self.ui.check_box_elst.isChecked():
            self.ui.tabWidget.setTabEnabled(9, True)
        else:
            self.ui.tabWidget.setTabEnabled(9, False)

    def process_data(self):
        """
        Process data using a worker thread.

        :param: none
        :return: none
        """
        # Get the list of thermal and electrical technologies to be analyzed.
        self.get_technologies()
        self.worker_thread = WorkerThread(output_folder_name=self.ui.OutputFolderLineEdit.text(),
                                          weather_file=self.ui.WeatherDataLineEdit.text(),
                                          th_technologies=self.th_technologies,
                                          el_technologies=self.el_technologies,
                                          heat_profiles_file=self.ui.HProfileLineEdit.text(),
                                          electrical_profiles_file=self.ui.ElProfileLineEdit.text(),
                                          hourly_excels=self.hourly_excels)
        self.connect(self.worker_thread, QtCore.SIGNAL("threadDone(QString)"), self.test_func,
                     QtCore.Qt.DirectConnection)
        self.worker_thread.start()

    @staticmethod
    def test_func(message):
        """
        Method to print success message to the console.

        :param message: String to be printed
        :return: none
        """
        print message

    def get_technologies(self):
        """
        Makes the list of thermal and electrical technologies that can be present in the system.

        :param: none
        :return: none
        """
        if self.ui.check_box_chp.isChecked():
            self.th_technologies.append('CHP')
            self.el_technologies.append('CHP')
        if self.ui.check_box_boiler.isChecked():
            self.th_technologies.append('B')
        if self.ui.check_box_thst.isChecked():
            self.th_technologies.append('ThSt')
        if self.ui.check_box_solth.isChecked():
            self.th_technologies.append('SolTh')
        if self.ui.check_box_elhe.isChecked():
            self.th_technologies.append('ElHe')
        if self.ui.check_box_elst.isChecked():
            self.el_technologies.append('ElSt')
        if self.ui.check_box_pv.isChecked():
            self.el_technologies.append('PV')
        print self.th_technologies, self.el_technologies

        if self.ui.rbtn_hourly_excels.isChecked():
            self.hourly_excels = True
        else:
            self.hourly_excels = False

    def reset_all(self):
        """
        Resets all the object in the user interface when user clicks cancel.

        :param: none
        :return: none
        """
        self.ui.check_box_chp.setChecked(False)
        self.ui.check_box_boiler.setChecked(False)
        self.ui.check_box_thst.setChecked(False)
        self.ui.check_box_solth.setChecked(False)
        self.ui.check_box_elhe.setChecked(False)
        self.ui.check_box_pv.setChecked(False)
        self.ui.check_box_elst.setChecked(False)
        self.ui.OutputFolderLineEdit.clear()
        self.ui.WeatherDataLineEdit.clear()
        self.ui.ElProfileLineEdit.clear()
        self.ui.HProfileLineEdit.clear()
        self.ui.rbtn_hourly_excels.setChecked(False)
        for index in range(3, 10):
            self.ui.tabWidget.setTabEnabled(index, False)

    def get_output_folder(self):
        """
        Get the folder where the output files will be stored

        :param: none
        :return: none
        """
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        self.output_folder_name = dialog.getExistingDirectory(dialog, 'Choose Directory', os.path.curdir)
        self.ui.OutputFolderLineEdit.setText(self.output_folder_name)
        return

    def get_weather_file(self):
        """
        Get path to weather file

        :param: none
        :return: none
        """
        dialog = QtGui.QFileDialog()
        # self.weather_file_location = dialog.getExistingDirectory(dialog, 'Choose Directory', os.path.curdir)
        self.weather_file, discard = dialog.getOpenFileName(caption="Choose TRY weather File",
                                                            filter=".csv files(*.csv)")
        self.ui.WeatherDataLineEdit.setText(self.weather_file)
        return

    def get_electrical_profiles(self):
        """
        Get path to electrical profiles file

        :param: none
        :return: none
        """
        dialog = QtGui.QFileDialog()
        self.electrical_profiles_file, \
            discard = dialog.getOpenFileName(caption="Choose file with electrical profiles",
                                             filter="Excel files(*.xlsx *.xls)")
        self.ui.ElProfileLineEdit.setText(self.electrical_profiles_file)
        return

    def get_heat_profiles(self):
        """
        Get the path to heat profiles file

        :param: none
        :return: none
        """
        dialog = QtGui.QFileDialog()
        # self.weather_file_location = dialog.getExistingDirectory(dialog, 'Choose Directory', os.path.curdir)
        self.heat_profiles_file, discard = dialog.getOpenFileName(caption="Choose file with heat profiles",
                                                                  filter="Excel files(*.xlsx *.xls)",
                                                                  )
        self.ui.HProfileLineEdit.setText(self.heat_profiles_file)
        return


class WorkerThread(QtCore.QThread):
    """
    Class representing the worker thread for the GUI. All the processing of the data happens here.

    Attributes:
        electrical_profiles_file: Path to the file containing electrical profiles
        heat_profiles_file: Path to the file containing heat profiles
        output_folder_name: Path to the folder where the output files have to be created
        weather_file: Path to the file containing weather data
        th_technologies: List containing thermal technologies which can be present in the system
        el_technologies: List containing electrical technologies which can be present in the system
        hourly_excels: True if hourly excels are required. False otherwise.
    """
    def __init__(self, output_folder_name, weather_file, heat_profiles_file, electrical_profiles_file, th_technologies,
                 el_technologies, hourly_excels):
        """
        Constructor method for worker thread

        :param output_folder_name: Path to the folder where the output files have to be created
        :param weather_file: Path to the file containing weather data
        :param heat_profiles_file: Path to the file containing heat profiles
        :param electrical_profiles_file: Path to the file containing electrical profiles
        :param th_technologies: List containing thermal technologies which can be present in the system
        :param el_technologies: List containing electrical technologies which can be present in the system
        :param hourly_excels: True if hourly excels are required. False otherwise.
        :return: none.
        """
        super(WorkerThread, self).__init__()
        self.electrical_profiles_file = electrical_profiles_file
        self.heat_profiles_file = heat_profiles_file
        self.output_folder_name = output_folder_name
        self.weather_file = weather_file
        self.th_technologies = th_technologies
        self.el_technologies = el_technologies
        self.hourly_excels = hourly_excels

    def run(self):
        """
        Process the data. Generate cases and calculate using the pre-processing tool

        :param: none
        :return: none
        """
        # Load weather data
        global_radiation = loaddata.get_weather_data(self.weather_file)
        # Load heat profiles
        heat_profiles, building_ids = loaddata.get_heat_profiles(self.heat_profiles_file)
        # Load electrical profiles
        el_profiles, building_ids = loaddata.get_el_profiles(self.electrical_profiles_file)

        # For each building call the tool with corresponding parameter
        for i in range(0, len(building_ids)):
            building_id = building_ids[i]
            thermal_profile = heat_profiles[i]
            electrical_profile = el_profiles[i]
            building_number = preprocessingtool.PreProcessingTool(building_id=building_id,
                                                                  thermal_profile=thermal_profile,
                                                                  electrical_profile=electrical_profile,
                                                                  global_radiation=global_radiation,
                                                                  th_technologies=self.th_technologies,
                                                                  el_technologies=self.el_technologies,
                                                                  location=self.output_folder_name,
                                                                  hourly_excels=self.hourly_excels)
            building_number.generate_cases()

        # Emit signal after processing is over
        self.emit(QtCore.SIGNAL("threadDone(QString)"), "Yahoo!! All done")

class MyTable(QtGui.QTableWidget):
    def __init__(self, dict):
        QtGui.QTableWidget.__init__(self)
        self.data = dict
        self.setmydata()

    def setmydata(self):
        n = 0
        for key in self.data:
            m = 0
            for item in self.data[key]:
                newitem = QtGui.QTableWidgetItem(item)
                self.setItem(m, n, newitem)
                m += 1
            n += 1


# Main method
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())

os.chdir("D:/aja-gmu/Simulation_Files")
