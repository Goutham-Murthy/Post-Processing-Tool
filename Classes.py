# -*- coding: utf-8 -*-
class Boiler:
    """Boiler class
    
    Attributes:
    model : Model of the boiler
    thermal_capacity : Thermal capacity of the boiler in kWh
    efficiency : Efficiency of the boiler
    boiler_heat: Heat in kWh of the fuel used by the boiler to provide heat"""

    def __init__(self,model,thermal_capacity, efficiency):
        self.model = model
        self.thermal_capacity = thermal_capacity
        self.efficiency = efficiency
        self.B_heat_hourly = 0
        self.B_heat = 0
    
    def getBoilerHeat(self,required_heat):
        if required_heat <= self.thermal_capacity:
            self.B_heat += required_heat
            self.B_heat_hourly = required_heat
            required_heat = 0
            return required_heat
        else:
            self.B_heat += self.thermal_capacity
            self.B_heat_hourly = self.thermal_capacity
            required_heat -= self.thermal_capacity
            return required_heat
