# -*- coding: utf-8 -*-
import annuity


class CHP(annuity.Annuity):
    """Class representing CHP technology.

    Attributes:
    model (string)              : Model of the boiler.
    thermal_capacity (float)    : Thermal capacity of the CHP [kW].
    electrical_capacity (float) : Electrical capacity of the CHP unit [kW].
    th_efficiency (float)       : Thermal efficiency of the CHP [decimal<1].
    el_efficiency (float)       : Electrical efficiency of the CHP [decimal<1].
    heat_yearly (float)         : Heat provided by the CHP unit over the
                                 year[kWh].
    heat_hourly (float)         : Hourly values of the heat demand met by
                                 the CHP unit [kWh].
    annuity                     : Annuity of the CHP [Euros].
    """

    def __init__(self, model, thermal_capacity, electrical_capacity,
                 th_efficiency, el_efficiency):
        self.model = model
        self.thermal_capacity = thermal_capacity
        self.electrical_capacity = electrical_capacity
        self.th_efficiency = th_efficiency
        self.el_efficiency = el_efficiency
        # Initialising other variables to zero.
        self.heat_hourly = [0]*8760
        self.heat = 0
        self.annuity = 0
        print 'CHP-', thermal_capacity

    def getEmissions(self):
        return 760
        
    @abc.abstractmethod
    def getCHPHeat(self,required_heat,storage_capacity):
        pass

class OnOffCHP(CHP):
    
    def getHeat(self,required_heat,hour):
        if required_heat < self.thermal_capacity:
            return required_heat
        else:
            self.heat += self.thermal_capacity
            self.heat_hourly[hour] = self.thermal_capacity
            required_heat -= self.thermal_capacity
            return required_heat
            
    def getAnnuity(self,storage=False):
        obperiod = 10
        q = 1.07
        r = 1.03
        b = Annuity.getb(q=q,r=r,obperiod=obperiod)
        bv = b
        bb = Annuity.getb(q=q,r=1.02,obperiod=obperiod)
        bi = b
        deperiod = 15
        effop = 10
        fwins = 0.01
        finst = 0.01
        be = b
    
        #This is price per kWel.
        bonus = self.getCHPBonus()
    
        #Taken fron ASUE data of 2015. Gives euro/kwel
        if self.electrical_capacity <= 10:
            CRC = 9.585*self.electrical_capacity**(-0.542)
        elif self.electrical_capacity>10 and self.electrical_capacity <=100:
            CRC = 5.438*self.electrical_capacity**(-0.351)
        elif self.electrical_capacity>100 and self.electrical_capacity <=1000:
            CRC = 4.907*self.electrical_capacity**(-0.352)
        else:
            CRC = 1.7*460.89*self.electrical_capacity**(-0.015)
        
        #Multiplying to get euros
        CRC = CRC*self.electrical_capacity*1000*1.4
        a = Annuity.getAnnuityFactor(q=q,obperiod=obperiod)
    
        #Capital related costs for the CHP include price of purchase and installation costs
        if storage:
            Ank = Annuity.getAnk(A0=CRC-bonus,r=r,q=q,obperiod=obperiod,deperiod=deperiod)
        else:
            Ank = Annuity.getAnk(A0=CRC,r=r,q=q,obperiod=obperiod,deperiod=deperiod)
    
        #Demand related costs include price of fuel to generate the required heat
        DRC = 0.0615*self.heat/self.th_efficiency
        Anv = DRC*a*bv
    
        #Operation related costs include maintanance and repair
        #ORC = 30*effop
        #Ain = CRC*(finst+fwins)
        #Anb = ORC*a*bb + Ain*a*bi
        if self.electrical_capacity>0 and self.electrical_capacity<10:
            ORC=(3.2619*self.electrical_capacity**0.1866)*self.heat/self.th_efficiency*self.el_efficiency/100
        elif self.electrical_capacity>=10 and self.electrical_capacity<100:
            ORC=(6.6626*self.electrical_capacity**-0.25)*self.heat/self.th_efficiency*self.el_efficiency/100
        elif self.electrical_capacity>=100 and self.electrical_capacity<1000:
            ORC=(6.2728*self.electrical_capacity**-0.283)*self.heat/self.th_efficiency*self.el_efficiency/100
        Anb=ORC*a*bb
        #Other costs
        Ans = 0
        
        #Proceeds
        E1= self.heat/self.th_efficiency*self.el_efficiency*0.10#*0.5 + 0.5*.3)
        Ane = E1*a*be
        E12 = self.heat/self.th_efficiency*self.el_efficiency*.3
        Ane2 = E12*a*be
        A = Ane - (Ank+Anv+Anb+Ans)
        #    print 'CHP'
        #    print 'A0=Investment amount=',CRC
        #    print 'Ank=Capital Realted Annuity=',Ank
        #    print 'Anv=Demand Related Annuity=',Anv
        #    print 'Anb=Operation Related Annuity=',Anb
        #    print 'Ane=Proceeds through feed-in-tariff=',Ane
        #    print 'Ane=Proceeds total self consumption=',Ane2 
        self.annuity = A
        return a,CRC,bonus,Ank,Anv,Anb,Ane,A 


    def getCHPBonus(self):
        if self.electrical_capacity>0 and self.electrical_capacity<=1:
            factor = 1900
        elif self.electrical_capacity>1 and self.electrical_capacity<=4:
            factor = 300
        elif self.electrical_capacity>4 and self.electrical_capacity<=10:
            factor = 100
        elif self.electrical_capacity>10 and self.electrical_capacity<=20:
            factor = 10
        else:
            factor = 1000000000
            
        if self.electrical_capacity>0 and self.electrical_capacity<=1:
            bonus = 1900
        elif self.electrical_capacity>1 and self.electrical_capacity<=2:
            bonus = 1900 + (self.electrical_capacity-1)*factor
        elif self.electrical_capacity>2 and self.electrical_capacity<=5:
            bonus = 2200 + (math.floor(self.electrical_capacity)-2)*300 + (self.electrical_capacity-math.floor(self.electrical_capacity))*factor
        elif self.electrical_capacity>5 and self.electrical_capacity<=11:
            bonus = 2900 + (math.floor(self.electrical_capacity)-5)*100 + (self.electrical_capacity-math.floor(self.electrical_capacity))*factor
        elif self.electrical_capacity>11 and self.electrical_capacity<=20:
            bonus = 3410 + (math.floor(self.electrical_capacity)-11)*10 + (self.electrical_capacity-math.floor(self.electrical_capacity))*factor
        else:
            bonus = 0
        
        bonus = bonus*1.25
        return bonus