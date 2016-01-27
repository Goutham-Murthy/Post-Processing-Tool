# -*- coding: utf-8 -*-
import annuity


class ElectricalGrid(annuity.Annuity):
    """Class representing the electrical grid.

    Attributes:
        electricity_yearly (float)   : Electricity provided by the electric grid unit over the
                                 year[kWh].
        electricity_hourly (float)   : Hourly values of the heat demand met by
                                 the electric grid unit [kWh].
        annuity (float)     : Annuity contribution of the grid to the annuity of the system [Euros].
        emissions (float)   : Emission contribution of the imported electricity to the grid [kg of CO2]
    Extends:
        Annuity class
    """

    def __init__(self):
        """Constructor method for class CHP.

        Args:
            None.
        Returns:
            None.
        """
        # Initialising variables to zero.
        self.electricity_hourly = [0]*8760
        self.electricity_yearly = 0
        self.annuity = 0
        self.annuity = 0
        self.emissions = 0
        super(ElectricalGrid, self).__init__(deperiod=0, effop=0, fwins=0, finst=0)

    def set_emissions(self):
        """
        Calculates the contribution of CO2 emissions of the grid due to the imported electricity.
        Args:
            None.

        Returns:
            None.
        """
        self.emissions = (595*self.electricity_yearly/1000)
        return

    def set_annuity(self):
        """
        Calculates the annuity of the electrical grid.

        Args:
            None.

        Returns:
            None..
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

    def get_electricity(self, p_hourly, hour):
        """
        Calculates electricity provided by electrical grid.
        :param p_hourly: Electricity demand in that hour  [kWh]
        :param hour: Hour
        :return: None
        """
        self.electricity_yearly += p_hourly
        self.electricity_hourly[hour] = p_hourly
        return

# CHP = OnOffCHP('YahooCHP', 2.7, 1, 0.6, 0.3)
# CHP.get_heat(3, 31)
