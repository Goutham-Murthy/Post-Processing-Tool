# -*- coding: utf-8 -*-
import Annuity

class ElectricHeater:
    """Electric Heater class
    
    Attributes:
    model : Model of the Electric Heater
    thermal_capacity : Thermal capacity of the Electric Heater [kW]
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
        self.annuity = 0
    
    def getHeat(self,required_heat,hour):
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
    
    def getEmissions(self):
        return 760
        
    def getAnnuity(self):
        obperiod = 10
        q = 1.07
        r = 1.03
        b = Annuity.getb(q=q,r=r,obperiod=obperiod)
        bv = b
        bb = Annuity.getb(q=q,r=1.02,obperiod=obperiod)
        bi = b
        deperiod = 15
        finst = 0.01
        fwins = 0.01
        effop = 5
        
        a = Annuity.getAnnuityFactor(q=q,obperiod=obperiod)
        #Capital related costs for the electrical heater include price of purchase and installation costs
        CRC = 53.938*(self.thermal_capacity*1000)**0.2685
        Ank = Annuity.getAnk(A0=CRC,r=r,q=q,obperiod=obperiod,deperiod=deperiod)
    
        #Demand related costs include price of fuel to generate the required heat
        DRC = self.heat*0.26
        Anv = DRC*a*bv
    
        #Operation related costs include maintanance and repair
        ORC = 30*effop
        Ain = CRC*(finst+fwins)
        Anb = ORC*a*bb + Ain*a*bi
        #Other costs
        Ans = 0
        
        #Proceeds 
        Ane = 0
        #print 'Electric Heater'
        #print 'A0=Investment amount=',CRC
        #print 'Ank=Capital Realted Annuity=',Ank
        #print 'Anv=Demand Related Annuity=',Anv
        #print 'Anb=Operation Related Annuity=',Anb
        #print 'Ane=Proceeds through feed-in-tariff=',Ane    
        A = Ane - (Ank+Anv+Anb+Ans)
        self.annuity = A
        return A 