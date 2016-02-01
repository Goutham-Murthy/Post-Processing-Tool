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
    Extends:
        Annuity class
    """

    def __init__(self, model):
        """Constructor method for class CHP.

        Args:
            model (string)          : Model of the CHP unit.
        """
        self.model_name = model[0]
        self.th_capacity = model[1]
        self.th_efficiency = model[2]
        self.el_efficiency = model[3]
        self.el_capacity = self.th_capacity/self.th_efficiency*self.el_efficiency
        # Initialising other variables to zero.
        self.emissions = 0
        self.annuity = 0
        self.bonus = 0
        self.heat_hourly = [0]*8760
        self.heat_yearly = 0
        self.electricity_yearly = 0
        self. electricity_hourly = [0]*8760
        self.electricity_hourly_exported = [0]*8760
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
        :param storage: If storage is present or not
        :return: none
        """
        # Capital related costs for the CHP include price of purchase and
        # installation costs
        # This is price per kWel.
        # Taken from ASUE data of 2015. Gives euro/kWel
        if self.el_capacity <= 10:
            crc = 9.585*self.el_capacity**(-0.542)
        elif 10 < self.el_capacity <= 100:
            crc = 5.438*self.el_capacity**(-0.351)
        elif 100 < self.el_capacity <= 1000:
            crc = 4.907*self.el_capacity**(-0.352)
        else:
            crc = 1.7*460.89*self.el_capacity**(-0.015)

        # Multiplying to get euros
        self.A0 = crc*self.el_capacity*1000*1.4

        # No bonus if storage is not present.
        if storage:
            self.set_chp_bonus()
        self.A0 -= self.bonus
        self.set_Ank()

        # Demand related costs include price of fuel to generate the required
        # heat. Excluding energy tax of .55 cents from gas price
        drc = (self.gas_price - 0.0055)*self.heat_yearly/self.th_efficiency
        self.Anv = drc*self.a*self.bv

        # Operation related costs include maintenance and repair
        # ORC = 30*effop
        # Ain = CRC*(finst+fwins)/100
        # Anb = ORC*a*bb + Ain*a*bi
        orc = 0
        if 0 < self.el_capacity < 10:
            orc = ((3.2619 * self.el_capacity**0.1866) * self.heat_yearly /
                   self.th_efficiency * self.el_efficiency / 100)
        elif 10 <= self.el_capacity < 100:
            orc = ((6.6626 * self.el_capacity**-0.25) *
                   self.heat_yearly/self.th_efficiency*self.el_efficiency/100)
        elif 100 <= self.el_capacity < 1000:
            orc = ((6.2728 * self.el_capacity**-0.283) *
                   self.heat_yearly/self.th_efficiency*self.el_efficiency/100)
        self.Anb = orc*self.a*self.bb

        # Other costs
        self.Ans = 0

        # Proceeds
        e1 = self.heat_yearly/self.th_efficiency*self.el_efficiency*0.10
        self.Ane = e1*self.a*self.be

        self.annuity = self.Ane - (self.Ank + self.Anv + self.Anb + self.Ans)
        return

    def set_chp_bonus(self):
        if 0 < self.el_capacity <= 1:
            factor = 1900
        elif 1 < self.el_capacity <= 4:
            factor = 300
        elif 4 < self.el_capacity <= 10:
            factor = 100
        elif 10 < self.el_capacity <= 20:
            factor = 10
        else:
            factor = 1000000000

        if 0 < self.el_capacity <= 1:
            bonus = 1900
        elif 1 < self.el_capacity <= 2:
            bonus = 1900 + (self.el_capacity-1)*factor
        elif 2 < self.el_capacity <= 5:
            bonus = 2200 + (math.floor(self.el_capacity)-2)*300 + (self.el_capacity -
                                                                   math.floor(self.el_capacity))*factor
        elif 5 < self.el_capacity <= 11:
            bonus = 2900 + (math.floor(self.el_capacity)-5)*100 + (self.el_capacity -
                                                                   math.floor(self.el_capacity))*factor
        elif 11 < self.el_capacity <= 20:
            bonus = 3410 + (math.floor(self.el_capacity)-11)*10 + (self.el_capacity -
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
        CHP and returns the value for unsatisfied thermal demand.

        Args:
            ThSt(class ThSt)        : Thermal Storage instance when present.
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
                if (self.th_capacity - required_heat) <= ThSt.get_availability(hour):
                    ThSt.store_heat((self.th_capacity - required_heat), hour)
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
                self.heat_hourly[hour] = 0
            else:
                self.heat_yearly += self.th_capacity
                self.heat_hourly[hour] = self.th_capacity
                required_heat -= self.th_capacity
        return required_heat

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
        self.electricity_hourly[hour] = self.el_efficiency * self.heat_hourly[hour] / self.th_efficiency
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
# CHP = OnOffCHP('YahooCHP', 2.7, 1, 0.6, 0.3)
# CHP.get_heat(3, 31)
