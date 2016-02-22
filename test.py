# ======================================================================================================================
# Modulating CHP
# ======================================================================================================================
# import CHP
# import thermalstorage

# Test modulating CHP without ThSt
# modCHP = CHP.ModCHP(('Test_Mod_CHP', 10, 0.6, 0.3))
# heat_profile = [1, 3.33, 3.0, 11.88, 10, 9.99, 3.001]
# hour = 0
# for demand in heat_profile:
#     modCHP.get_heat(demand, hour)
#     hour += 1
# print heat_profile[0:7]
# print modCHP.heat_hourly[0:7], modCHP.heat_yearly

# Test modulating CHP with ThSt
# modCHP = CHP.ModCHP(('Test_Mod_CHP', 10, 0.6, 0.3))
# ThSt = thermalstorage.ThermalStorage(('Test_storage', 2, 1))
# heat_profile = [1, 3.33, 3.0, 11.88, 10, 9.99, 3.001]
# hour = 0
# for demand in heat_profile:
#     ThSt.apply_losses(hour)
#     modCHP.get_heat(demand, hour, ThSt)
#     modCHP.get_electricity(demand, hour)
#     hour += 1
# print heat_profile[0:7]
# print modCHP.heat_hourly[0:7], modCHP.heat_yearly
# print modCHP.electricity_hourly[0:7], modCHP.electricity_hourly_exported[0:7]
# print ThSt.heat_stored[0:7]
# print ThSt.heat_given[0:7]

# ======================================================================================================================
# Continuous CHP
# ======================================================================================================================
# import CHP
# import thermalstorage

# # Test continuous CHP without ThSt
# contCHP = CHP.ConCHP(('Test_Con_CHP', 10, 0.6, 0.3))
# heat_profile = [1, 3.33, 3.0, 11.88, 10, 9.99, 3.001]
# hour = 0
# for demand in heat_profile:
#     contCHP.get_heat(demand, hour)
#     hour += 1
# print heat_profile[0:7]
# print contCHP.heat_hourly[0:7], contCHP.heat_yearly

# # Test continuous CHP with ThSt
# contCHP = CHP.ConCHP(('Test_Mod_CHP', 10, 0.6, 0.3))
# ThSt = thermalstorage.ThermalStorage(('Test_storage', 2, 1))
# heat_profile = [1, 3.33, 3.0, 11.88, 10, 9.99, 3.001]
# hour = 0
# for demand in heat_profile:
#     ThSt.apply_losses(hour)
#     contCHP.get_heat(demand, hour, ThSt)
#     contCHP.get_electricity(demand, hour)
#     hour += 1
# print heat_profile[0:7]
# print contCHP.heat_hourly[0:7], contCHP.heat_yearly
# print contCHP.electricity_hourly[0:7], contCHP.electricity_hourly_exported[0:7]
# print ThSt.heat_stored[0:7]
# print ThSt.heat_given[0:7]
# ======================================================================================================================

