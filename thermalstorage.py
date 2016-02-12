# -*- coding: utf-8 -*-
import annuity


class ThermalStorage(annuity.Annuity):
    """
    Class representing Thermal Storage technology.

    Attributes:
        model_name: (string)Model of the thermal storage unit.
        th_capacity: (float) Thermal capacity of the storage unit [kWh].
        loss_percent: (float) Percentage of heat lost in the thermal storage unit over each hour [%].
        heat_stored: (float) Heat present in the thermal storage unit at the beginning of hour [kWh].
        heat_given: (float) Hourly values of the heat provided by the thermal storage unit [kWh].
        annuity: (float) Annuity of the thermal storage unit [Euros].
        losses: (float) Total heat losses from the thermal storage unit [kWh]
    Extends:
        Annuity class
    """

    def __init__(self, model):
        """
        "
        Constructor method for class thermal storage.

        :param model: Tuple containing information about the thermal storage model in the
                       form (name, area, loss percentage)
        :return: none
        """
        print model
        self.model_name = model[0]
        self.th_capacity = model[1]
        self.loss_percent = model[2]
        # Initialising other variables to zero.
        self.heat_stored = [0]*8761
        self.heat_given = [0]*8760
        self.annuity = 0
        self.losses = 0
        super(ThermalStorage, self).__init__(deperiod=15, effop=0, fwins=1.0, finst=2.0)

    def get_heat(self, required_heat, hour):
        """
        Given the required heat, function calculates the hourly heat met by the thermal storage and returns the value
        for unsatisfied thermal demand.

        :param required_heat: (float)Hourly thermal demand [kWh].
        :param hour: (int)Hour of the year[hour].
        :return: required_heat: (float)Hourly thermal demand not met by the thermal storage unit [kWh].
        """
        # If thermal capacity is more than hourly thermal demand, meet the
        # demand entirely.
        if required_heat <= self.heat_stored[hour]:
            self.heat_given[hour] = required_heat
            self.heat_stored[hour] -= required_heat
            required_heat = 0
        # If hourly thermal demand is greater than the capacity, meet as much
        # as possible.
        else:
            self.heat_given[hour] = self.heat_stored[hour]
            required_heat -= self.heat_stored[hour]
            self.heat_stored[hour] = 0
        return required_heat

    def set_annuity(self):
        """
        Calculates the annuity of the thermal storage unit.

        :param: none
        :return: none
        """
        th_capacity_l = self.get_cap_l

        if th_capacity_l > 1000:
            bonus = 250*th_capacity_l/1000
        else:
            bonus = 0
        # Capital related costs for the boiler include price of purchase and
        # installation costs.
        self.A0 = 1.0912*th_capacity_l + 367.92 - bonus
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

    @property
    def get_cap_l(self):
        """
        Given the thermal capacity of the storage unit in kWh, return the capacity in liters.

        :return: th_capacity_l   : (float)Thermal capacity of storage unit in liters.
        """
        th_capacity_l = self.th_capacity*3600000 / (4180*40)
        return th_capacity_l

    def store_heat(self, heat, hour):
        """
        Method to store heat in the thermal storage unit. Method used by other
        active heat producing technologies like CHP, boiler etc.

        Args:
            heat    : Value of heat to be stored [kWh].
            hour    : Hour.
        Returns:
            None.
        """
        self.heat_stored[hour] += heat
        return

    def get_availability(self, hour):
        return self.th_capacity - self.heat_stored[hour]

    def apply_losses(self, hour):
        """
        Method to calculate losses and re-initialise the values.

        Args:
            hour    : Hour.

        Returns:
            None.
        """
        # Carry over heat to next hour
        self.heat_stored[hour] += (self.heat_stored[hour-1] *
                                   (100-self.loss_percent)/100)
        self.losses += ((self.heat_stored[hour-1]*self.loss_percent)/100)
