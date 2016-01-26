# -*- coding: utf-8 -*-
import annuity


class PV(annuity.Annuity):
    """Class representing PV.

    Attributes:
        area (float)        : Area of the PV module [m2].
        elec_yearly (float) : Sum value of electricity provided by the PV
                             unit over the year [kWh].
        elec_hourly (float) : Hourly values of the electricity provided by the
                             PV unit [kWh].
        annuity (float)       : Annuity of the PV [Euros].
        emissions (float)     : CO2 emissions of the PV [kg of CO2].
        deperiod(float)       : Depreciation period [years].
        finst(float)          : Effort for annual repairs as percentage of
                               initial investment [%].
        fwins(float)          : Effort for annual maintenance and inspection
                               as percentage of total investment [%].
        effop(float)          : Effort for operation [hours/annum].

    Extends:
        Annuity class
    """

    def __init__(self, area):
        """Constructor method for class Boiler.

        Args:
            area (float)        : Area of the PV module [m2].
        """
        self.area = area
        # Initialising other variables to zero.
        self.elec_hourly = [0]*8760
        self.elec_yearly = 0
        self.annuity = 0
        self.emissions = 0
        self.deperiod = 25
        self.finst = .5
        self.fwins = 1
        self.effop = 5
        super(PV, self).__init__(deperiod=25, effop=5, fwins=1, finst=0.5)

    def get_elec(self, required_elec, hour):
        """
        Given the required electricity, function calculates the hourly heat met
        by the PV and returns the value for electricity thermal demand.

        Args:
            required_elec (float)   : Hourly electrical demand of the building
                                     [kWh].
            hour (int)              : Hour of the year.

        Returns:
            required_elec (float)   : Hourly electrical demand not met by the
                                      PV [kWh].
        """
        # If thermal capacity is more than hourly thermal demand, meet the
        # demand entirely.
        if required_elec <= self.th_capacity:
            self.heat_yearly += required_elec
            self.heat_hourly[hour] = required_elec
            required_heat = 0
        # If hourly thermal demand is grreater than the capacity, meet as much
        # as possible.
        else:
            self.heat_yearly += self.th_capacity
            self.heat_hourly[hour] = self.th_capacity
            required_heat -= self.th_capacity
        return required_heat

    def set_emissions(self):
        """
        Calculates the CO2 emissions of the boiler unit.

        Args:
            None.

        Returns:
            None
        """
        # CO2 emissions of condensing boilers are about 56 g/MJ or 201.6 g/kWh.
        # [R Dones, Thomas Heck, and S Hirschberg. Greenhouse gas emissions
        # from energy systems:comparison and overview. 2004.]
        self.emissions = (201.6*self.heat_yearly/1000)
        return

    def set_annuity(self):
        """
        Calculates the annuity of the boiler.

        Args:
            None.

        Returns:
            None
        """
        # Capital related costs for the boiler include price of purchase and
        # installation costs.
        self.A0 = 79.061*self.th_capacity + 1229.8
        self.set_Ank()

        # Demand related costs include price of fuel to produce required heat
        DRC = self.gas_price*self.heat_yearly/self.efficiency
        self.Anv = DRC*self.a*self.bv

        # Operation related costs include maintanance and repair
        ORC = 30*self.effop
        Ain = self.A0*(self.finst + self.fwins)/100   # finst and fwins in %
        self.Anb = ORC*self.a*self.bb + Ain*self.a*self.bi

        # Other costs
        self.Ans = 0

        # Proceeds
        self.Ane = 0

        self.annuity = self.Ane - (self.Ank + self.Anv + self.Anb + self.Ans)
        return
# b=Boiler('Model',11.2,0.98)
# print b.emissions
