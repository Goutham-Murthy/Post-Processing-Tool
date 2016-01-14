# -*- coding: utf-8 -*-
import LoadData
import GenerateCases
import os
global_radiation = LoadData.getWeatherData("D:/aja-gmu/Simulation_Files")
heat_profiles,building_ids = LoadData.getHeatProfiles("D:/aja-gmu/Simulation_Files")


for i in range(0,len(building_ids)):
    building_id = building_ids[i]
    thermal_profile = heat_profiles[i]
    building_number = GenerateCases.PreProcessingTool(building_id=building_id,thermal_profile=thermal_profile)
    building_number.generateCases()
    
os.chdir("D:/aja-gmu/Simulation_Files")