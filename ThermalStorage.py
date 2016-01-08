# -*- coding: utf-8 -*-
class ThermalStorage:
    """Thermal Storage class
    
    Attributes:
    model : Model of the thermal storage
    thermal_capacity : Thermal capacity of the thermal storage [kWh]
    thermal_capacity_l : Thermal capacity of the thermal storage [liters]
    losses :Losses incurred as percentage of heat present [%]
    heat: Heat stored in the thermal storage [kWh]
    heat_hourly : Hourly values of the heat provided by the thermal storage unit [kWh]
    annuity : Annuity of the Thermal Storage"""

    def __init__(self,model,thermal_capacity, losses):
        self.model = model
        self.thermal_capacity = thermal_capacity
        self.losses = losses
        self.heat_hourly = 0
        self.heat = 0
        self.annuity = 0
    
    def getThStHeat(self,required_heat):
        if required_heat <= self.heat:
            self.heat -= required_heat
            self.heat_hourly = required_heat
            required_heat = 0
            return required_heat
        else:
            self.heat_hourly = self.heat
            required_heat -= self.heat
            self.heat = 0
            return required_heat
            
    def storeThStHeat(self,store_heat):
        self.heat += store_heat