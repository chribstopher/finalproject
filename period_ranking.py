"""
Christopher Rose
CSCI-141
period_ranking.py
"""
import index_tools


def quarter_data(data, year, qtr):
    """
    Depending on the year and quarter of interest, makes a list of tuples sorted from high
    HPI to low HPI (region, HPI)
    :param data: dictionary mapping a state region to a list of QuarterHPI objects
    :param year: year of interest
    :param qtr: quarter of interest
    :return: list of (region, HPI) tuples sorted from high to low value HPI
    """
    tuple_list = []
    year_dict = {}
    for key, value in data.items():
        for obj in value:
            if obj.year in year_dict:
                year_dict[obj.year].append([key, obj.qtr, obj.index])
            else:
                year_dict[obj.year] = []
                year_dict[obj.year].append([key, obj.qtr, obj.index])
    year_data = year_dict[year]
    for value in year_data:
        if value[1] == qtr:
            tuple_list.append((value[0], value[2]))
    tuple_list.sort(key=lambda x: x[1], reverse=True)
    return tuple_list


def annual_data(data, year):
    """
    Depending on the year of interest, makes a tuple list (region, HPI) that is
    sorted from high HPI to low HPI value.
    :param data: dictionary mapping a state or zip code to a list of AnnualHPI objects
    :param year: year of interest
    :return: list of (region, HPI) tuples sorted from high HPI to low HPI
    """
    tuple_list = []
    year_dict = {}
    for key, value in data.items():
        for obj in value:
            if obj.year in year_dict:
                year_dict[obj.year].append([key, obj.index])
            else:
                year_dict[obj.year] = []
                year_dict[obj.year].append([key, obj.index])
    year_data = year_dict[year]
    for obj in year_data:
        tuple_list.append((obj[0], obj[1]))
    tuple_list.sort(key=lambda x: x[1], reverse=True)
    return tuple_list


def main():

    filename = "data/" + input("Enter house price index file: ")
    if "ZIP5" in filename:
        year = int(input("Enter year of interest for house prices: "))
        data = index_tools.read_zip_house_price_data(filename)
        print("")
        year_data = annual_data(data, year)
        index_tools.print_ranking(year_data, heading=str(year) + " " + "Annual Ranking")
    else:
        year = int(input("Enter year of interest for house prices: "))
        qtr_interest = int(input("Enter quarter of interest for house prices: "))
        data = index_tools.read_state_house_price_data(filename)
        print("")
        quarter = quarter_data(data, year, qtr_interest)
        index_tools.print_ranking(quarter, heading=str(year) + " Quarter: " + str(qtr_interest) + " " + "Annual Ranking")



if __name__ == '__main__':
    main()