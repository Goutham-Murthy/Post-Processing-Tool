# -*- coding: utf-8 -*-
from xlrd import open_workbook
from xlutils.copy import copy
import os
import itertools
import xlsxwriter
import shutil
import CHP
import Boiler
import ElectricHeater

class PostProcessingTool:
    """Boiler class
    
    Attributes:
    building_id : Building ID of the particular building
    th_technologies : List of the thermal technologies to be considered
    el_technologies : List of the thermal technologies to be considered
    max_el_technologies : Maximum number of electrical technologies to be considered
    min_el_technologies : Minimum number of electrical technologies to be considered
    max_th_technologies : Maximum number of thermal technologies to be considered
    min_th_technologies : Minimum number of thermal technologies to be considered
    Location : Address of the folder where the ouput folder is to be created"""
    
    def __init__(self,building_id,thermal_profile,\
                maxr_thermal_power=0,
                maxr_hours=0,
                peak_thermal_power=0,th_technologies = ["CHP","B","ElHe"],\
                el_technologies = ["CHP"],\
                max_el_technologies = 1,\
                min_el_technologies = 0,\
                max_th_technologies = 2,\
                min_th_technologies = 0,\
                hourly_excels = 'y',\
                location = "D:/aja-gmu/Simulation_Files/Output"):
        self.thermal_profile = thermal_profile
        self.building_id = building_id
        self.th_technologies = th_technologies
        self.el_technologies = el_technologies
        self.max_el_technologies = max_el_technologies
        self.min_el_technologies = min_el_technologies
        self.max_th_technologies = max_th_technologies
        self.min_th_technologies = min_th_technologies
        self.location = location
        self.maxr_thermal_power,self.maxr_hours = PostProcessingTool.getMaximumRectangle(self,thermal_profile)
        self.peak_thermal_power = max(thermal_profile)

    def generateCases(self):
        """Generates the scenarios"""
    
        if not os.path.exists(self.location+"/"+self.building_id):  # Make the output folder if it does not exist
            os.makedirs(self.location+"/"+self.building_id)
        
        os.chdir(self.location+"/"+self.building_id)  # Change to the folder
        for the_file in os.listdir(self.location+"/"+self.building_id): # Delete all the old files and folders
            file_path = os.path.join(self.location+"/"+self.building_id, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): 
                shutil.rmtree(file_path)
    
        
        #Load thermal profile and weather data
        technologies = list(set(self.th_technologies).union(self.el_technologies))
        
        #------------------------------------------------------------------------------
        #Iterating from 1 to the maximum number of technologies 
        for number in range(1,len(technologies)+1):
            
            #Make seperate directories depending on the number of technologies present in the system
            if (number <= self.max_el_technologies + self.max_th_technologies-1 \
            and number >= self.min_el_technologies+ self.min_th_technologies):      
                if not os.path.exists(str(number)+'technologies'):
                    os.makedirs(str(number)+'technologies')
        
                #Changing to the required directory in output directory
                os.chdir('./'+str(number)+'technologies')
                #----------------------------------------------------------------------
                #Iterating through the various possible combinations.
                for combo in itertools.combinations(technologies,number):
                    
                    #Proceed further only if there is CHP present in the system
                    if 'CHP' in combo:
                        
                        #Proceed further is the number of technologies in the system are suitable
                        if (len(set(combo) & set(self.el_technologies)) <= self.max_el_technologies\
                        and len(set(combo) & set(self.th_technologies)) <= self.max_th_technologies \
                        and len(set(combo) & set(self.el_technologies)) >= self.min_el_technologies \
                        and len(set(combo) & set(self.th_technologies)) >= self.min_th_technologies):               
                                             
                            system = ""
                            count = 1
                            for i in combo:
                                if len(set(combo)) == count:
                                    system += i
                                else:
                                    system += i + "-"
                                    count += 1
                                
                            
                            
                            # Create classes of the technologies
                            print '\n\n====================System-',system
                            PostProcessingTool.initialiseTechnologies(self,combo)

                            #Create excel with the corresponding name
                            excel = xlsxwriter.Workbook(system+".xls")
                                    
                            #------------------------------------------------------
                            #Generating different thermal priorities for each electrical
                            #priority and iterating through them
                            for th_order in itertools.permutations(set(combo) & set(self.th_technologies)):
                                th_priority = ""
                                count = 1
                                for elements in th_order:
                                    if len(set(combo)&set(self.th_technologies)) == count:
                                        th_priority += elements
                                    else:
                                        th_priority += elements + ">"
                                        count += 1
                                    #For each thermal
                                    # priority a seperate worksheet is created.
                                excel.add_worksheet(th_priority)
                                count += 1
                            excel.close()
                                
                            for th_order in itertools.permutations(set(combo) & set(self.th_technologies)):
                                th_priority = ""
                                count = 1
                                for elements in th_order:
                                    if len(set(combo)&set(self.th_technologies)) == count:
                                        th_priority += elements
                                    else:
                                        th_priority += elements + ">"
                                        count += 1
                                PostProcessingTool.performCalculations(self,th_order) 
                                self.write_hourly_excel(system+".xls",th_priority,th_order)
                                
                os.chdir("../")
        return
        
    def getMaximumRectangle(self,thermal_profile):
        
        #Sort thermal demand in decreasing order for the load distribution curve
        thermal_profile = sorted(thermal_profile, reverse=True)
        
        #Finding the maximum rectangle
        q_yearly = 0
        maxr = 0
        for k in range(0,8760):
            q_yearly += thermal_profile[k]
            if k*thermal_profile[k]>maxr:
                maxr=k*thermal_profile[k]
                hours=k
        print maxr,hours,thermal_profile[hours]
        return thermal_profile[hours],hours
        
    def initialiseTechnologies(self, system):
        
        #------------------------------------------------------------------------------
        #CHP    
        #If CHP is present, it will check for a peak load device. If peak load 
        #device is present, CHP is sized according to maximum rectangle method. 
        # Otherwise it is sized according to peak thermal load.
        if 'CHP' in system:
            if 'ElHe' in system or 'B' in system:
                self.OnOffCHP = CHP.OnOffCHP('YahooCHP',self.maxr_thermal_power,0.6,0.3)
            else:
                self.OnOffCHP = CHP.OnOffCHP('YahooCHP',self.peak_thermal_power,0.6,0.3)
    
    #------------------------------------------------------------------------------
    #Boiler    
        #If boiler is present, dimension it to peak thermal demand
        if 'B' in system:
            self.B = Boiler.Boiler('YahooB',self.peak_thermal_power,0.98)
                
            
    #------------------------------------------------------------------------------
    #Electric Resistance Heater
        #If electric heater is present, dimension it to peak thermal demand 
        if 'ElHe' in system:
            self.ElHe = ElectricHeater.ElectricHeater('Model',self.peak_thermal_power,0.98)
        
        return
        
    def performCalculations(self,th_order):
        for i in range (0,8760):
            q_hourly=self.thermal_profile[i]
            
            for technology in th_order:
                if technology is 'CHP' and q_hourly>0:
                    q_hourly=self.OnOffCHP.getCHPHeat(q_hourly,i)
                if technology is 'B' and q_hourly>0:
                    q_hourly=self.B.getBoilerHeat(q_hourly,i)
                if technology is 'ElHe' and q_hourly>0:
                    q_hourly = self.ElHe.getElHeHeat(q_hourly,i)
        return
            
        
    def write_hourly_excel(self,workbook_name,worksheet_name,th_order):  

        #--------------------------------------------------------------------------
        #write all values into the worksheet   

        workbook = open_workbook(workbook_name,worksheet_name)
        idx = workbook.sheet_names().index(worksheet_name)
        workbook = copy(workbook)
        worksheet = workbook.get_sheet(idx)
        worksheet.write(0,0,"Hour")
        worksheet.write(0,1,"Hourly Thermal Demand")
        count = 2
        for technology in th_order:
            if technology is 'CHP':
                worksheet.write(0,count,"CHP Production")
            elif technology is 'B':
                worksheet.write(0,count,"Boiler Production")
            elif technology is 'ElHe':
                worksheet.write(0,count,"Electrical Resistance Heater Production")
            count += 1
               
        for i in range (0,8760):
            worksheet.write(i+1,0,i)
            worksheet.write(i+1,1,self.thermal_profile[i])
            count = 2
            for technology in th_order:
                if technology is 'CHP':
                    worksheet.write(i+1,count,self.OnOffCHP.heat_hourly[i])
                elif technology is 'B':
                    worksheet.write(i+1,count,self.B.heat_hourly[i])
                elif technology is 'ElHe':
                    worksheet.write(i+1,count,self.ElHe.heat_hourly[i])
                count += 1     
        workbook.save(workbook_name)