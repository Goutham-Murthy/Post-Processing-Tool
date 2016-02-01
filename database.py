# -*- coding: utf-8 -*-
"""
Module contains the database of all the commercially available units of different technologies and their associated
parameters. Is used in the pre-processing tool to initialise technologies.
"""


# -*- coding: utf-8 -*-
import math

CHP_database = {
                2.58: ('CHP_mikro_ECO_POWER_1', 2.58, 0.657, 0.263),
                8: ('CHP_mini_ECO_POWER_3', 8, .65, .25),
                12.5: ('CHP_mini_ECO_POWER_4.7', 12.5, .65, .25),
                20: ('CHP_XRGI_9kWel', 20, .65, .29),
                42: ('CHP_mini_ECO_POWER_20', 42, .638, .276)
                }

B_database = {
                11: ('Boiler_Vitogas200F_11kW', 11, 0.98),
                15: ('Boiler_Vitogas200F_15kW', 15, 0.98),
                18: ('Boiler_Vitogas200F_18kW', 18, 0.98),
                22: ('Boiler_Vitogas200F_22kW', 22, 0.98),
                29: ('Boiler_Vitogas200F_29kW', 29, 0.98),
                35: ('Boiler_Vitogas200F_35kW', 35, 0.98),
                42: ('Boiler_Vitogas200F_42kW', 42, 0.98),
                48: ('Boiler_Vitogas200F_48kW', 48, 0.98),
                60: ('Boiler_Vitogas200F_60kW', 60, 0.98)
                }

ThSt_database = {
                300: ('Vaillant_VPS_allSTOR_300', 13.933, 1),
                500: ('Vaillant_VPS_allSTOR_500', 23.222, 1),
                800: ('Vaillant_VPS_allSTOR_800', 37.155, 1),
                100: ('Vaillant_VPS_allSTOR_1000', 46.444, 1),
                1500: ('Vaillant_VPS_allSTOR_1500', 69.667, 1),
                2000: ('Vaillant_VPS_allSTOR_1200', 92.888, 1)
                }


def get_chp_capacity(required_capacity):
    print required_capacity
    model = ()
    if required_capacity > 42:
        model = CHP_database[42]

    max_difference = 200000
    for available_capacity in CHP_database.keys():
        difference = abs(available_capacity - required_capacity)
        if difference <= max_difference:
            max_difference = difference
            model = CHP_database[available_capacity]
    return model


def get_b_capacity(required_capacity):
    model = ()
    max_difference = 200000
    for available_capacity in B_database.keys():
        if available_capacity >= required_capacity:
            difference = available_capacity - required_capacity
            if difference <= max_difference:
                max_difference = difference
                model = B_database[available_capacity]
    if required_capacity > 60:
        number = math.ceil(required_capacity/60.0)
        model = ('Boiler_Vitogas200F_60kW', number * 60, 0.98)
    return model


def get_thst_capacity(required_capacity):
    model = ()
    required_capacity = change_kwh_to_litres(required_capacity)
    max_difference = 200000
    for available_capacity in ThSt_database.keys():
        difference = abs(available_capacity - required_capacity)
        if difference <= max_difference:
            max_difference = difference
            model = ThSt_database[available_capacity]
    if required_capacity > 2000:
        model = ('Big storage', change_litres_to_kwh(required_capacity))
    return model


def get_solth_capacity(required_capacity):
    capacity = math.floor(required_capacity/2.55)*2.55
    return capacity


def get_pv_capacity(required_capacity):
    capacity = math.floor(required_capacity/1.6434)*1.6434
    return capacity


def get_elhe_capacity(required_capacity):
    capacity = math.ceil(required_capacity/100.0)*100
    return capacity


def change_kwh_to_litres(kwh):
    litres = kwh*3600000.0/(4180.0*40.0)
    return litres


def change_litres_to_kwh(litres):
    kwh = litres*4180.0*40.0/3600000.0
    return kwh
