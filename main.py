# -*- coding: utf-8 -*-
import LoadData
import GenerateCases
global_radiation = LoadData.getWeatherData("D:/Final_code")
heat_profiles,building_ids = LoadData.getHeatProfiles("D:/Python_Simulation")

for i in range(0,len(building_ids)):
    building_id = building_ids[i]
    thermal_profile = heat_profiles[i]
    building_number = GenerateCases.PostProcessingTool(building_id=building_id,thermal_profile=thermal_profile)
    building_number.generate_cases()
    
    