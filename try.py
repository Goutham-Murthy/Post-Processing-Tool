import GenerateCases
import os

building1 = GenerateCases.PostProcessingTool(building_id="building1")
building1.generate_cases()
os.chdir("E:/Post Processing Tool/Output")
ffwfq = GenerateCases.PostProcessingTool(building_id="building2")
ffwfq.generate_cases()

