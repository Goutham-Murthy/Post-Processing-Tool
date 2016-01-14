# -*- coding: utf-8 -*-
import annuity

class Boiler:
    """Boiler class
    
    Attributes:
    model: Model of the boiler
    thermal_capacity : Thermal capacity of the boiler [kWh]
    efficiency : Efficiency of the boiler [decimal<1]
    heat_yearly : Heat provided by the boiler unit [kWh]
    heat_hourly : Hourly values of the heat provided by the boiler unit [kWh]
    annuity : Annuity of the boiler"""

    def __init__(self, model, thermal_capacity, efficiency):
        self.model = model
        self.thermal_capacity = thermal_capacity
        self.efficiency = efficiency
        self.heat_hourly = [0]*8760
        self.heat_yearly = 0
        self.annuity = 0
        
    def get_heat(self,required_heat,hour):
        if required_heat <= self.thermal_capacity:
            self.heat_yearly += required_heat
            self.heat_hourly[hour] = required_heat
            required_heat = 0
            return required_heat
        else:
            self.heat_yearly += self.thermal_capacity
            self.heat_hourly[hour] = self.thermal_capacity
            required_heat -= self.thermal_capacity
            return required_heat
        
    def get_emissions(self):
        emissions = 201.6*self.heat_yearly
        return (emissions/1000)
        
    def get_annuity(self):
        obperiod = 10 #VDI2067
        
        #The following factors are assumed. For boilers and other technologies
        q = 1.07
        r = 1.03
        b = annuity.getb(q=q,r=r,obperiod=obperiod)
        bv = b
        bb = annuity.getb(q=q,r=1.02,obperiod=obperiod)
        bi = b

        #The deprecition period, finst,fwins and effop are different for different capacitites according to 
        #VDI 2067    
        if self.thermal_capacity < 100:
            deperiod = 18
            finst = 0.015
            fwins = 0.015
            effop = 10
        elif self.thermal_capacity in range(100,200):
            deperiod = 20
            finst = 0.01
            fwins = 0.015
            effop = 20
        else:
            deperiod = 20
            finst = 0.01
            fwins = 0.02
            effop = 20
    
        a = annuity.get_annuity_factor(q=q,obperiod=obperiod)
        #Capital related costs for the boiler include price of purchase and installation costs
        CRC = 79.061*self.thermal_capacity + 1229.8
        Ank = annuity.get_Ank(A0=CRC,r=r,q=q,obperiod=obperiod,deperiod=deperiod)
    
        #Demand related costs include price of fuel to generate the required heat
        DRC = 0.067*self.heat/self.efficiency
        Anv = DRC*a*bv
        
        #Operation related costs include maintanance and repair
        ORC = 30*effop
        Ain = CRC*(finst+fwins)
        Anb = ORC*a*bb + Ain*a*bi
    
        #Other costs
        Ans = 0
        
        #Proceeds
        Ane = 0
        A = Ane - (Ank+Anv+Anb+Ans)
        self.annuity = A
        return CRC,Ank,Anv,Anb,A 