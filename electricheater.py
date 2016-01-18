# -*- coding: utf-8 -*-
"""
Module consists class representing electric heaters.
"""
import annuity


class ElectricHeater(annuity.Annuity):
    """Class representing Electric Heaters. Efficiency is approximated to 100%.

    Attributes:
        model (string)          : Model of the Electric Heater.
        thermal_capacity (float): Thermal capacity of the Electric Heater [kW].
        heat_yearly (float)     : Sum value of heat provided by the electric
                                 heater unit over the year [kWh].
        heat_hourly (float)     : Hourly values of the heat provided by the
                                 Electric Heater unit [kWh].
        annuity (float)         : Annuity of the Electric Heater [Euros].
        emissions (float)       : CO2 emissions of the electric heater unit
                                 [kg of CO2].
        deperiod(float)         : Depreciation period [years].
        finst(float)            : Effort for annual repairs as percentage of
                                 initial investment [%].
        fwins(float)            : Effort for annual maintenance and inspection
                                 as percentage of total investment [%].
        effop(float)            : Effort for operation [hours/annum].

    Extends:
        Annuity class
        """
    def __init__(self, model, thermal_capacity):
        """ Constructor method for Electric Heater Class

        Args:
            model (string)              : Model of the Electric Heater.
            thermal_capacity (float)    : Thermal capacity of the Electric
                                         Heater [kW].
        """
        self.model = model
        self.thermal_capacity = thermal_capacity
        # Initialising other variables to zero.
        self.heat_hourly = [0]*8760
        self.heat_yearly = 0
        self.annuity = 0
        self.emissions = self.getEmissions()
        self.deperiod = 15
        self.finst = 0.01
        self.fwins = 0.01
        self.effop = 5

    def get_heat(self, required_heat, hour):
        """
        Given the required heat, function calculates the hourly heat met by the
        electric heater and returns the value for unsatified thermal demand.

        Args:
            required_heat (float)   : Hourly heat demand of the building [kWh].
            hour (int)              : Hour of the year.

        Returns:
            required_heat (float)   : Hourly thermal demand not met by the
                                     electric heater [kWh].
        """
        # If thermal capacity is more than hourly thermal demand, meet the
        # demand entirely.
        if required_heat <= self.thermal_capacity:
            self.heat_yearly += required_heat
            self.heat_hourly[hour] = required_heat
            required_heat = 0
            return required_heat
        # If hourly thermal demand is grreater than the capacity, meet as much
        # as possible.
        else:
            self.heat_yearly += self.thermal_capacity
            self.heat_hourly[hour] = self.thermal_capacity
            required_heat -= self.thermal_capacity
            return required_heat

    def set_emissions(self):
        """
        Calculates the CO2 emissions of the electric heater unit.

        Args:
            None.

        Returns:
            None.
        """
        # CO2 emissions for prodution of grid electricity, used by electric
        # heaters are 595 g/kWh for Germany.
        # [Petra Icha. Entwicklung der spezifischen Kohlendioxid-Emissionen des
        # deutschen Strommix in den Jahren 1990 bis 2013. Umweltbundesamt,
        # 2014]
        self.emissions = 595*self.heat_yearly/1000
        return

    def set_annuity(self):
        """
        Calculates the annuity of the boiler.

        Args:
            None.

        Returns:
            None..
        """
        # Capital related costs for the electrical heater include price of
        # purchase and installation costs
        self.A0 = 53.938*(self.thermal_capacity*1000)**0.2685
        self.set_Ank()

        # Demand related costs include price of fuel to generate the required
        # heat i.e. electricity price
        DRC = self.heat*self.electricity_price
        self.Anv = DRC*self.a*self.bv

        # Operation related costs include maintanance and repair
        ORC = 30*self.effop
        Ain = self.A0*(self.finst+self.fwins)
        self.Anb = ORC*self.a*self.bb + Ain*self.a*self.bi

        # Other costs
        self.Ans = 0

        # Proceeds
        self.Ane = 0

        self.annuity = self.Ane - (self.Ank + self.Anv + self.Anb + self.Ans)
        return
