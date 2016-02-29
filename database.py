# -*- coding: utf-8 -*-
"""
Module contains the database of all the commercially available units of different technologies and their associated
parameters. Is used in the pre-processing tool to initialise technologies.
"""


# -*- coding: utf-8 -*-
import math

SolTh_fixed_area = None
SolTh_available_area = None
SolTh_module_area = None
PV_fixed_area = None
PV_available_area = None
PV_module_area = None
ElHe_module_cap = None
ElHe_fixed_cap = None
ElSt_capacity = None
ElSt_max_hourly_input = None


# Annuity factors for the various technologies
annuity_factors = {
                    'Common': (10.00, 0.067, 0.26, 0.10, 0.12),
                    'CHP': (15.0, 10.0, 1.0, 1.0, 1.07, 1.03),
                    'B': (18.0, 10.0, 1.5, 1.5, 1.07, 1.03),
                    'ThSt': (15.0, 0.0, 1.0, 2.0, 1.07, 1.03),
                    'SolTh': (20.0, 5.0, 1.0, 0.5, 1.07, 1.03),
                    'ElHe': (15.0, 5.0, 1.0, 1.0, 1.07, 1.03),
                    'PV': (25.0, 5.0, 1.0, 0.5, 1.07, 1.03),
                    'ElSt': (5.0, 0.0, 1.0, 0.5, 1.07, 1.03)
                    }

# CHP database with thermal capacity as key and model details as a tuple in values.
# Key              : Value
# thermal capacity : (model name, thermal capacity(kW), thermal efficiency, electrical efficiency)
CHP_database = {
                2.58: ('CHP_mikro_ECO_POWER_1', 2.58, 0.657, 0.263),
                8: ('CHP_mini_ECO_POWER_3', 8, .65, .25),
                12.5: ('CHP_mini_ECO_POWER_4.7', 12.5, .65, .25),
                20: ('CHP_XRGI_9kWel', 20, .65, .29),
                42: ('CHP_mini_ECO_POWER_20', 42, .638, .276)
                }

# Boiler database with thermal capacity as key and model details as a tuple in values.
# Key              : Value
# thermal capacity : {model name, thermal capacity(kW), thermal efficiency}
B_database = {
                11: ('Boiler_Vitogas200F_11kW', 11.0, 0.98),
                15: ('Boiler_Vitogas200F_15kW', 15.0, 0.98),
                18: ('Boiler_Vitogas200F_18kW', 18.0, 0.98),
                22: ('Boiler_Vitogas200F_22kW', 22.0, 0.98),
                29: ('Boiler_Vitogas200F_29kW', 29.0, 0.98),
                35: ('Boiler_Vitogas200F_35kW', 35.0, 0.98),
                42: ('Boiler_Vitogas200F_42kW', 42.0, 0.98),
                48: ('Boiler_Vitogas200F_48kW', 48.0, 0.98),
                60: ('Boiler_Vitogas200F_60kW', 60.0, 0.98)
                }

# Thermal storage database with thermal capacity in liters as key and model details as a tuple in values.
# Key                       : Value
# thermal capacity (liters) : {model name, thermal capacity(kWh), losses(%/hour)}
ThSt_database = {
                300: ('Vaillant_VPS_allSTOR_300', 13.933, 1),
                500: ('Vaillant_VPS_allSTOR_500', 23.222, 1),
                800: ('Vaillant_VPS_allSTOR_800', 37.155, 1),
                100: ('Vaillant_VPS_allSTOR_1000', 46.444, 1),
                1500: ('Vaillant_VPS_allSTOR_1500', 69.667, 1),
                2000: ('Vaillant_VPS_allSTOR_1200', 92.888, 1)
                }


def get_chp_capacity(required_capacity):
    """
    Returns commercially available CHP model details closest to required thermal capacity of the CHP.

    :param required_capacity: Required thermal capacity of the CHP unit[kW].
    :return: model: Specifications of the CHP unit with thermal capacity closest to the required capacity
    """
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
    """
    Returns commercially available boiler model details closest to required thermal capacity of the boiler.

    :param required_capacity: Required thermal capacity of the boiler unit[kW].
    :return: model: Specifications of the boiler unit with thermal capacity closest to the required capacity
    """
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
    """
    Returns commercially available thermal storage model details closest to required thermal capacity of the thermal
    storage unit.

    :param required_capacity: Required thermal capacity of the thermal storage unit[kWh].
    :return: model: Specifications of the thermal storage unit with thermal capacity closest to the required
                    capacity
    """
    model = ()
    required_capacity = change_kwh_to_litres(required_capacity)
    max_difference = 200000
    for available_capacity in ThSt_database.keys():
        difference = abs(available_capacity - required_capacity)
        if difference <= max_difference:
            max_difference = difference
            model = ThSt_database[available_capacity]

    # If required capacity is large, custom made?
    if required_capacity > 2000:
        model = ('Big storage', change_litres_to_kwh(required_capacity), 1.0)
    return model


def get_solth_capacity(required_capacity):
    """
    Returns commercially available solar thermal model area closest to required area of the solar thermal unit.

    :param required_capacity: Required area of the solar thermal unit[m2].
    :return: capacity: Area of the solar thermal unit with area closest to the required area.
    """
    if SolTh_fixed_area is not None:
        capacity = SolTh_fixed_area
    else:
        # Each module is considered to be of area SolTh_module_area
        capacity = math.floor(required_capacity/SolTh_module_area)*SolTh_module_area
    return capacity


def get_pv_capacity(required_capacity):
    """
    Returns commercially available PV model area closest to required area of the PV unit.

    :param required_capacity:  Required area of the PV[m2].
    :return: capacity:  Area of the PV unit with area closest to the required area.
    """
    if PV_available_area is not None:
        capacity = PV_fixed_area
    else:
        # Each module is considered to be of area PV_module_area
        capacity = math.floor(required_capacity/PV_module_area)*PV_module_area
    return capacity


def get_elhe_capacity(required_capacity):
    """
    Returns commercially available electrical heater model capacity closest to required capacity of the electrical
    heater unit.

    :param required_capacity:  Required capacity of the electrical heater[kW].
    :return: capacity:  Capacity of the electrical heater unit with area closest to the required capacity[kW].
    """
    if ElHe_fixed_cap is not None:
        return ElHe_fixed_cap
    else:
        # Multiples of module capacity
        capacity = math.ceil(required_capacity/ElHe_module_cap)*ElHe_module_cap
    return capacity


def change_kwh_to_litres(capacity_in_kwh):
    """
    Converts kWh to liters for the thermal storage unit

    :param capacity_in_kwh: Capacity of the thermal storage in kWh[kWh].
    :return: capacity_in_liters: Capacity of the thermal storage in liters[liters].
    """
    # capacity in liters = capacity in kwh*360000/(density of water * Cp of water * temperature difference between top
    #                                              and bottom parts of the storage, assumed to be 40 K)
    capacity_in_litres = capacity_in_kwh*3600000.0/(4180.0*40.0)
    return capacity_in_litres


def change_litres_to_kwh(capacity_in_litres):
    """
    Converts kWh to liters for the thermal storage unit

    :param capacity_in_litres:  Capacity of the thermal storage in liters[liters].
    :return: capacity_in_kwh: Capacity of the thermal storage in kWh[kWh].
    """
    capacity_in_kwh = capacity_in_litres*4180.0*40.0/3600000.0
    return capacity_in_kwh
