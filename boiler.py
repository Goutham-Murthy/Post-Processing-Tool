# -*- coding: utf-8 -*-
"""
Module consists class representing boilers.
"""
import annuity


class Boiler(annuity.Annuity):
    """Class representing boiler technology.

    Attributes:
        model (string)          : Model of the boiler.
        th_capacity (float): Thermal capacity of the boiler [kW].
        efficiency (float)      : Efficiency of the boiler [decimal<1].
        heat_yearly (float)     : Sum value of heat provided by the boiler unit
                                 over the year [kWh].
        heat_hourly (float)     : Hourly values of the heat provided by the
                                 boiler unit [kWh].
        annuity (float)         : Annuity of the boiler [Euros].
        emissions (float)       : CO2 emissions of the boiler [kg of CO2].
        deperiod(float)         : Depreciation period [years].
        finst(float)            : Effort for annual repairs as percentage of
                                 initial investment [%].
        fwins(float)            : Effort for annual maintenance and inspection
                                 as percentage of total investment [%].
        effop(float)            : Effort for operation [hours/annum].

    Extends:
        Annuity class
    """

    def __init__(self, model, th_capacity, efficiency):
        """Constructor method for class Boiler.

        Args:
            model (string)          : Model of the boiler.
            th_capacity (float)     : Thermal capacity of the boiler [kW].
            efficiency (float)      : Efficiency of the boiler [decimal<1].
        """
        self.model = model
        self.th_capacity = th_capacity
        self.efficiency = efficiency
        # Initialising other variables to zero.
        self.heat_hourly = [0]*8760
        self.heat_yearly = 0
        self.annuity = 0
        self.emissions = 0
        # The deprecition period, finst, fwins and effop are different for
        # different capacitites according to VDI 2067.
        if self.th_capacity < 100:
            self.deperiod = 18
            self.finst = 1.5
            self.fwins = 1.5
            self.effop = 10
        elif self.th_capacity in range(100, 200):
            self.deperiod = 20
            self.finst = 1.0
            self.fwins = 1.5
            self.effop = 20
        else:
            self.deperiod = 20
            self.finst = 1.0
            self.fwins = 2.0
            self.effop = 20

    def get_heat(self, required_heat, hour):
        """
        Given the required heat, function calculates the hourly heat met by
        the boiler and returns the value for unsatified thermal demand.

        Args:
            required_heat (float)   : Hourly heat demand of the building [kWh].
            hour (int)              : Hour of the year.

        Returns:
            required_heat (float)   : Hourly thermal demand not met by the
                                      boiler [kWh].
        """
        # If thermal capacity is more than hourly thermal demand, meet the
        # demand entirely.
        if required_heat <= self.th_capacity:
            self.heat_yearly += required_heat
            self.heat_hourly[hour] = required_heat
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
        DRC = self.gas_price*self.heat/self.efficiency
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
