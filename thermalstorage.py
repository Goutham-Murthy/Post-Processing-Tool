# -*- coding: utf-8 -*-
import annuity


class ThermalStorage(annuity.Annuity):
    """
    Class representing Thermal Storage technologgy.

    Attributes:
        model (string)          : Model of the thermal storage unit.
        th_capacity (float)     : Thermal capacity of the stortage unit [kWh].
        loss_percent (float)    : Percentage of heat lost in the thermal
                                 storage unit over each hour [%].
        heat_stored (float)     : Heat present in the thermal storage unit
                                 at the beginning of hour [kWh].
        heat_hourly (float)     : Hourly values of the heat provided by the
                                 thermal storage unit [kWh].
        annuity (float)         : Annuity of the thermal storage unit [Euros].
        losses (float)          : Total heat losses from the thermal storage
                                 unit [kWh]
        deperiod(float)         : Depreciation period [years].
        finst(float)            : Effort for annual repairs as percentage of
                                 initial investment [%].
        fwins(float)            : Effort for annual maintenance and inspection
                                 as percentage of total investment [%].
        effop(float)            : Effort for operation [hours/annum].

    Extends:
        Annuity class
    """

    def __init__(self, model, th_capacity, loss_percent):
        """Constructor method for class thermal storage.

        Args:
            model (string)          : Model of the thermal storage unit.
            th_capacity (float)     : Thermal capacity of the storage unit
                                     [kWh].
            loss_percent (float)    : Percentage of heat lost in the thermal
                                     storage unit over each hour [decimal<1].
        """
        self.model = model
        self.th_capacity = th_capacity
        self.loss_percent = loss_percent
        # Initialising other variables to zero.
        self.heat_stored = [0]*8761
        self.heat_hourly = [0]*8760
        self.annuity = 0
        self.losses = 0
        self.deperiod = 15
        self.finst = 2
        self.fwins = 1
        self.effop = 0
        annuity.Annuity.__init__(self)

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
        if required_heat <= self.heat_stored[hour]:
            self.heat_hourly[hour] = required_heat
            self.heat_stored[hour] -= required_heat
            required_heat = 0
        # If hourly thermal demand is grreater than the capacity, meet as much
        # as possible.
        else:
            self.heat_hourly[hour] = self.heat_stored[hour]
            required_heat -= self.heat_stored[hour]
            self.heat_stored[hour] = 0
        return required_heat

    def set_annuity(self):
        """
        Calculates the annuity of the thermal storage unit.

        Args:
            None.

        Returns:
            None
        """
        th_capacity_l = self.get_ThSt_Cap_l()

        if th_capacity_l > 1000:
            bonus = 250*th_capacity_l/1000
        else:
            bonus = 0
        # Capital related costs for the boiler include price of purchase and
        # installation costs.
        self.A0 = 1.0912*th_capacity_l + 367.92 - bonus
        self.set_Ank()

        # Demand related costs include price of fuel to produce required heat
        DRC = 0
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

    def get_ThSt_Cap_l(self):
        """
        Given the thermal capacity of the storage unit in kWh, return the
        capacity in liters.

        Args:
            None
        Returns:
            th_capacity_l   : Thermal capacity of storage unit in liters.
        """
        th_capacity_l = self.th_capacity*3600000/(4180*40)
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
        self.heat_stored[hour] = heat + self.heat_stored[hour]
        return

    def get_ThSt_avaiability(self, hour):
        return (self.th_capacity - self.heat_stored[hour])

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
