# -*- coding: utf-8 -*-
import annuity
import abc
import math


class CHP(annuity.Annuity):
    """Class representing CHP technology.

    Attributes:
        model (string)          : Model of the boiler.
        th_capacity (float)     : Thermal capacity of the CHP [kW].
        el_capacity (float)     : Electrical capacity of the CHP unit [kW].
        th_efficiency (float)   : Thermal efficiency of the CHP [<1].
        el_efficiency (float)   : Electrical efficiency of the CHP [<1].
        heat_yearly (float)     : Heat provided by the CHP unit over the
                                 year[kWh].
        heat_hourly (float)     : Hourly values of the heat demand met by
                                 the CHP unit [kWh].
        annuity                 : Annuity of the CHP [Euros].
        deperiod(float)         : Depreciation period [years].
        finst(float)            : Effort for annual repairs as percentage
                                 of initial investment [%].
        fwins(float)            : Effort for annual maintenance and inspection
                                 as percentage of total investment [%].
        effop(float)            : Effort for operation [hours/annum].
    Extends:
        Annuity class
    """

    def __init__(self, model, th_capacity, el_capacity,
                 th_efficiency, el_efficiency):
        """Constructor method for class CHP.

        Args:
            model (string)          : Model of the CHP unit.
            th_capacity (float)     : Thermal capacity of the CHP [kW].
            el_capacity (float)     : Electrical capacity of the CHP [kW].
            th_efficiency (float)   : Thermal efficiency of the CHP[decimal<1].
            el_efficiency (float)   : Electrical efficiency of the CCHP unit.
        """
        self.model = model
        self.th_capacity = th_capacity
        self.el_capacity = el_capacity
        self.th_efficiency = th_efficiency
        self.el_efficiency = el_efficiency
        # Initialising other variables to zero.
        self.emissions = 0
        self.annuity = 0
        self.bonus = 0
        self.heat_hourly = [0]*8760
        self.heat_yearly = 0
        self.annuity = 0
        super(CHP, self).__init__(deperiod=15, effop=10, fwins=1, finst=1)

    def set_emissions(self):
        """
        Calculates the CO2 emissions of the CHP unit.

        Args:
            None.

        Returns:
            None.
        """
        # emissions = (180*self.heat_yearly - 595*self.heat_yearly*.3)/.6
        self.emissions = (2.5*self.heat_yearly/1000)
        return

    def set_annuity(self, storage=False):
        """
        Calculates the annuity of the boiler.

        Args:
            None.

        Returns:
            None..
        """
        # Capital related costs for the CHP include price of purchase and
        # installation costs
        # This is price per kWel.
        # Taken fron ASUE data of 2015. Gives euro/kwel
        if self.el_capacity <= 10:
            CRC = 9.585*self.el_capacity**(-0.542)
        elif (self.el_capacity > 10 and
              self.el_capacity <= 100):
            CRC = 5.438*self.el_capacity**(-0.351)
        elif (self.el_capacity > 100 and
              self.el_capacity <= 1000):
            CRC = 4.907*self.el_capacity**(-0.352)
        else:
            CRC = 1.7*460.89*self.el_capacity**(-0.015)

        # Multiplying to get euros
        self.A0 = CRC*self.el_capacity*1000*1.4

        # No bonus if storage is not present.
        if storage:
            self.set_CHP_Bonus()
        self.A0 -= self.bonus
        self.set_Ank()

        # Demand related costs include price of fuel to generate the required
        # heat. Excluding energy tax of .55 cents frmo gas price
        DRC = (self.gas_price - 0.0055)*self.heat_yearly/self.th_efficiency
        self.Anv = DRC*self.a*self.bv

        # Operation related costs include maintanance and repair
        # ORC = 30*effop
        # Ain = CRC*(finst+fwins)/100
        # Anb = ORC*a*bb + Ain*a*bi
        if self.el_capacity > 0 and self.el_capacity < 10:
            ORC = ((3.2619 * self.el_capacity**0.1866) * self.heat_yearly /
                   self.th_efficiency * self.el_efficiency / 100)
        elif self.el_capacity >= 10 and self.el_capacity < 100:
            ORC = ((6.6626 * self.el_capacity**-0.25) *
                   self.heat_yearly/self.th_efficiency*self.el_efficiency/100)
        elif (self.el_capacity >= 100 and
              self.el_capacity < 1000):
            ORC = ((6.2728 * self.el_capacity**-0.283) *
                   self.heat_yearly/self.th_efficiency*self.el_efficiency/100)
        self.Anb = ORC*self.a*self.bb

        # Other costs
        self.Ans = 0

        # Proceeds
        E1 = self.heat_yearly/self.th_efficiency*self.el_efficiency*0.10
        self.Ane = E1*self.a*self.be

        self.annuity = self.Ane - (self.Ank + self.Anv + self.Anb + self.Ans)
        return

    def set_CHP_Bonus(self):
        if self.el_capacity > 0 and self.el_capacity <= 1:
            factor = 1900
        elif self.el_capacity > 1 and self.el_capacity <= 4:
            factor = 300
        elif self.el_capacity > 4 and self.el_capacity <= 10:
            factor = 100
        elif self.el_capacity > 10 and self.el_capacity <= 20:
            factor = 10
        else:
            factor = 1000000000

        if self.el_capacity > 0 and self.el_capacity <= 1:
            bonus = 1900
        elif self.el_capacity > 1 and self.el_capacity <= 2:
            bonus = 1900 + (self.el_capacity-1)*factor
        elif self.el_capacity > 2 and self.el_capacity <= 5:
            bonus = 2200 + (math.floor(self.el_capacity)-2)*300 +\
                (self.el_capacity -
                 math.floor(self.el_capacity))*factor
        elif self.el_capacity > 5 and self.el_capacity <= 11:
            bonus = 2900 + (math.floor(self.el_capacity)-5)*100 +\
                (self.el_capacity -
                 math.floor(self.el_capacity))*factor
        elif self.el_capacity > 11 and self.el_capacity <= 20:
            bonus = 3410 + (math.floor(self.el_capacity)-11)*10 +\
                (self.el_capacity -
                 math.floor(self.el_capacity))*factor
        else:
            bonus = 0

        self.bonus = bonus*1.25
        return

    @abc.abstractmethod
    def get_heat(self,  required_heat, hour, ThSt=None):
        pass


