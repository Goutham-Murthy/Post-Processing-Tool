# -*- coding: utf-8 -*-
"""
Module consists class representing electric heaters.
"""
import annuity

class ElectricHeater:
    """Class representing Electric Heaters. Efficiency is approximated to 100%.
    
    Attributes:
        model (string) : Model of the Electric Heater.
        thermal_capacity (float): Thermal capacity of the Electric Heater [kW].
        heat_yearly (float): Sum value of heat provided by the electric heater unit over the year [kWh].
        heat_hourly (float) : Hourly values of the heat provided by the Electric Heater unit [kWh].
        annuity (float) : Annuity of the Electric Heater [Euros].
        emissions (float): CO2 emissions of the electric heater unit [kg of CO2].
        """
    def __init__(self,model,thermal_capacity):
        """ Constructor method for Electric Heater Class
        
        Args:
            model (string) : Model of the Electric Heater.
            thermal_capacity (float): Thermal capacity of the Electric Heater [kW].
        """
        self.model = model
        self.thermal_capacity = thermal_capacity
        # Initialising other variables to zero.
        self.heat_hourly = [0]*8760
        self.heat = 0
        self.annuity = 0
        self.emissions = self.getEmissions()
    
    def getHeat(self,required_heat,hour):
        """
        Given the required heat, function calculates the hourly heat met by 
        the electric heater and returns the value for unsatified thermal demand.
        
        Args:
            required_heat (float): Hourly heat demand of the building [kWh].
            hour (int): Hour of the year.
        
        Returns:
            required_heat (float): Hourly thermal demand not met by the electric heater [kWh].
        """
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
        """
        Calculates the CO2 emissions of the electric heater unit.
        
        Args:
            None
        
        Returns:
            emissions (float): CO2 emissions of the electric heater unit [kg of CO2].
        """
        # CO2 emissions for prodution of grid electricity, used by electric heaters 
        # are 595 g/kWh for Germany.
        # [Petra Icha. Entwicklung der spezifischen Kohlendioxid-Emissionen des deutschen Strommix
        # in den Jahren 1990 bis 2013. Umweltbundesamt, 2014]
        
        return 760
        
    def getAnnuity(self):
        obperiod = 10
        q = 1.07
        r = 1.03
        b = annuity.getb(q=q,r=r,obperiod=obperiod)
        bv = b
        bb = annuity.getb(q=q,r=1.02,obperiod=obperiod)
        bi = b
        deperiod = 15
        finst = 0.01
        fwins = 0.01
        effop = 5
        
        a = annuity.getAnnuityFactor(q=q,obperiod=obperiod)
        #Capital related costs for the electrical heater include price of purchase and installation costs
        CRC = 53.938*(self.thermal_capacity*1000)**0.2685
        Ank = annuity.getAnk(A0=CRC,r=r,q=q,obperiod=obperiod,deperiod=deperiod)
    
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

elhe = ElectricHeater('fdwef',11.2)
print elhe.emissions