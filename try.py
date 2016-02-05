from PySide import QtGui
from PySide import QtCore
import sys
import ahoi
import loaddata
import os
import preprocessingtool


class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = ahoi.UiMainWindow()
        self.ui.setup_gui(self)
        self.ui.buttonBox.accepted.connect(self.process_data)
        self.ui.buttonBox.rejected.connect(self.reset_all)
        
        self.ui.btn_output_folder.clicked.connect(self.get_output_folder)
        self.ui.btn_weather_file.clicked.connect(self.get_weather_file)
        self.ui.btn_heat_profiles.clicked.connect(self.get_heat_profiles)
        self.ui.btn_electrical_profiles.clicked.connect(self.get_electrical_profiles)
        self.th_technologies = []
        self.el_technologies = []

    def process_data(self):
        self.get_technologies()
        self.worker_thread = WorkerThread(output_folder_name=self.output_folder_name,
                                          weather_file=self.weather_file,
                                          th_technologies=self.th_technologies,
                                          el_technologies=self.el_technologies,
                                          heat_profiles_file=self.heat_profiles_file,
                                          electrical_profiles_file=self.electrical_profiles_file,
                                          hourly_excels=self.hourly_excels)
        self.connect(self.worker_thread, QtCore.SIGNAL("threadDone(QString)"), self.test_func, QtCore.Qt.DirectConnection)
        self.worker_thread.start()

    def test_func(self, message):
        print message

    def get_technologies(self):
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
        self.ui.check_box_chp.setChecked(False)
        self.ui.check_box_boiler.setChecked(False)
        self.ui.check_box_thst.setChecked(False)
        self.ui.check_box_solth.setChecked(False)
        self.ui.check_box_elhe.setChecked(False)
        self.ui.check_box_pv.setChecked(False)
        self.ui.check_box_elst.setChecked(False)
        self.ui.line_edit_output_folder.clear()
        self.ui.line_edit_weather.clear()
        self.ui.line_edit_electrical_profiles.clear()
        self.ui.line_edit_heat_profiles.clear()
        self.ui.rbtn_hourly_excels.setChecked(False)

    def get_output_folder(self):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        self.output_folder_name = dialog.getExistingDirectory(dialog, 'Choose Directory', os.path.curdir)
        self.ui.line_edit_output_folder.insert(self.output_folder_name)
        return

    def get_weather_file(self):
        dialog = QtGui.QFileDialog()
        # self.weather_file_location = dialog.getExistingDirectory(dialog, 'Choose Directory', os.path.curdir)
        self.weather_file, discard = dialog.getOpenFileName(caption="Choose TRY weather File",
                                                                 filter=".csv files(*.csv)")
        self.ui.line_edit_weather.insert(self.weather_file)
        return

    def get_electrical_profiles(self):
        dialog = QtGui.QFileDialog()
        self.electrical_profiles_file, \
            discard = dialog.getOpenFileName(caption="Choose file with electrical profiles",
                                             filter="Excel files(*.xlsx *.xls)")
        self.ui.line_edit_electrical_profiles.insert(self.electrical_profiles_file)
        return

    def get_heat_profiles(self):
        dialog = QtGui.QFileDialog()
        # self.weather_file_location = dialog.getExistingDirectory(dialog, 'Choose Directory', os.path.curdir)
        self.heat_profiles_file, discard = dialog.getOpenFileName(caption="Choose file with heat profiles",
                                                                  filter="Excel files(*.xlsx *.xls)",
                                                                  )
        self.ui.line_edit_heat_profiles.insert(self.heat_profiles_file)
        return


class WorkerThread(QtCore.QThread):
    def __init__(self, output_folder_name, weather_file, heat_profiles_file, electrical_profiles_file, th_technologies,
                 el_technologies, hourly_excels):
        super(WorkerThread, self).__init__()
        #self.done_signal = QtCore.Signal(str)
        self.electrical_profiles_file = electrical_profiles_file
        self.heat_profiles_file = heat_profiles_file
        self.output_folder_name = output_folder_name
        self.weather_file = weather_file
        self.th_technologies = th_technologies
        self.el_technologies = el_technologies
        self.hourly_excels = hourly_excels

    def run(self):
        global_radiation = loaddata.get_weather_data(self.weather_file)
        heat_profiles, building_ids = loaddata.get_heat_profiles(self.heat_profiles_file)
        el_profiles, building_ids = loaddata.get_el_profiles(self.electrical_profiles_file)

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
        print "yahoo!!"
        self.emit(QtCore.SIGNAL("threadDone(QString)"), "Yahoo!! All done")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())

os.chdir("D:/aja-gmu/Simulation_Files")
