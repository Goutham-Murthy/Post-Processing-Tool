# -*- coding: utf-8 -*-
import loaddata
import preprocessingtool
import os
global_radiation = loaddata.get_weather_data("D:/aja-gmu/Simulation_Files")
heat_profiles, building_ids = loaddata.get_heat_profiles("D:/aja-gmu/Simulation_Files")

for i in range(0, len(building_ids)):
    building_id = building_ids[i]
    thermal_profile = heat_profiles[i]
    building_number = preprocessingtool.PreProcessingTool(building_id=building_id, thermal_profile=thermal_profile)
    building_number.generate_cases()

os.chdir("D:/aja-gmu/Simulation_Files")
