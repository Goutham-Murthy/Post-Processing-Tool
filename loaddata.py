# -*- coding: utf-8 -*-
import xlrd
import csv  # Importing csv module for reading the thermal load profiles
from itertools import islice  # Importing islice to iterate over rows


def get_weather_data(location):
    """
    Loads weather data

    :param location: String containing path to the weather file.
    :return: global_radiation: global radiation for PV and solar thermal operation.
    """
    global_radiation = []

    # Opening the TRY data. The delimiter is ;.
    reader = open(location)
    csv_reader = csv.reader(reader, delimiter='\t')

    for row in islice(csv_reader, 2, None):
        global_radiation.append(float(row[14])+float(row[15]))
    reader.close()
    print "Weather data Loaded"
    return global_radiation


def get_heat_profiles(location):
    """
    Loads heat profiles and corresponding building ids.

    :param location: String containing path to the weather file.
    :return: heat_profilesHeat profiles of the building.
    :return: building_idsBuilding ids
    """
    wb = xlrd.open_workbook(location)

    heat_profiles = []
    building_ids = []
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols
        for col in range(number_of_columns):
            thermal_profile = []
            building = str(sheet.cell(0, col).value)
            for row in range(1, number_of_rows):
                value = sheet.cell(row, col).value / 1000
                try:
                    value = float(value)
                except ValueError:
                    pass
                finally:
                    thermal_profile.append(value)
            heat_profiles.append(thermal_profile)
            building_ids.append(building)
    print "Building Heat Profile loaded"
    return heat_profiles, building_ids


def get_el_profiles(location):
    """
    Loads electrical profiles and corresponding building ids.

    :param location: String containing path to the weather file.
    :return: heat_profilesElectrical profiles of the building.
    :return: building_idsBuilding ids
    """
    wb = xlrd.open_workbook(location)

    el_profiles = []
    building_ids = []
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols
        for col in range(number_of_columns):
            electrical_profile = []
            building = str(sheet.cell(0, col).value)
            for row in range(1, number_of_rows):
                value = sheet.cell(row, col).value / 1000
                try:
                    value = float(value)
                except ValueError:
                    pass
                finally:
                    electrical_profile.append(value)
            el_profiles.append(electrical_profile)
            building_ids.append(building)
    print "Building Electrical Profile loaded"
    return el_profiles, building_ids
