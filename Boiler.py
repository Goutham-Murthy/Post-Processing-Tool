# -*- coding: utf-8 -*-
class Boiler:
    """Boiler class
    
    Attributes:
    model : Model of the boiler
    thermal_capacity : Thermal capacity of the boiler [kWh]
    efficiency : Efficiency of the boiler [decimal<1]
    heat: Heat provided by the boiler unit [kWh]
    heat_hourly : Hourly values of the heat provided by the boiler unit [kWh]
    annuity : Annuity of the boiler"""

    def __init__(self,model,thermal_capacity, efficiency):
        self.model = model
        self.thermal_capacity = thermal_capacity
        self.efficiency = efficiency
        self.heat_hourly = 0
        self.heat = 0
        self.annuity = 0
    
    def getBoilerHeat(self,required_heat):
        if required_heat <= self.thermal_capacity:
            self.heat += required_heat
            self.heat_hourly = required_heat
            required_heat = 0
            return required_heat
        else:
            self.heat += self.thermal_capacity
            self.heat_hourly = self.thermal_capacity
            required_heat -= self.thermal_capacity
            return required_heat