# -*- coding: utf-8 -*-
import abc

class CHP:
    """CHP class
    
    Attributes:
    model : Model of the boiler
    thermal_capacity : Thermal capacity of the CHP [kWh]
    th_efficiency : Thermal efficiency of the CHP [decimal<1]
    el_efficiency : Electrical efficiency of the CHP [decimal<1]
    heat: Heat provided by the CHP unit [kWh]
    heat_hourly : Hourly values of the heat provided by the CHP unit [kWh]
    annuity : Annuity of the CHP"""

    def __init__(self,model,thermal_capacity, th_efficiency, el_efficiency):
        self.model = model
        self.thermal_capacity = thermal_capacity
        self.th_efficiency = th_efficiency
        self.el_efficiency = el_efficiency
        self.heat_hourly = [0]*8760
        self.heat = 0
        self.annuity = 0
        print 'CHP-',thermal_capacity
        
    @abc.abstractmethod
    def getCHPHeat(self,required_heat,storage_capacity):
        pass

class OnOffCHP(CHP):
    
    def getCHPHeat(self,required_heat,hour):
        if required_heat < self.thermal_capacity:
            return required_heat
        else:
            self.heat += self.thermal_capacity
            self.heat_hourly[hour] = self.thermal_capacity
            required_heat -= self.thermal_capacity
            return required_heat