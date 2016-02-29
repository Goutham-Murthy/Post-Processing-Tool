# -*- coding: utf-8 -*-


from xlrd import open_workbook
from xlutils.copy import copy
import CHP
import boiler
import electricheater
import thermalstorage
import solarthermal
import photovoltaics
import electricalstorage
import electricalgrid
import database


class SupplySystem:
    """
    Class for supply system. Different supply systems with different compositions and thermal and electrical priorities
    are formed by the pre-processing tool.

    Attributes
        th_order        : Thermal priority of system
        el_order        : Electrical priority of system
        peak_th_power   : Peak thermal power
        maxr_th_power   : Thermal power according to maximum rectangle method
        global_radiation: Hourly global radiation values
        total_annuity   : Annuity of the whole system
        total_emissions : Emissions of the whole system
        total_pef       : Primary energy factor of the whole system
        OnOffCHP        : Instance of the CHP class with ON/OFF operating strategy.
        B               : Instance of boiler class
        ElHe            : Instance of the electric heater class.
        SolTh           : Instance of the solar thermal class.
        PV              : Instance of the PV class.
        ThSt            : Instance of the thermal storage class.
        ElSt            : Instance of the electric storage class.
        ElGrid          : Instance of the electric grid glass.

    Extends
        none
    """
    def __init__(self, th_order, el_order, peak_th_power, maxr_th_power, global_radiation):
        """
        Constructor class for supply system

        :param th_order: Thermal priority of system
        :param el_order: Electrical priority of system
        :param peak_th_power: Peak thermal power
        :param maxr_th_power: Thermal power according to maximum rectangle method
        :param global_radiation: Hourly global radiation values
        :return:
        """
        self.th_order = th_order
        self.el_order = el_order
        self.total_annuity = 0
        self.total_emissions = 0
        self.total_pef = 0
        self.peak_th_power = peak_th_power
        self.maxr_th_power = maxr_th_power
        self.global_radiation = global_radiation
        # ---------------------------------------------------------------------
        # CHP
        # If CHP is present, it will check for a peak load device. If peak load
        # device is present, CHP is sized according to maximum rectangle
        # method. Otherwise it is sized according to peak thermal load.
        if 'CHP' in th_order and 'ElHe' not in th_order and 'B'not in th_order:
            self.OnOffCHP = CHP.OnOffCHP(database.get_chp_capacity(self.peak_th_power))
        if 'CHP' in th_order and ('ElHe' in th_order or 'B' in th_order):
            self.OnOffCHP = CHP.OnOffCHP(database.get_chp_capacity(self.maxr_th_power))

        # ---------------------------------------------------------------------
        # Boiler
        # If boiler is present, dimension it to peak thermal demand
        if 'B' in th_order:
            self.B = boiler.Boiler(database.get_b_capacity(self.peak_th_power))

        # ---------------------------------------------------------------------
        # Electric Resistance Heater
        # If electric heater is present, dimension it to peak thermal demand
        if 'ElHe' in th_order:
            self.ElHe = electricheater.ElectricHeater('Electric Heater Model',
                                                      database.get_elhe_capacity(self.peak_th_power))

        # ---------------------------------------------------------------------
        # Thermal Storage
        # If thermal storage is present, dimension it according to CHP
        # capacity.
        if 'ThSt' in th_order:
            self.ThSt = thermalstorage.ThermalStorage(database.get_thst_capacity(3*self.OnOffCHP.th_capacity))

        # ---------------------------------------------------------------------
        # Solar Thermal
        # If Solar thermal is present, dimension according to roof area
        if 'SolTh' in th_order:
            self.SolTh = solarthermal.SolarThermal('Buderus SKS 5.0-s', database.get_solth_capacity(database.SolTh_available_area),
                                                   self.global_radiation)

        # ---------------------------------------------------------------------
        # Photovoltaics
        # If PV is present, dimension according to roof area
        if 'PV' in el_order:
            self.PV = photovoltaics.Photovoltaics('Buderus aleo s19', database.get_pv_capacity(database.PV_available_area),
                                                  self.global_radiation)

        # ---------------------------------------------------------------------
        # Electrical Storage
        # Dimension logic to be implemented
        if 'ElSt' in el_order:
            self.ElSt = electricalstorage.ElectricalStorage('Model', database.ElSt_capacity, 1)

        # ---------------------------------------------------------------------
        # HeatPump

        # ---------------------------------------------------------------------
        # Electrical Grid
        # Initialising electrical grid
        self.ElGrid = electricalgrid.ElectricalGrid()
        return

    def perform_calculations(self, thermal_profile, electrical_profile):
        """
        Performs the thermal and electrical calculations.

        :param thermal_profile:
        :param electrical_profile:
        :return:
        """
        print self.th_order, self.el_order
        for i in range(0, 8760):
            q_hourly = thermal_profile[i]  # Hourly thermal demand
            if 'ThSt' in self.th_order:  # Thermal loss in the thermal storage
                self.ThSt.apply_losses(i)

            # Meeting the thermal demand
            for technology in self.th_order:
                if technology is 'CHP' and q_hourly > 0:
                    if 'ThSt' in self.th_order:
                        q_hourly = self.OnOffCHP.get_heat(q_hourly, i, self.ThSt)
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

            p_hourly = electrical_profile[i]  # Hourly electrical demand
            if 'ElHe' in self.th_order:
                p_hourly += self.ElHe.heat_hourly[i]  # Adding to the electrical demand
            # Meeting the electrical demand
            for technology in self.el_order:
                if technology is 'PV':
                    if 'ElSt' in self.el_order:
                        p_hourly = self.PV.get_electricity(p_hourly, i, self.ElSt)
                    else:
                        p_hourly = self.PV.get_electricity(p_hourly, i)
                if technology is 'CHP':
                    if 'ElSt' in self.el_order:
                        p_hourly = self.OnOffCHP.get_electricity(p_hourly, i, self.ElSt)
                    else:
                        p_hourly = self.OnOffCHP.get_electricity(p_hourly, i)
                if technology is 'ElSt':
                    p_hourly = self.ElSt.get_electricity(p_hourly, i)
                # If electrical demand is not met, take electricity from the grid.
                if p_hourly > 0:
                    self.ElGrid.get_electricity(p_hourly, i)

            if 'ElHe' in self.th_order:
                # If imported electricity from grid is more than consumer electrical demand, the increased demand is due
                # to the electric heater
                if self.ElGrid.electricity_hourly[i] > electrical_profile[i]:
                    self.ElHe.imported_electricity += self.ElGrid.electricity_hourly[i] - electrical_profile[i]
                # If imported electricity is lower or equal to consumer electrical demand then electric heater
                # electricity demand is met through in-house sources.
        return True

    def calculate_kpi(self):
        # calculate annuity and emissions for the technologies present in the system.
        total_final_energy = 0
        total_primary_energy = 0
        if 'CHP' in self.th_order:
            if 'ThSt' in self.th_order:
                self.OnOffCHP.set_annuity(storage=True)
            else:
                self.OnOffCHP.set_annuity()
            self.OnOffCHP.set_emissions()
            self.OnOffCHP.set_hours_on_count()
            self.total_annuity += self.OnOffCHP.annuity
            self.total_emissions += self.OnOffCHP.emissions
            total_final_energy += self.OnOffCHP.heat_yearly
            total_primary_energy += self.OnOffCHP.heat_yearly * 0.7

        if 'B' in self.th_order:
            self.B.set_annuity()
            self.B.set_emissions()
            self.total_annuity += self.B.annuity
            self.total_emissions += self.B.emissions
            total_final_energy += self.B.heat_yearly
            total_primary_energy += self.B.heat_yearly * 1.1

        if 'ElHe' in self.th_order:
            self.ElHe.set_annuity()
            self.ElHe.set_emissions()
            self.total_annuity += self.ElHe.annuity
            self.total_emissions += self.ElHe.emissions
            total_final_energy += self.ElHe.imported_electricity
            total_primary_energy += self.ElHe.imported_electricity * 2.8

        if 'ThSt' in self.th_order:
            self.ThSt.set_annuity()
            self.total_annuity += self.ThSt.annuity

        if 'SolTh' in self.th_order:
            self.SolTh.set_annuity()
            self.total_annuity += self.SolTh.annuity
            total_final_energy += self.SolTh.heat_yearly
            total_primary_energy += self.SolTh.heat_yearly * 1

        if 'PV' in self.el_order:
            self.PV.set_annuity()
            self.PV.set_emissions()
            self.total_annuity += self.PV.annuity
            self.total_emissions += self.PV.emissions

        if 'ElSt' in self.el_order:
            self.ElSt.set_annuity()
            self.total_annuity += self.ElSt.annuity

        self.ElGrid.set_annuity()
        self.ElGrid.set_emissions()
        self.total_annuity += self.ElGrid.annuity
        self.total_emissions += self.ElGrid.emissions
        self.total_pef = total_primary_energy / total_final_energy

    def write_hourly_excel(self, workbook_name, worksheet_name, thermal_profile, electrical_profile):
        """
        Writes hourly data into the excel sheet.

        :param workbook_name: String containing the name of the excel sheet
        :param workbook_name: Name of the workbook
        :param worksheet_name: Name of the worksheet
        :param thermal_profile: Thermal profile of the building
        :param electrical_profile: Electrical profile of the building
        :return: none
        """
        # ---------------------------------------------------------------------
        # write all values into the worksheet
        workbook = open_workbook(workbook_name, worksheet_name)
        idx = workbook.sheet_names().index(worksheet_name)
        workbook = copy(workbook)
        worksheet = workbook.get_sheet(idx)
        worksheet.write(0, 0, 'Hour')
        worksheet.write(0, 1, 'Hourly Thermal Demand')
        count = 2
        for technology in self.th_order:
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
            worksheet.write(i+1, 1, thermal_profile[i])
            count = 2
            for technology in self.th_order:
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

        if 'ThSt' in self.th_order:
            count = 3 + len(self.th_order)
        else:
            count = 2 + len(self.th_order)
        worksheet.write(0, count, 'Hourly Electrical Demand')
        count += 1
        for technology in self.el_order:
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
            if 'ThSt' in self.th_order:
                count = 3 + len(self.th_order)
            else:
                count = 2 + len(self.th_order)
            worksheet.write(i+1, count, electrical_profile[i])
            count += 1
            for technology in self.el_order:
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
