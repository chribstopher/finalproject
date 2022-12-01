"""
Christopher Rose
CSCI-141
index_tools.py
"""


from dataclasses import dataclass


@dataclass()
class QuarterHPI:
    """
    class for storing quarter HPI data
    year: year
    qtr: which quarter of the year
    index: index value
    """
    year: int
    qtr: int
    index: float


@dataclass()
class AnnualHPI:
    """
    class for storing annualized HPI data
    year: year
    index: index value
    """
    year: int
    index: float


def read_state_house_price_data(filepath):
    """
    this function accepts a filepath and reads through the file,
    creating a dictionary mapping States to the QuarterHPI objects
    that are associated with them
    :param filepath: name of file the function must read
    :return:
    """
    dict_hpi = {}
    with open(filepath) as file:
        for line in file:
            data = line.split()
            if data[0] == 'state':
                continue
            elif data[3] == ".":
                print(data[0] + " " + data[1] + " " + data[2] + " " + data[3] + " " +
                      "warning: data unavailable in original source")
            else:
                if data[0] in dict_hpi:
                    dict_hpi[data[0]].append(QuarterHPI(int(data[1]), int(data[2]), float(data[3])))
                else:
                    dict_hpi[data[0]] = []
                    dict_hpi[data[0]].append(QuarterHPI(int(data[1]), int(data[2]), float(data[3])))
    return dict_hpi


def read_zip_house_price_data(filepath):
    """
    Function that creates a dictionary mapping zip codes to
    the list of AnnualHPI objects associated with them
    :param filepath: name of file the function must read
    :return:
    """
    dict_zip = {}
    count = 0
    uncounted = 0
    with open(filepath) as file:
        for line in file:
            data = line.split()
            if data[0] == "Five-Digit":
                continue
            elif data[1] == ".":
                uncounted += 1
                continue
            elif data[3] == ".":
                uncounted += 1
                continue
            else:
                if data[0] in dict_zip:
                    dict_zip[data[0]].append(AnnualHPI(int(data[1]), float(data[3])))
                    count += 1
                else:
                    dict_zip[data[0]] = []
                    dict_zip[data[0]].append(AnnualHPI(int(data[1]), float(data[3])))
                    count += 1
    print("Count: ", count, "Uncounted: ", uncounted)
    return dict_zip


def index_range(data, region):
    """
    finds the lowest and highest index values in a dataset
    :param data: dictionary mapping regions to lists of HPI objects and a region name
    :param region: chosen region
    :return: tuple of the two min and max objects
    """
    object_list = data[region]
    object_list.sort(key=lambda x: x.index)
    minimum = object_list[0]
    maximum = object_list[-1]
    data_range = (minimum, maximum)
    return data_range


def print_range(data, region):
    """
    prints the low and high values of the HPI for a given region
    :param data: dictionary mapping regions to lists of HPI objects and a region name
    :param region: chosen region
    """
    data_range = index_range(data, region)
    minimum = data_range[0]
    maximum = data_range[1]
    try:
        print("Region: ", region)
        print("Low: year/quarter/index: ", minimum.year, "/", minimum.qtr, "/", minimum.index)
        print("High: year/quarter/index: ", maximum.year, "/", maximum.qtr, "/", maximum.index)
    except AttributeError:
        print("Low: year/index: ", minimum.year,  "/", minimum.index)
        print("High: year/index: ", maximum.year, "/", maximum.index)


def print_ranking(data, heading="Ranking"):
    """
    prints the first and last 10 elements of a sorted list of tuples
    :param data: sorted list of objects
    :param heading: str with default "Ranking" value
    """
    print(heading)
    print("Top 10")
    print("1 : ", data[0])
    print("2 : ", data[1])
    print("3 : ", data[2])
    print("4 : ", data[3])
    print("5 : ", data[4])
    print("6 : ", data[5])
    print("7 : ", data[6])
    print("8 : ", data[7])
    print("9 : ", data[8])
    print("10 : ", data[9])
    print("Bottom 10")
    print(len(data)-9, ":", data[-10])
    print(len(data)-8, ":", data[-9])
    print(len(data)-7, ":", data[-8])
    print(len(data)-6, ":", data[-7])
    print(len(data)-5, ":", data[-6])
    print(len(data)-4, ":", data[-5])
    print(len(data)-3, ":", data[-4])
    print(len(data)-2, ":", data[-3])
    print(len(data)-1, ":", data[-2])
    print(len(data), ":", data[-1])


def annualize(data):
    """
    takes QuarterHPI data and averages it into AnnualHPI data
    :param data: dictionary mapping regions to lists of HPI objects and a region name
    :return: AnnualHPI data
    """
    annualized_dict = {}
    for key, value in data.items():
        quarter_dict = {}
        for obj in value:
            if obj.year in quarter_dict:
                quarter_dict[obj.year].append(obj.index)
            else:
                quarter_dict[obj.year] = []
                quarter_dict[obj.year].append(obj.index)
        for year in quarter_dict:
            index_list = quarter_dict[year]
            total = 0
            for index in index_list:
                total += index
            average = total / len(index_list)
            if key in annualized_dict:
                annualized_dict[key].append(AnnualHPI(int(year), float(average)))
            else:
                annualized_dict[key] = []
                annualized_dict[key].append(AnnualHPI(int(year), float(average)))
    return annualized_dict


def main():
    """
    standalone execution operation, prompts for filename and
    regions of interest. prints data associated with them
    """
    filename = "data/" + input("Enter house price index file: ")
    if "ZIP5" in filename:
        data = read_zip_house_price_data(filename)
    else:
        data = read_state_house_price_data(filename)
        annual = annualize(data)
    region_list = []
    region = input("Next region of interest (Hit ENTER to stop): ")
    if region == "":
        exit()
    else:
        region_list.append(region)
    while region != "":
        region = input("Next region of interest (Hit ENTER to stop): ")
        if region == "":
            break
        else:
            region_list.append(region)
    for region in region_list:
        print("=============================================================")
        print_range(data, region)
        annual_data = annualize(data)
        print_range(annual_data, region)
        print("Annualized Index Values for", region)
        region_list = annual_data[region]
        for item in region_list:
            print(item)


if __name__ == '__main__':
    main()