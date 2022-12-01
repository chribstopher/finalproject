"""
Christopher Rose
CSCI-141
trending.py
"""

import index_tools
import period_ranking


def cagr(idxlist, periods):
    """
    computes the compound annual growth rate, CAGR, for a period
    :param idxlist: 2 item list of [HPI0, HPI1]
    :param periods: number of periods between the two HPI values in the list
    :return:
    """
    cagr_value = (((idxlist[1]/idxlist[0])**(1/periods))-1) * 100

    return cagr_value


def calculate_trends(data, year0, year1):
    """
    calculates trend data between years of interest and makes a sorted
    list of tuples by compound annual growth rate
    :param data: dictionary from region to a list of AnnualHPI objects
    :param year0: beginning year of interest
    :param year1: ending year of interest
    :return: list of (region, rate) tuples sorted in descending order
    by compound annual growth rate
    """
    trend_list = []
    period = year1 - year0
    