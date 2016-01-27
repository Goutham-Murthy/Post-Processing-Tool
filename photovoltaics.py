# -*- coding: utf-8 -*-
import annuity


class Photovoltaics(annuity.Annuity):
    """Class representing PV.

    Attributes:
        area (float)        : Area of the PV module [m2].
        electricity_yearly (float) : Sum value of electricity provided by the PV
                             unit over the year [kWh].
        electricity_hourly (float) : Hourly values of the electricity provided by the
                             PV unit [kWh].
        annuity (float)       : Annuity of the PV [Euros].
        emissions (float)     : CO2 emissions of the PV [kg of CO2].
    Extends:
        Annuity class
    """

    def __init__(self, model, area, global_radiation):
        """
        Constructor method for class Boiler.
        :param model: Model of the PV
        :param area: Area of the PV module [m2].
        :param global_radiation: Global radiation incident on the PV module.
        :return: none
        """
        self.model = model
        self.area = area
        self.global_radiation = global_radiation
        # Initialising other variables to zero.
        self.electricity_hourly = [0]*8760
        self.electricity_yearly = 0
        self.annuity = 0
        self.emissions = 0
        super(Photovoltaics, self).__init__(deperiod=25, effop=5, fwins=1, finst=0.5)

    def get_electricity(self, required_electricity, hour):
        """
        Given the required electricity, function calculates the hourly heat met
        by the PV and returns the value for electricity thermal demand.

        Args:
            required_electricity (float)    : Hourly electrical demand of the building
                                            [kWh].
            hour (int)                      : Hour of the year.

        Returns:
            required_electricity (float)   : Hourly electrical demand not met by the
                                            PV [kWh].
        """
        # If thermal capacity is more than hourly thermal demand, meet the
        # demand entirely.
        produced_electricity = .15*0.8*self.area*self.global_radiation[hour]
        if required_electricity <= produced_electricity:
            self.electricity_yearly += required_electricity
            self.electricity_hourly[hour] = required_electricity
            required_electricity = 0
        # If hourly thermal demand is greater than the capacity, meet as much
        # as possible.
        else:
            self.electricity_yearly += produced_electricity
            self.electricity_hourly[hour] = produced_electricity
            required_electricity -= produced_electricity
        return required_electricity

    def set_emissions(self):
        """
        Calculates the CO2 emissions of the boiler unit.

        Args:
            None.

        Returns:
            None
        """
        self.emissions = (-705*self.electricity_yearly/1000)
        return

    def set_annuity(self):
        """
        Calculates the annuity of the boiler.

        Args:
            None.

        Returns:
            None
        """
        # Capital related costs for the boiler include price of purchase and installation costs.
        self.A0 = 200*self.area + 500 + 65*self.area
        self.set_Ank()

        # Demand related costs include price of fuel to produce required heat
        drc = 0
        self.Anv = drc*self.a*self.bv

        # Operation related costs include maintenance and repair
        orc = 30*self.effop
        ain = self.A0*(self.finst + self.fwins)/100   # finst and fwins in %
        self.Anb = orc*self.a*self.bb + ain*self.a*self.bi

        # Other costs
        self.Ans = 0

        # Proceeds
        self.Ane = 0

        self.annuity = self.Ane - (self.Ank + self.Anv + self.Anb + self.Ans)
        return
# b=Boiler('Model',11.2,0.98)
# print b.emissions
