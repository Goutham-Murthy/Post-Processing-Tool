# -*- coding: utf-8 -*-
"""
Module consists class representing electric heaters.
"""
import annuity


class ElectricHeater(annuity.Annuity):
    """Class representing Electric Heaters. Efficiency is approximated to 100%.

    Attributes:
        model (string)          : Model of the Electric Heater.
        th_capacity (float): Thermal capacity of the Electric Heater [kW].
        heat_yearly (float)     : Sum value of heat provided by the electric
                                 heater unit over the year [kWh].
        heat_hourly (float)     : Hourly values of the heat provided by the
                                 Electric Heater unit [kWh].
        annuity (float)         : Annuity of the Electric Heater [Euros].
        emissions (float)       : CO2 emissions of the electric heater unit
                                 [kg of CO2].

    Extends:
        Annuity class
        """
    def __init__(self, model, th_capacity):
        """ Constructor method for Electric Heater Class

        Args:
            model (string)              : Model of the Electric Heater.
            th_capacity (float)         : Thermal capacity of the Electric
                                         Heater [kW].
        """
        self.model = model
        self.th_capacity = th_capacity
        # Initialising other variables to zero.
        self.heat_hourly = [0]*8760
        self.heat_yearly = 0
        self.annuity = 0
        self.emissions = 0
        super(ElectricHeater, self).__init__(deperiod=15, effop=5, fwins=1,
                                             finst=1)

    def get_heat(self, required_heat, hour):
        """
        Given the required heat, function calculates the hourly heat met by the
        electric heater and returns the value for unsatisfied thermal demand.

        Args:
            required_heat (float)   : Hourly heat demand of the building [kWh].
            hour (int)              : Hour of the year.

        Returns:
            required_heat (float)   : Hourly thermal demand not met by the
                                     electric heater [kWh].
        """
        # If thermal capacity is more than hourly thermal demand, meet the
        # demand entirely.
        if required_heat <= self.th_capacity:
            self.heat_yearly += required_heat
            self.heat_hourly[hour] = required_heat
            required_heat = 0
            return required_heat
        # If hourly thermal demand is greater than the capacity, meet as much
        # as possible.
        else:
            self.heat_yearly += self.th_capacity
            self.heat_hourly[hour] = self.th_capacity
            required_heat -= self.th_capacity
            return required_heat

    def set_emissions(self):
        """
        Calculates the CO2 emissions of the electric heater unit.

        Args:
            None.

        Returns:
            None.
        """
        # CO2 emissions for production of grid electricity, used by electric
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
        self.A0 = 53.938*(self.th_capacity*1000)**0.2685
        self.set_Ank()

        # Demand related costs include price of fuel to generate the required
        # heat i.e. electricity price
        drc = self.heat_yearly*self.electricity_price
        self.Anv = drc*self.a*self.bv

        # Operation related costs include maintenance and repair
        orc = 30*self.effop
        ain = self.A0*(self.finst+self.fwins)/100
        self.Anb = orc*self.a*self.bb + ain*self.a*self.bi

        # Other costs
        self.Ans = 0

        # Proceeds
        self.Ane = 0

        self.annuity = self.Ane - (self.Ank + self.Anv + self.Anb + self.Ans)
        return
