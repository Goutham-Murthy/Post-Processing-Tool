# -*- coding: utf-8 -*-
"""
Module consists class representing boilers.
"""
import annuity

class Boiler:
    """Class representing boiler technology.
    
    Attributes:
    model (string): Model of the boiler.
    thermal_capacity (float): Thermal capacity of the boiler [kW].
    efficiency (float): Efficiency of the boiler [decimal<1].
    heat_yearly (float): Sum value of heat provided by the boiler unit over the year[kWh].
    heat_hourly (float): Hourly values of the heat provided by the boiler unit [kWh].
    annuity (float) : Annuity of the boiler [Euros]
    """

    def __init__(self, model, thermal_capacity, efficiency):
        """Constructor method for class Boiler.
        
        Args:
        model (string): Model of the boiler.
        thermal_capacity (float): Thermal capacity of the boiler [kW].
        efficiency (float): Efficiency of the boiler [decimal<1].
        """
        self.model = model
        self.thermal_capacity = thermal_capacity
        self.efficiency = efficiency
        # Initialising other attributes to zero.
        self.heat_hourly = [0]*8760
        self.heat_yearly = 0
        self.annuity = 0
        
    def get_heat(self,required_heat,hour):
        """
        Given the required heat, function calculates the hourly heat given by 
        the boiler and returns the value for unsatified thermal demand.
        
        Args:
        required_heat (float): Hourly heat demand of the building [kWh].
        hour (int): Hour of the year.
        
        Returns:
        required_heat (float): Hourly thermal demand not met by the boiler [kWh].
        """
        # If thermal capacity is more than hourly thermal demand, meet the demand
        # entirely.
        if required_heat <= self.thermal_capacity:
            self.heat_yearly += required_heat
            self.heat_hourly[hour] = required_heat
            required_heat = 0
            return required_heat
        # If hourly thermal demand is grreater than the capacity, meet as much as
        # possible.
        else:
            self.heat_yearly += self.thermal_capacity
            self.heat_hourly[hour] = self.thermal_capacity
            required_heat -= self.thermal_capacity
            return required_heat
        
    def get_emissions(self):
        """
        Calculates the CO2 emissions of the boiler unit.
        
        Args:
        None
        
        Returns:
        emissions (float): CO2 emissions of the boiler unit [kg of CO2].
        """
        # CO2 emissions of condensing boilers are about 56 g/MJ or 201.6 g/kWh.
        # [R Dones, Thomas Heck, and S Hirschberg. Greenhouse gas emissions from energy systems:
        # comparison and overview. 2004.]
        emissions = (201.6*self.heat_yearly/1000)
        return emissions
        
    def get_annuity(self):
        """
        Calculates the annuity of the boiler according to equations in VDI 2067.
        
        Args:
        None
        
        Returns:
        annuity (float): Annuity of the boiler unit [Euros]
        """
        obperiod = 10 #VDI2067
        # The following factors are assumed. For boilers and other technologies
        q = 1.07
        r = 1.03
        b = annuity.getb(q=q,r=r,obperiod=obperiod)
        bv = b
        bb = annuity.getb(q=q,r=1.02,obperiod=obperiod)
        bi = b
        # The deprecition period, finst,fwins and effop are different for different 
        # capacitites according to VDI 2067    
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
        
        # Capital Related Costs
        a = annuity.get_annuity_factor(q=q,obperiod=obperiod)
        # Capital related costs for the boiler include price of purchase and 
        # installation costs.
        CRC = 79.061*self.thermal_capacity + 1229.8
        Ank = annuity.get_Ank(A0=CRC,r=r,q=q,obperiod=obperiod,deperiod=deperiod)
    
        # Demand related costs include price of fuel to produce the required heat
        # Price of gas is 0.067 Euros/kWh. [Eurostat. nrg_pc_205. Accessed: 2015-02-11.]
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
              
        self.annuity = Ane - (Ank+Anv+Anb+Ans)        
        return CRC,Ank,Anv,Anb,self.annuity 

