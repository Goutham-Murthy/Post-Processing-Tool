# -*- coding: utf-8 -*-
import annuity


class ElectricalGrid(annuity.Annuity):
    """Class representing the electrical grid.

    Attributes:
        electricity_hourly: (float)Hourly values of electricity exported to the grid [kWh]
        electricity_yearly: (float)Sum value of electricity exported to teh grid throughout the year [kWh]
        emissions: (float) Emissions due to imported electricity throughout the year [kg of CO2].
        annuity: (float)Annuity of the grid thanks to the imported electricity [Euros].
    Extends:
        Annuity class
    """

    def __init__(self):
        """Constructor method for class electrical grid.

        :param: none
        :return: none
        """
        # Initialising variables to zero.
        self.electricity_hourly = [0]*8760
        self.electricity_yearly = 0
        self.annuity = 0
        self.emissions = 0
        super(ElectricalGrid, self).__init__(deperiod=0, effop=0, fwins=0, finst=0)

    def set_emissions(self):
        """
        Calculates the contribution of CO2 emissions of the grid due to the imported electricity.

        :param: none
        :return: none
        """
        # Grid electricity in Germany has an emission factor of 595 g of CO2/kWh
        # [Petra Icha. Entwicklung der spezifischen Kohlendioxid-Emissionen des deutschen Strommix in den
        # Jahren 1990 bis 2013. Umweltbundesamt, 2014.]
        self.emissions = (595*self.electricity_yearly/1000)
        return

    def set_annuity(self):
        """
        Calculates the annuity of the electrical grid.

        :param: none
        :return: none
        """
        # Capital related costs for the grid are nil
        self.A0 = 0
        self.Ank = 0

        # Demand related costs include price of imported electricity
        drc = self.electricity_price*self.electricity_yearly
        self.Anv = drc*self.a*self.bv

        # Operation related costs include maintenance and repair
        self.Anb = 0

        # Other costs
        self.Ans = 0

        # Proceeds
        self.Ane = 0

        self.annuity = self.Ane - (self.Ank + self.Anv + self.Anb + self.Ans)
        return

    def get_electricity(self, required_electricity, hour):
        """
        Calculates electricity provided by electrical grid.

        :param required_electricity: (float)Hourly electrical demand of the building [kWh].
        :param hour: (int)Hour of the year[hour].
        :return: none
        """
        self.electricity_yearly += required_electricity
        self.electricity_hourly[hour] = required_electricity
        return

# CHP = OnOffCHP('YahooCHP', 2.7, 1, 0.6, 0.3)
# CHP.get_heat(3, 31)
