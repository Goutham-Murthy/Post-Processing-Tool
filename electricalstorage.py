# -*- coding: utf-8 -*-
import annuity


class ElectricalStorage(annuity.Annuity):
    """
    Class for electrical storage technology. Heavy duty deep-cycle batteries considered.

    Attributes:
        model_name: (string)Model of the  electrical storage unit.
        storage_capacity: (float)Storage capacity of the electrical storage [kWh].
        loss_percent: (float)Loss percentage of the electrical storage unit [%].
        electricity_stored: (float) Hourly values of electricity stored in the storage unit [kWh]
        electricity_given: (float)Hourly values of electricity provided by the storage unit [kWh]
        annuity: (float)Annuity of the CHP [Euros].
        losses: (float)Total losses of the electrical storage unit in the year [kWh].
        max_el: (float)Maximum electrical power that can be stored in the storage in an hour [kWh].

    Extends:
        Annuity class
    """
    def __init__(self, model, storage_capacity, loss_percent):
        """
        Constructor method for class ElectricalStorage.

        :param model: Model of the electrical storage.
        :param storage_capacity: (float)Storage capacity of the storage unit[kWh].
        :param loss_percent: (float)Loss percentage of the storage capacity[%].
        :return: none
        """
        self.model_name = model
        self.storage_capacity = storage_capacity
        self.loss_percent = loss_percent
        # Initialising other variables to zero.
        self.electricity_stored = [0]*8761
        self.electricity_given = [0]*8760
        self.annuity = 0
        self.losses = 0
        self.max_el = 2
        super(ElectricalStorage, self).__init__(deperiod=5, effop=0, fwins=1.0, finst=0.5)

    def get_electricity(self, required_electricity, hour):
        """
        Method to keep track of electricity given and stored in the storage unit.

        :param required_electricity: (float)Unsatisfied electricity demand in the specified hour [kWh].
        :param hour: (float)hour.
        :return: required_electricity: (float)Unsatisfied electricity demand in the specified hour after electricity
                                       storage[kWh].
        """
        # If stored electricity is more than required electricity, meet the demand entirely.
        if required_electricity <= self.electricity_stored[hour]:
            self.electricity_given[hour] = required_electricity
            self.electricity_stored[hour] -= required_electricity
            required_electricity = 0
        # If hourly electricity demand is greater than the stored electricity, meet as much as possible.
        else:
            self.electricity_given[hour] = self.electricity_stored[hour]
            required_electricity -= self.electricity_stored[hour]
            self.electricity_stored[hour] = 0
        return required_electricity

    def set_annuity(self):
        """
        Annuity method for electric storage.

        :param: none
        :return: none
        """
        # Capital related costs for the battery include price of purchase and installation costs
        self.A0 = 0.1308*self.storage_capacity - 21.774
        self.set_ank()

        # Demand related costs include price of fuel to produce required heat
        self.Anv = 0

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

    def store_electricity(self, electricity, hour):
        """
        Method to store electricity in the electrical storage unit.

        :param electricity: (float)Excess electricity to be stored in the battery [kWh]
        :param hour: (float)hour [h]
        :return: none
        """
        self.electricity_stored[hour] += electricity
        return

    def get_availability(self, hour):
        """
        Calculates available storage capacity in the electrical storage unit.
        :param hour:  (float)hour [h]
        :return: storage_capacity: (float)Available storage capacity in the electrical storage unit[kWh].
        """
        return self.storage_capacity - self.electricity_stored[hour]

    def apply_losses(self, hour):
        """
        Method to calculate losses and re-initialise the values.

        :param hour: (float)hour [h]
        :return: none
        """
        # Carry over heat to next hour
        self.electricity_stored[hour] += (self.electricity_stored[hour-1] * (100-self.loss_percent)/100)
        self.losses += ((self.electricity_stored[hour-1]*self.loss_percent)/100)
        return
