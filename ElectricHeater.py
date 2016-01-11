# -*- coding: utf-8 -*-
class ElectricHeater:
    """Electric Heater class
    
    Attributes:
    model : Model of the Electric Heater
    thermal_capacity : Thermal capacity of the Electric Heater [kWh]
    efficiency : Efficiency of the Electric Heater [decimal<1]
    heat: Heat provided by the Electric Heater unit [kWh]
    heat_hourly : Hourly values of the heat provided by the Electric Heater unit [kWh]
    annuity : Annuity of the Electric Heater"""

    def __init__(self,model,thermal_capacity, efficiency):
        self.model = model
        self.thermal_capacity = thermal_capacity
        self.efficiency = efficiency
        self.heat_hourly = [0]*8760
        self.heat = 0
        print 'Elhe-',thermal_capacity
    
    def getElHeHeat(self,required_heat,hour):
        if required_heat <= self.thermal_capacity:
            self.heat += required_heat
            self.heat_hourly[hour] = required_heat
            required_heat = 0
            return required_heat
        else:
            self.heat += self.thermal_capacity
            self.heat_hourly[hour] = self.thermal_capacity
            required_heat -= self.thermal_capacity
            return required_heat

