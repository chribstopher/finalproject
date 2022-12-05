"""
Christopher Rose
CSCI-141
timeline_plot.py
"""

import numpy.ma as ma
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import copy
import index_tools


def build_plottable_array(xyears, regiondata):
    """
    constructs an array that builds a bridge over the possibility of
    unavailable data gaps
    :param xyears: list of integer year values
    :param regiondata: list of AnnualHPI objects
    :return: array suitable for plotting with the matplotlib module
    """
    corrected_data = []
    year_dict = {}
    for object in regiondata:
        year_dict[object.year] = object.index
    for year in xyears:
        if year in year_dict:
            corrected_data.append(year_dict[year])
        else:
            corrected_data.append('None')
    mask = [(el == "None") for el in corrected_data]
    masked_data = ma.masked_array(corrected_data, mask=mask)
    print(masked_data)
    return masked_data


def filter_years(data, year0, year1):
    """
    Creates a dictionary of region to HPI values within the year
    range given by the user
    :param data: dictionary mapping regions to lists of AnnualHPI objects
    :param year0: beginning year of interest
    :param year1: ending year of interest
    :return: dictionary mapping regions to lists of HPI values
    :pre-condition:year0 < year1
    that are within the given year range
    """
    yr_range_dict = {}
    yr_list = [i for i in range(int(year0), int(year1)+1)]
    for key, value in data.items():
        for obj in value:
            if obj.year in yr_list:
                if key in yr_range_dict:
                    yr_range_dict[key].append(obj)
                else:
                    yr_range_dict[key] = []
                    yr_range_dict[key].append(obj)
    return yr_range_dict


def year_finder(data):
    """
    finds the range of years represented in the data given
    :param data: dictionary mapping regions to lists of HPI objects
    :return: list containing the min and max values
    """
    minimum = ""
    maximum = ""
    for key, values in data.items():
        if minimum == "":
            minimum = values[0].year
        elif values[0].year < minimum:
            minimum = values[0]
        if maximum == "":
            maximum = values[-1].year
        elif values[-1].year > maximum:
            maximum = values[-1].year
    return [minimum, maximum]


def plot_HPI(data, regionlist):
    """
    plots a timeline from point to point over the time period of the data
    :param data: dictionary mapping a state or zip code to a list of Annual HPI objects
    :param regionlist: list of key values whose type is string
    :return: NoneType
    """
    year0 = year_finder(data)[0]
    year1 = year_finder(data)[1]
    year_list = [i for i in range(year0, year1+1)]
    for region in regionlist:
        plot_data = build_plottable_array(year_list, data[region])
        plt.plot(year_list, plot_data, '*', linestyle='-', label=region)
    plt.title('Home Price Index: ' + str(year0) + "-" + str(year1))
    plt.autoscale(True, 'both', True)
    mticker.AutoLocator()
    plt.legend()
    plt.show()


data = index_tools.read_zip_house_price_data('data/HPI_AT_ZIP5.txt')
graph_data = filter_years(data, 1988, 2008)
plot_HPI(graph_data, ['04083', '14625', '48210', '12202'])
