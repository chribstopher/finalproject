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
    :precondition: year0<year1
    :param data: dictionary from region to a list of AnnualHPI objects
    :param year0: beginning year of interest
    :param year1: ending year of interest
    :return: list of (region, rate) tuples sorted in descending order
    by compound annual growth rate
    """
    trend_list = []
    period = year1 - year0
    for key, value in data.items():
        year_dict = {}
        for obj in value:
            if obj.year == year0 or obj.year == year1:
                if obj.year in year_dict:
                    year_dict[obj.year].append([key, obj.index])
                else:
                    year_dict[obj.year] = []
                    year_dict[obj.year].append([key, obj.index])
        try:
            idxlist = [year_dict[year0][0][1], year_dict[year1][0][1]]
        except KeyError:
            continue
        trend_list.append((key, cagr(idxlist, period)))
        trend_list.sort(key=lambda x: x[1], reverse=True)
    return trend_list


def main():
    """
    standalone execution method, prompts for filename and years of interest
    then prints the top and bottom 10 growth regions in that time span
    """
    filename = "data/" + input("Enter house price index file: ")
    if "ZIP5" in filename:
        year0 = int(input("Enter start year of interest: "))
        year1 = int(input("Enter ending year of interest: "))
        data = index_tools.read_zip_house_price_data(filename)
        trend_list = calculate_trends(data, year0, year1)
        print("")
        index_tools.print_ranking(trend_list, heading= str(year0)+"-"+str(year1)+" "+"Compound Annual Growth Rate")
    else:
        year0 = int(input("Enter start year of interest: "))
        year1 = int(input("Enter ending year of interest: "))
        data = index_tools.read_state_house_price_data(filename)
        annual = index_tools.annualize(data)
        trend_list = calculate_trends(annual, year0, year1)
        print("")
        index_tools.print_ranking(trend_list, heading= str(year0)+"-"+str(year1)+" "+"Compound Annual Growth Rate")


if __name__ == "__main__":
    main()
