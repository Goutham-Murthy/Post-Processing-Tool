# -*- coding: utf-8 -*-
from xlrd import open_workbook
from xlutils.copy import copy
import os
import itertools
import xlsxwriter
import shutil
import CHP
import boiler
import electricheater
import thermalstorage
import solarthermal
import photovoltaics
import electricalstorage
# import heatpump
import electricalgrid
import database


class PreProcessingTool:
    """PreProcessingTool

    Attributes:
        building_id         : Building ID of the particular building.
        thermal_profile     : Thermal profile of the building.
        electrical_profile  : Electrical profile of the building.
        global_radiation    : Hourly global radiation values.
        th_technologies     : List of the thermal technologies to be considered.
        el_technologies     : List of the electrical technologies to be considered.
        max_el_technologies : Maximum number of electrical technologies to be considered.
        min_el_technologies : Minimum number of electrical technologies to be considered.
        max_th_technologies : Maximum number of thermal technologies to be considered.
        min_th_technologies : Minimum number of thermal technologies to be considered.
        hourly_excels       : Hourly excels required? True or False.
        location            : Address of the folder where the output folder is to be created.
        maxr_th_power       : Maximum thermal capacity of the CHP in the presence of a peak load device.
                              Is calculated according to maximum rectangle method.
        peak_th_power       : Peak thermal capacity needed to meet the demands of the consumer.
        KPI                 : KPI array containing the output data for the tool.
        OnOffCHP            : Instance of the CHP class with ON/OFF operating strategy.
        B                   : Instance of boiler class
        ElHe                : Instance of the electric heater class.
        SolTh               : Instance of the solar thermal class.
        PV                  : Instance of the PV class.
        ThSt                : Instance of the thermal storage class.
        ElSt                : Instance of the electric storage class.
        ElGrid              : Instance of the electric grid glass.
    """

    def __init__(self, building_id,
                 thermal_profile,
                 electrical_profile,
                 global_radiation,
                 th_technologies=None,
                 el_technologies=None,
                 # max_el_technologies=3,
                 # min_el_technologies=1,
                 # max_th_technologies=2,
                 # min_th_technologies=1,
                 hourly_excels=True,
                 location='D:/aja-gmu/Simulation_Files/Output'):
        """
        Constructor class for the pre-processing tool

        :param building_id: Building ID of the particular building.
        :param thermal_profile: Thermal profile of the building.
        :param electrical_profile: Electrical profile of the building.
        :param global_radiation: Hourly global radiation values.
        :param th_technologies: List of the thermal technologies to be onsidered.
        :param el_technologies: List of the electrical technologies to be considered.
        :param hourly_excels: Hourly excels required? True or False.
        :param location: Address of the folder where the output folder is to be created.
        :return: none
        """
        self.building_id = building_id
        self.thermal_profile = thermal_profile
        self.electrical_profile = electrical_profile
        self.global_radiation = global_radiation
        if th_technologies is None:
            self.th_technologies = ['CHP', 'SolTh', 'ThSt', 'B']
        else:
            self.th_technologies = th_technologies
        if el_technologies is None:
            self.el_technologies = ['CHP', 'PV', 'ElSt']
        else:
            self.el_technologies = el_technologies
        self.max_el_technologies = len(self.el_technologies)
        self.min_el_technologies = 0
        self.max_th_technologies = len(self.th_technologies)
        self.min_th_technologies = 0
        self.hourly_excels = hourly_excels
        self.location = location
        # Initialising other variables
        self.maxr_th_power, self.maxr_hours = self.get_maxr(thermal_profile)
        self.peak_th_power = max(thermal_profile)
        self.KPI = []

    def generate_cases(self):
        """
        This is where the magic happens. Generates the scenarios with different energy supply systems and does all the
        thermal and electrical calculations.

        :param: none
        :return: none
        """

        # change to the output folder
        os.chdir(self.location)

        # Make the building folder if it does not exist
        if not os.path.exists(self.location+'/'+self.building_id):
            os.makedirs(self.location+'/'+self.building_id)

        # Change to the building folder
        os.chdir(self.location+'/'+self.building_id)

        # Delete all the old files and folders in the building directory
        for the_file in os.listdir(self.location+'/'+self.building_id):
            file_path = os.path.join(self.location+'/'+self.building_id,
                                     the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        # Total number of technologies
        technologies = list(set(self.th_technologies).
                            union(self.el_technologies))

        # ---------------------------------------------------------------------
        # Iterating from 1 to the maximum number of technologies
        for number in range(1, len(technologies)+1):

            # Change to the building folder
            os.chdir(self.location+'/'+self.building_id)
            # Make separate sub-folders depending on the number of technologies presenting the system
            if (self.max_el_technologies + self.max_th_technologies-1 >= number >= self.min_el_technologies +
                    self.min_th_technologies-1) and self.hourly_excels:

                # make sub-folders for different number of technologies
                if not os.path.exists(str(number)+'technologies'):
                    os.makedirs(str(number)+'technologies')

                # Changing to the required directory in output directory
                os.chdir('./'+str(number)+'technologies')

            # -----------------------------------------------------------------
            # Iterating through the various possible combinations.
            for system in itertools.combinations(technologies, number):

                # Proceed further only if there is CHP present in the system
                if 'CHP' in system:

                    # Proceed further is the number of technologies in the system are suitable
                    if (self.max_el_technologies >= len(set(system) &
                                                        set(self.el_technologies)) >= self.min_el_technologies and
                            self.max_th_technologies >= len(set(system) &
                                                            set(self.th_technologies)) >= self.min_th_technologies):

                        print '\n\n====================System-', system

                        # ----------------------------------------------------------------------------------------------
                        # Create excel for system.
                        # Create excel with the corresponding name
                        if self.hourly_excels:
                            excel = xlsxwriter.Workbook(self.get_system_name(system) + '.xls')

                            # Generating different thermal and electrical priorities
                            for th_order in itertools.permutations(set(system) & set(self.th_technologies)):
                                for el_order in itertools.permutations(set(system) & set(self.el_technologies)):
                                    # For each combo of thermal and electrical priority add a worksheet
                                    excel.add_worksheet(self.get_priority(th_order)+','+self.get_priority(el_order))
                            excel.close()

                        # ----------------------------------------------------------------------------------------------
                        # Calculations.
                        # Generating different thermal and electrical priorities
                        for th_order in itertools.permutations(set(system) & set(self.th_technologies)):
                            for el_order in itertools.permutations(set(system) & set(self.el_technologies)):

                                # Spells for the magic to happen
                                self.initialise_technologies(system)  # Initialise the units of the system
                                demand_satisfied = self.perform_calculations(th_order, el_order)  # Perform calculations
                                if demand_satisfied:  # If system is successful in meeting the thermal demand
                                    self.update_kpi(system, th_order, el_order)  # Update the KPI variable.
                                    if self.hourly_excels:  # If hourly excels are required write data into them
                                        self.write_hourly_excel(self.get_system_name(system)+'.xls', th_order, el_order)
        self.write_kpi_excel()  # After everything, write the KPI excel
        return

    def update_kpi(self, system, th_order, el_order):
        """
        Updates the KPI variable and stores information about the different systems and corresponding thermal and
        electrical priorities.

        :param system: List containing the technologies in the system
        :param th_order: Thermal priority
        :param el_order: Electrical priority
        :return: none
        """
        total_annuity = 0
        total_emissions = 0
        total_pef = 0
        sc_percentage = 0

        # calculate annuity and emissions for the technologies present in the system.
        if 'CHP' in system:
            if 'ThSt' in system:
                self.OnOffCHP.set_annuity(storage=True)
            else:
                self.OnOffCHP.set_annuity()
            self.OnOffCHP.set_emissions()
            total_annuity += self.OnOffCHP.annuity
            total_emissions += self.OnOffCHP.emissions

        if 'B' in system:
            self.B.set_annuity()
            self.B.set_emissions()
            total_annuity += self.B.annuity
            total_emissions += self.B.emissions

        if 'ElHe' in system:
            self.ElHe.set_annuity()
            self.ElHe.set_emissions()
            total_annuity += self.ElHe.annuity
            total_emissions += self.ElHe.emissions

        if 'ThSt' in system:
            self.ThSt.set_annuity()
            total_annuity += self.ThSt.annuity

        if 'SolTh' in system:
            self.SolTh.set_annuity()
            total_annuity += self.SolTh.annuity

        if 'PV' in system:
            self.PV.set_annuity()
            self.PV.set_emissions()
            total_annuity += self.PV.annuity
            total_emissions += self.PV.emissions

        # Append to the KPI variable.
        self.KPI.append([self.get_system_name(system),
                         self.get_priority(th_order),
                         self.get_priority(el_order),
                         total_annuity,
                         total_emissions,
                         total_pef,
                         self.ThSt.losses if 'ThSt' in system else 0,
                         self.OnOffCHP.th_capacity if 'CHP' in system else 0,
                         self.OnOffCHP.heat_yearly if 'CHP' in system else 0,
                         0,
                         0,
                         self.B.th_capacity if 'B' in system else 0,
                         self.B.heat_yearly if 'B' in system else 0,
                         self.ThSt.th_capacity if 'ThSt' in system else 0,
                         self.ThSt.heat_stored[8760] if 'ThSt' in system else 0,
                         self.SolTh.area if 'SolTh' in system else 0,
                         self.SolTh.heat_yearly if 'SolTh' in system else 0,
                         self.ElHe.th_capacity if 'ElHe' in system else 0,
                         self.ElHe.heat_yearly if 'ElHe' in system else 0,
                         self.PV.area if 'PV' in system else 0,
                         self.PV.electricity_yearly if 'PV' in system else 0,
                         self.OnOffCHP.annuity if 'CHP' in system else 0,
                         self.B.annuity if 'B' in system else 0,
                         self.ThSt.annuity if 'ThSt' in system else 0,
                         self.SolTh.annuity if 'SolTh' in system else 0,
                         self.ElHe.annuity if 'ElHe' in system else 0,
                         self.PV.annuity if 'PV' in system else 0,
                         sc_percentage])

    @staticmethod
    def get_maxr(thermal_profile):
        """
        Returns capacity calculated according to maximum rectangle method. Is used in dimensioning the CHP unit in the
        presence of a peak load device.

        :param thermal_profile: Thermal profile of the building.
        :return: none
        """
        # Sort thermal demand in decreasing order for the load distribution
        # curve
        thermal_profile = sorted(thermal_profile, reverse=True)

        # Finding the maximum rectangle
        q_yearly = 0
        maxr = 0
        hours = 0
        for k in range(0, 8760):
            q_yearly += thermal_profile[k]
            if k*thermal_profile[k] > maxr:
                maxr = k*thermal_profile[k]
                hours = k
        # print maxr, hours, thermal_profile[hours]
        return thermal_profile[hours], hours

    def initialise_technologies(self, system):
        """
        Initialise required technologies according to the system passed to it.

        :param system: List of technologies present in the system.
        :return: none
        """
        # ---------------------------------------------------------------------
        # CHP
        # If CHP is present, it will check for a peak load device. If peak load
        # device is present, CHP is sized according to maximum rectangle
        # method. Otherwise it is sized according to peak thermal load.
        if 'CHP' in system and 'ElHe' not in system and 'B'not in system:
            self.OnOffCHP = CHP.OnOffCHP(database.get_chp_capacity(self.peak_th_power))
        if 'CHP' in system and ('ElHe' in system or 'B' in system):
            self.OnOffCHP = CHP.OnOffCHP(database.get_chp_capacity(self.maxr_th_power))

        # ---------------------------------------------------------------------
        # Boiler
        # If boiler is present, dimension it to peak thermal demand
        if 'B' in system:
            self.B = boiler.Boiler(database.get_b_capacity(self.peak_th_power))

        # ---------------------------------------------------------------------
        # Electric Resistance Heater
        # If electric heater is present, dimension it to peak thermal demand
        if 'ElHe' in system:
            self.ElHe = electricheater.ElectricHeater('Electric Heater Model',
                                                      database.get_elhe_capacity(self.peak_th_power))

        # ---------------------------------------------------------------------
        # Thermal Storage
        # If thermal storage is present, dimension it according to CHP
        # capacity.
        if 'ThSt' in system:
            self.ThSt = thermalstorage.ThermalStorage(database.get_thst_capacity(3*self.OnOffCHP.th_capacity))

        # ---------------------------------------------------------------------
        # Solar Thermal
        # If Solar thermal is present, dimension according to roof area
        if 'SolTh' in system and 'PV' not in system:
            self.SolTh = solarthermal.SolarThermal('Buderus SKS 5.0-s', database.get_solth_capacity(10),
                                                   self.global_radiation)
        if 'SolTh' in system and 'PV' in system:
            self.SolTh = solarthermal.SolarThermal('Buderus SKS 5.0-s', database.get_solth_capacity(5),
                                                   self.global_radiation)

        # ---------------------------------------------------------------------
        # Photovoltaics
        # If PV is present, dimension according to roof area
        if 'PV' in system and 'SolTh' not in system:
            self.PV = photovoltaics.Photovoltaics('Buderus aleo s19', database.get_pv_capacity(10),
                                                  self.global_radiation)
        if 'PV' in system and 'SolTh' in system:
            self.PV = photovoltaics.Photovoltaics('Buderus aleo s19', database.get_pv_capacity(5),
                                                  self.global_radiation)

        # ---------------------------------------------------------------------
        # Electrical Storage
        # Dimension logic to be implemented
        if 'ElSt' in system:
            self.ElSt = electricalstorage.ElectricalStorage('Model', 1000, 1)

        # ---------------------------------------------------------------------
        # HeatPump

        # ---------------------------------------------------------------------
        # Electrical Grid
        # Initialising electrical grid
        self.ElGrid = electricalgrid.ElectricalGrid()

        return

    def perform_calculations(self, th_order, el_order):
        """
        Performs the thermal and electrical calculations.

        :param th_order: Thermal priority list
        :param el_order: Electrical priority list
        :return: none
        """
        print th_order, el_order

        for i in range(0, 8760):
            q_hourly = self.thermal_profile[i]  # Hourly thermal demand
            if 'ThSt' in th_order:  # Thermal loss in the thermal storage
                self.ThSt.apply_losses(i)

            # Meeting the thermal demand
            for technology in th_order:
                if technology is 'CHP' and q_hourly > 0:
                    if 'ThSt' in th_order:
                        q_hourly = self.OnOffCHP.get_heat(q_hourly, i,
                                                          self.ThSt)
                    else:
                        q_hourly = self.OnOffCHP.get_heat(q_hourly, i)
                if technology is 'B' and q_hourly > 0:
                    q_hourly = self.B.get_heat(q_hourly, i)
                if technology is 'ElHe' and q_hourly > 0:
                    q_hourly = self.ElHe.get_heat(q_hourly, i)
                if technology is 'ThSt' and q_hourly > 0:
                    q_hourly = self.ThSt.get_heat(q_hourly, i)
                # if technology is 'HP' and q_hourly > 0:
                #   q_hourly = self.HP.get_heat(q_hourly, i)
                if technology is 'SolTh' and q_hourly > 0:
                    q_hourly = self.SolTh.get_heat(q_hourly, i)
            if q_hourly != 0:
                return False

            p_hourly = self.electrical_profile[i]  # Hourly electrical demand
            if 'ElHe' in th_order:  # Adding electrical heater production to the electrical demand.
                p_hourly += self.ElHe.heat_hourly[i]
            # Meeting the electrical demand
            for technology in el_order:
                if technology is 'PV' and p_hourly > 0:
                    if 'ElSt' in el_order:
                        p_hourly = self.PV.get_electricity(p_hourly, i, self.ElSt)
                    else:
                        p_hourly = self.PV.get_electricity(p_hourly, i)
                if technology is 'CHP' and p_hourly > 0:
                    if 'ElSt' in el_order:
                        p_hourly = self.OnOffCHP.get_electricity(p_hourly, i, self.ElSt)
                    else:
                        p_hourly = self.OnOffCHP.get_electricity(p_hourly, i)
                if technology is 'ElSt' and p_hourly > 0:
                    p_hourly = self.ElSt.get_electricity(p_hourly, i)
                # If electrical demand is not met, take electricity from the grid.
                if p_hourly > 0:
                    self.ElGrid.get_electricity(p_hourly, i)
        return True

    def write_hourly_excel(self, workbook_name, th_order, el_order):
        """
        Writes hourly data into the excel sheet.

        :param workbook_name: String containing the name of the excel sheet
        :param th_order: Thermal priority
        :param el_order: Electrical priority
        :return: none
        """
        # ---------------------------------------------------------------------
        # write all values into the worksheet
        worksheet_name = self.get_priority(th_order)+','+self.get_priority(el_order)
        workbook = open_workbook(workbook_name, worksheet_name)
        idx = workbook.sheet_names().index(worksheet_name)
        workbook = copy(workbook)
        worksheet = workbook.get_sheet(idx)
        worksheet.write(0, 0, 'Hour')
        worksheet.write(0, 1, 'Hourly Thermal Demand')
        count = 2
        for technology in th_order:
            if technology is 'CHP':
                worksheet.write(0, count, 'CHP Production')
            elif technology is 'B':
                worksheet.write(0, count, 'Boiler Production')
            elif technology is 'ElHe':
                worksheet.write(0, count, 'Electrical Resistance Heater Production')
            elif technology is 'ThSt':
                worksheet.write(0, count, 'Heat stored in Thermal Storage')
                count += 1
                worksheet.write(0, count, 'Heat provided by thermal Storage')
            # elif technology is 'HP':
            #    worksheet.write(0, count, 'Heat Pump Production')
            elif technology is 'SolTh':
                worksheet.write(0, count, 'Solar Thermal Production')
            count += 1

        for i in range(0, 8760):
            worksheet.write(i+1, 0, i)
            worksheet.write(i+1, 1, self.thermal_profile[i])
            count = 2
            for technology in th_order:
                if technology is 'CHP':
                    worksheet.write(i+1, count, self.OnOffCHP.heat_hourly[i])
                elif technology is 'B':
                    worksheet.write(i+1, count, self.B.heat_hourly[i])
                elif technology is 'ElHe':
                    worksheet.write(i+1, count, self.ElHe.heat_hourly[i])
                elif technology is 'ThSt':
                    worksheet.write(i+1, count, self.ThSt.heat_stored[i])
                    count += 1
                    worksheet.write(i+1, count, self.ThSt.heat_given[i])
                # elif technology is 'HP':
                #    worksheet.write(i+1, count, self.HP.heat_hourly[i])
                elif technology is 'SolTh':
                    worksheet.write(i+1, count, self.SolTh.heat_hourly[i])
                count += 1

        if 'ThSt' in th_order:
            count = 3 + len(th_order)
        else:
            count = 2 + len(th_order)
        worksheet.write(0, count, 'Hourly Electrical Demand')
        count += 1
        for technology in el_order:
            if technology is 'CHP':
                worksheet.write(0, count, 'CHP Electricity Production')
                count += 1
                worksheet.write(0, count, 'CHP Exported Electricity')
            elif technology is 'PV':
                worksheet.write(0, count, 'PV Production')
                count += 1
                worksheet.write(0, count, 'PV Exported Electricity')
            # elif technology is 'HP':
            #    worksheet.write(0, count, 'HP electricity Consumption')
            elif technology is 'ElSt':
                worksheet.write(0, count, 'Electricity stored in electrical storage')
                count += 1
                worksheet.write(0, count, 'Electricity provided by electrical storage')
            count += 1
        worksheet.write(0, count, 'Electricity Grid Production')

        for i in range(0, 8760):
            if 'ThSt' in th_order:
                count = 3 + len(th_order)
            else:
                count = 2 + len(th_order)
            worksheet.write(i+1, count, self.electrical_profile[i])
            count += 1
            for technology in el_order:
                if technology is 'CHP':
                    worksheet.write(i+1, count, self.OnOffCHP.electricity_hourly[i])
                    count += 1
                    worksheet.write(i+1, count, self.OnOffCHP.electricity_hourly_exported[i])
                elif technology is 'PV':
                    worksheet.write(i+1, count, self.PV.electricity_hourly[i])
                    count += 1
                    worksheet.write(i+1, count, self.PV.electricity_hourly_exported[i])
                # elif technology is 'HP':
                #    worksheet.write(i+1, count, self.HP.electricity_hourly[i])
                elif technology is 'ElSt':
                    worksheet.write(i+1, count, self.ElSt.electricity_stored[i])
                    count += 1
                    worksheet.write(i+1, count, self.ElSt.electricity_given[i])
                count += 1
            worksheet.write(i+1, count, self.ElGrid.electricity_hourly[i])

        workbook.save(workbook_name)

    @staticmethod
    def get_system_name(system):
        """
        Concatenates the name of the technologies and generates the system name for excel workbook naming

        :param system: set of technologies in system
        :return: system_name : set of technologies in system- suitably formatted for excel workbook naming
        """
        system_name = ''
        count = 1
        for i in system:
            if len(set(system)) == count:
                system_name += i
            else:
                system_name += i + '-'
                count += 1
        return system_name

    @staticmethod
    def get_priority(order):
        """
        Returns the priority list suitably formatted for excel worksheet naming

        :param order: set of technologies in thermal or electrical priority
        :return: priority : set of technologies in priority list- suitably formatted for excel worksheet naming
        """
        priority = ''
        count = 1
        for elements in order:
            if len(order) == count:
                priority += elements
            else:
                priority += elements + '>'
                count += 1
        return priority

    def write_kpi_excel(self):
        """
        Writes data into the KPI excel.

        :param: none
        :return: none
        """
        # Change to building directory
        os.chdir(self.location+'/'+self.building_id)
        excel = xlsxwriter.Workbook(self.building_id+'.xls')  # Create excel
        worksheet = excel.add_worksheet('Thermal Profile')  # Insert thermal profile of the building in the first sheet
        for row in range(0, len(self.thermal_profile)):
            worksheet.write(row, 0, row)
            worksheet.write(row, 1, self.thermal_profile[row])

        # Create a new Chart object.
        chart = excel.add_chart({'type': 'line'})

        chart.set_x_axis({
                         'name': 'Hours',
                         'name_font': {'size': 10, 'bold': True},
                         'label_position': 'low'
                         })

        chart.set_y_axis({
                         'name': 'Thermal Demand in kWh',
                         'name_font': {'size': 10, 'bold': True}
                         })

        chart.set_title({'name': 'Thermal Load Profile'})

        # Configure the chart.
        chart.add_series({'values': ['Thermal Profile', 0, 1, 8760, 1],
                          'categories': ['Thermal Profile', 0, 0, 8760, 0]})
        chart.set_legend({'none': True})
        # Insert the chart into the worksheet.
        worksheet.insert_chart('D4', chart)

        # Second sheet with all the systems, thermal priorities and electrical priorities.
        worksheet = excel.add_worksheet('KPI')
        worksheet.write(0, 0, 'System')
        worksheet.write(0, 1, 'Thermal Priority')
        worksheet.write(0, 2, 'Electrical Priority')
        worksheet.write(0, 3, 'Annuity (Euros)')
        worksheet.write(0, 4, 'Emissions (kg of CO2)')
        worksheet.write(0, 5, 'Primary Energy Factor')
        worksheet.write(0, 6, 'Total Losses (kWh)')
        worksheet.write(0, 7, 'CHP capacity (kW)')
        worksheet.write(0, 8, 'CHP heat (kWh)')
        worksheet.write(0, 9, 'CHP_On_Count')
        worksheet.write(0, 10, 'CHP_Hours (hours)')
        worksheet.write(0, 11, 'Boiler capacity (kW)')
        worksheet.write(0, 12, 'Boiler heat (kWh)')
        worksheet.write(0, 13, 'Storage capacity (liters)')
        worksheet.write(0, 14, 'Storage heat (kWh)')
        worksheet.write(0, 15, 'Solar Thermal Are (m2)')
        worksheet.write(0, 16, 'Solar Thermal heat (kWh)')
        worksheet.write(0, 17, 'El heater capacity (kW)')
        worksheet.write(0, 18, 'El heater heat (kWh)')
        worksheet.write(0, 19, 'PV area (m2)')
        worksheet.write(0, 20, 'PV El (kWh)')
        worksheet.write(0, 21, 'CHP Annuity(Euros)')
        worksheet.write(0, 22, 'Boiler Annuity(Euros)')
        worksheet.write(0, 23, 'Th Storage Annuity(Euros)')
        worksheet.write(0, 24, 'Sol Thermal Annuity(Euros)')
        worksheet.write(0, 25, 'El Heater Annuity(Euros)')
        worksheet.write(0, 26, 'PV Annuity(Euros)')
        worksheet.write(0, 27, 'Self Consumption needed for break-even with \
                                boiler(%)')
        row = 1
        for item in self.KPI:
            for column in range(0, 28):
                worksheet.write(row, column, item[column])
                column += 1
            row += 1

        # Create a new Chart object.
        chart = excel.add_chart({'type': 'scatter'})

        chart.set_x_axis({
                         'name': 'Yearly Emissions',
                         'name_font': {'size': 10, 'bold': True},
                         'label_position': 'low'
                         })

        chart.set_y_axis({
                         'name': 'Annuity',
                         'name_font': {'size': 10, 'bold': True}
                         })

        chart.set_title({'name': 'Results'})

        # Configure the chart. In simplest case we add one or more data series.
        chart.add_series({'values': ['KPI', 1, 3, row, 3],
                          'categories': ['KPI', 1, 4, row, 4]})
        chart.set_legend({'none': True})
        # Insert the chart into the worksheet.
        worksheet.insert_chart('V4', chart)

#        worksheet = excel.add_worksheet('Economic Factors in Detail')
#        worksheet.write(0, 0, "System")
#        worksheet.write(0, 1, "Thermal Priority")
#        worksheet.write(0, 2, "Total Annuity(Euros)")
#        worksheet.write(0, 3, "Th Capacity of CHP(kW)")
#        worksheet.write(0, 4, "Heat generated by the CHP(kWh)")
#        worksheet.write(0, 5, "Electricity generated by the CHP(kWh)")
#        worksheet.write(0, 6, "Annuity factor")
#        worksheet.write(0, 7, "CHP Capital Costs(Euros)")
#        worksheet.write(0, 8, "CHP bonus(Euros)")
#        worksheet.write(0, 9, "CHP Capital related Annuity(Euros)")
#        worksheet.write(0, 10, "CHP demand related Annuity(Euros)")
#        worksheet.write(0, 11, "CHP operation related Annuity(Euros)")
#        worksheet.write(0, 12, "CHP proceeds related Annuity(Euros)")
#        worksheet.write(0, 13, "CHP Total Annuity(Euros)")
#        worksheet.write(0, 14, "Boiler Capacity(kW)")
#        worksheet.write(0, 15, "Heat generated by the Boiler(kWh)")
#        worksheet.write(0, 16, "Boiler Capital related Costs(Euros)")
#        worksheet.write(0, 17, "Boiler Capital related Annuity(Euros)")
#        worksheet.write(0, 18, "Boiler demand related Annuity(Euros)")
#        worksheet.write(0, 19, "Boiler operation related Annuity(Euros)")
#        worksheet.write(0, 20, "Total Boiler Annuity(Euros)")
#        row = 1
#        for item in self.EconomicFactors:
#            for column in range(0, 21):
#                worksheet.write(row, column, item[column])
#                column += 1
#            row += 1

        excel.close()
        return
