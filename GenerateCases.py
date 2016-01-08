# -*- coding: utf-8 -*-
import os
import itertools
import xlsxwriter
import shutil


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
                th_technologies = ["CHP","B","ThSt"],\
                el_technologies = ["ElHe"],\
                max_el_technologies = 1,\
                min_el_technologies = 0,\
                max_th_technologies = 3,\
                min_th_technologies = 0,\
                location = "E:/Post Processing Tool/Output"):
        self.thermal_profile = thermal_profile
        self.building_id = building_id
        self.th_technologies = th_technologies
        self.el_technologies = el_technologies
        self.max_el_technologies = max_el_technologies
        self.min_el_technologies = min_el_technologies
        self.max_th_technologies = max_th_technologies
        self.min_th_technologies = min_th_technologies
        self.location = location
        

    def generate_cases(self):
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
                os.chdir("../")
        return