class OnOffCHP(CHP):

    def get_heat(self, required_heat, hour, ThSt=None):
        """
        Given the required heat, function calculates the hourly heat met by the
        CHP and returns the value for unsatified thermal demand.

        Args:
            ThSt(class Thst)        : Thermal Storage instance when present.
            required_heat (float)   : Hourly heat demand of the building
                                         [kWh].
            hour (int)              : Hour of the year.

        Returns:
            required_heat (float)   : Hourly thermal demand not met by the
                                         CHP unit [kWh].
        """
        if ThSt is not None:
            if required_heat < self.th_capacity:
                # Excess heat can be stored in the storage unit.
                # Check for availability of thermal storage unit.
                if (self.th_capacity - required_heat) <= ThSt.get_ThSt_avaiability(hour):
                    ThSt.store_heat((self.th_capacity - required_heat),
                                    (hour))
                    required_heat = 0
                    self.heat_yearly += self.th_capacity
                    self.heat_hourly[hour] = self.th_capacity
                # If not available, do nothing.
            else:
                self.heat_yearly += self.th_capacity
                self.heat_hourly[hour] = self.th_capacity
                required_heat -= self.th_capacity
            # If thermal demand is greater than capacity meet it as much as
            # possible.
        else:
            if required_heat < self.th_capacity:
                pass
            else:
                self.heat_yearly += self.th_capacity
                self.heat_hourly[hour] = self.th_capacity
                required_heat -= self.th_capacity
        return required_heat

# CHP = OnOffCHP('YahooCHP', 2.7, 1, 0.6, 0.3)
# CHP.get_heat(3, 31)
