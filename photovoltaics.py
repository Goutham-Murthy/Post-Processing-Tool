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
        self.electricity_hourly_exported = [0]*8760
        super(Photovoltaics, self).__init__(deperiod=25, effop=5, fwins=1, finst=0.5)

    def get_electricity(self, required_electricity, hour, ElSt=None):
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
        # If electrical production is more than electrical thermal demand, meet the
        # demand entirely.
        self.electricity_hourly[hour] = .15*0.8*self.area*self.global_radiation[hour]/1000  # In KWh
        self.electricity_yearly += self.electricity_hourly[hour]
        if ElSt is not None:
            if required_electricity < self.electricity_hourly[hour]:
                # Excess electricity can be stored in the storage unit.
                # Check for availability of electrical storage unit.
                possible_electricity_storage = min((self.electricity_hourly[hour] - required_electricity), ElSt.max_el,
                                                   ElSt.get_availability(hour))
                ElSt.store_electricity(possible_electricity_storage, hour)
                required_electricity = 0
                self.electricity_hourly_exported[hour] = self.electricity_hourly[hour] - possible_electricity_storage
            else:
                required_electricity -= self.electricity_hourly[hour]
        else:
            # If electrical production is more than electrical thermal demand, meet the
            # demand entirely and export the rest
            if required_electricity < self.electricity_hourly[hour]:
                self.electricity_hourly_exported[hour] = self.electricity_hourly[hour] - required_electricity
                required_electricity = 0
            # If hourly electrical demand is greater than the capacity, meet as much
            # as possible. Nothing is exported to the grid
            else:
                required_electricity -= self.electricity_hourly[hour]
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
