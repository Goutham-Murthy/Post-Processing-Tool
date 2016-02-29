# -*- coding: utf-8 -*-
import annuity
import database


class SolarThermal(annuity.Annuity):
    """
    Class representing Solar Thermal Collectors.

    Attributes:
        model: Model of the solar thermal collector module
        area: Area of the solar thermal collector module [m2]
        global_radiation: Hourly values of thermal radiation
        heat_hourly: Hourly values of electricity given by the solar thermal unit [kWh]
        heat_yearly: Sum value of heat provided by the solar thermal unit over the year [kWh].
        annuity: Annuity of the solar thermal unit [Euros].
        emissions: CO2 emissions of the solar thermal unit[kg of CO2].
    Extends:
        Annuity class

    """
    def __init__(self, model, area, global_radiation):
        """
        Constructor class for the solar thermal unit.

        :param model: Model of the solar thermal collector
        :param area: Area of the collector
        :return: none
        """
        self.model = model
        self.area = area
        self.global_radiation = global_radiation
        # Initialising other variables to zero.
        self.heat_hourly = [0]*8761
        self.heat_yearly = 0
        self.annuity = 0
        self.emissions = 0
        super(SolarThermal, self).__init__(deperiod=database.annuity_factors['SolTh'][0],
                                           effop=database.annuity_factors['SolTh'][1],
                                           fwins=database.annuity_factors['SolTh'][2],
                                           finst=database.annuity_factors['SolTh'][3],
                                           obperiod=database.annuity_factors['Common'][0],
                                           q=database.annuity_factors['SolTh'][4],
                                           r=database.annuity_factors['SolTh'][5],
                                           gas_price=database.annuity_factors['Common'][1],
                                           electricity_price=database.annuity_factors['Common'][2])

    def get_heat(self, required_heat, hour, ThSt=None):
        """
        Given the required heat, function calculates the hourly heat met by the solar thermal unit and returns the value
         for unsatisfied thermal demand.

        :param required_heat: Hourly heat demand of the building[kWh].
        :param hour: Hour of the year
        :param ThSt: Thermal Storage instance when present.
        :return: required_heat: Hourly thermal demand not met by the solar thermal unit [kWh].
        """
        self.heat_hourly[hour] = 0.7*self.area*self.global_radiation[hour]
        if ThSt is not None:
            if required_heat < self.heat_hourly[hour]:
                # Excess heat can be stored in the storage unit.
                # Check for availability of thermal storage unit.
                if (self.heat_hourly[hour] - required_heat) <= ThSt.get_ThSt_avaiability(hour):
                    ThSt.store_heat((self.heat_hourly[hour] - required_heat), hour)
                    required_heat = 0
                    self.heat_yearly += self.heat_hourly[hour]
                # If not available, store as much as possible and excess heat is wasted
                else:
                    self.heat_hourly[hour] = ThSt.get_ThSt_avaiability(hour) + required_heat
                    ThSt.store_heat(self.heat_hourly[hour] - required_heat, hour)
                    required_heat = 0
                    self.heat_yearly += self.heat_hourly[hour]
            # If thermal demand is greater than capacity meet it as much as
            # possible.
            else:
                self.heat_yearly += self.heat_hourly[hour]
                required_heat -= self.heat_hourly[hour]
        # if thermal storage is not present
        else:
            # Excess heat is wasted. Demand is met as production is more.
            if required_heat < self.heat_hourly[hour]:
                self.heat_hourly[hour] = required_heat
                self.heat_yearly += self.heat_hourly[hour]
                required_heat = 0
            else:
                print self.heat_yearly, self.heat_hourly[hour], hour
                self.heat_yearly += self.heat_hourly[hour]
                required_heat -= self.heat_hourly[hour]
        return required_heat

    def set_annuity(self):
        """
        Calculates the annuity of the solar thermal unit

        :param: none
        :return: none
        """
        # Capital related costs for the boiler include price of purchase and
        # installation costs.
        self.A0 = 442.8*self.area + 1000
        self.set_ank()

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
