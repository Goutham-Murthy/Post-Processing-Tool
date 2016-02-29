# -*- coding: utf-8 -*-
import os
import itertools
import xlsxwriter
import shutil
import supplysystem


class PreProcessingTool:
    """
    PreProcessingTool

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
                 location='D:/aja-gmu/Simulation_Files/Output',
                 chp_type='ONOFF'):
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
        self.chp_type = chp_type

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
                                # Initialise system
                                self.supply_system = supplysystem.SupplySystem(th_order= th_order, el_order=el_order,
                                                                               peak_th_power=self.peak_th_power,
                                                                               maxr_th_power=self.maxr_th_power,
                                                                               global_radiation=self.global_radiation)
                                demand_satisfied = self.supply_system.perform_calculations(
                                                    thermal_profile=self.thermal_profile,
                                                    electrical_profile=self.electrical_profile)  # Perform calculations

                                if demand_satisfied:  # If system is successful in meeting the thermal demand
                                    self.update_kpi(system, th_order, el_order)  # Update the KPI variable.
                                    if self.hourly_excels:  # If hourly excels are required write data into them
                                        self.supply_system.write_hourly_excel(workbook_name=self.get_system_name(system)+'.xls',
                                                                              worksheet_name=self.get_priority(th_order)+','+self.get_priority(el_order),
                                                                              thermal_profile=self.thermal_profile,
                                                                              electrical_profile=self.electrical_profile
                                                                              )
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
        self.supply_system.calculate_kpi()

        # Append to the KPI variable.
        self.KPI.append([self.get_system_name(system),
                         self.get_priority(th_order),
                         self.get_priority(el_order),
                         self.supply_system.total_annuity,
                         self.supply_system.total_emissions,
                         self.supply_system.total_pef,
                         self.supply_system.ThSt.losses if 'ThSt' in system else 0,
                         self.supply_system.OnOffCHP.th_capacity if 'CHP' in system else 0,
                         self.supply_system.OnOffCHP.heat_yearly if 'CHP' in system else 0,
                         self.supply_system.OnOffCHP.on_count if 'CHP' in system else 0,
                         self.supply_system.OnOffCHP.on_hours if 'CHP' in system else 0,
                         self.supply_system.B.th_capacity if 'B' in system else 0,
                         self.supply_system.B.heat_yearly if 'B' in system else 0,
                         self.supply_system.ThSt.th_capacity if 'ThSt' in system else 0,
                         self.supply_system.ThSt.heat_stored[8760] if 'ThSt' in system else 0,
                         self.supply_system.SolTh.area if 'SolTh' in system else 0,
                         self.supply_system.SolTh.heat_yearly if 'SolTh' in system else 0,
                         self.supply_system.ElHe.th_capacity if 'ElHe' in system else 0,
                         self.supply_system.ElHe.heat_yearly if 'ElHe' in system else 0,
                         self.supply_system.PV.area if 'PV' in system else 0,
                         self.supply_system.PV.electricity_yearly if 'PV' in system else 0,
                         self.supply_system.OnOffCHP.annuity if 'CHP' in system else 0,
                         self.supply_system.B.annuity if 'B' in system else 0,
                         self.supply_system.ThSt.annuity if 'ThSt' in system else 0,
                         self.supply_system.SolTh.annuity if 'SolTh' in system else 0,
                         self.supply_system.ElHe.annuity if 'ElHe' in system else 0,
                         self.supply_system.PV.annuity if 'PV' in system else 0])

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

        # Insert thermal profile and electrical profile of the building in the first sheet
        worksheet = excel.add_worksheet('Th and El Profiles')

        worksheet.write(0, 0, 'Hour')
        worksheet.write(0, 1, 'Thermal Profile')
        worksheet.write(0, 2, 'Electrical Profile')

        for row in range(1, len(self.thermal_profile)):
            worksheet.write(row, 0, row)
            worksheet.write(row, 1, self.thermal_profile[row])
            worksheet.write(row, 2, self.electrical_profile[row])

        # Create a new Chart object.
        chart = excel.add_chart({'type': 'line'})

        chart.set_x_axis({
                         'name': 'Hours',
                         'name_font': {'size': 10, 'bold': True},
                         'label_position': 'low'
                         })

        chart.set_y_axis({
                         'name': 'Demand in kWh',
                         'name_font': {'size': 10, 'bold': True}
                         })

        chart.set_title({'name': 'Thermal and Electrical Load Profile'})

        # Configure the chart. [sheet_name, first_row, first_col, last_row, last_col]
        chart.add_series({'values': ['Th and El Profiles', 1, 1, 8761, 1],
                          'categories': ['Th and El Profiles', 1, 1, 8761, 1],
                          'name': 'Thermal Profile'})
        chart.add_series({'values': ['Th and El Profiles', 1, 2, 8761, 2],
                          'categories': ['Th and El Profiles', 1, 2, 8761, 2],
                          'name': 'Electrical Profile'})
        # chart.set_legend({'none': True})
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
        row = 1
        for item in self.KPI:
            for column in range(0, 27):
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
