import pandas as pd
import GridPoint
import xml.etree.ElementTree as ET


#Generate a codified data model of xml data input
#and return a list of GridPoints
#file=xml file
#num_grid_points = number of grid branches
def DataModel(file, num_grid_points):
    #Create grid model in the form of grid_points={GridPoint1,GridPoint2....}
    grid_points = []

    #parse xml file into tree
    tree = ET.parse(file)
    root = tree.getroot()

    #Loop through all <grid> sections and add mac_ad and rssi to grid_points dict
    for x in range(num_grid_points):
        grid = root[x]
        wifi = grid.find("wifi")

        mac_list = []
        rssi_list = []
        #Acquire all rssi and mac_ad into lists
        for rssi in wifi.findall("rssi"):
            mac_list.append(rssi.get("mac_ad"))
            rssi_list.append(rssi.text)

        #df = a df with only mac_ad and rssi
        df = pd.DataFrame()
        df["mac_ad"] = mac_list
        df["rssi"] = rssi_list

        grid_point = GridPoint.GridPoint(x=grid.find("X").text,
                                         y=grid.find("Y").text,
                                         df=df.copy(deep=True))
        grid_points.append(grid_point)

    return grid_points

#Read coordinates from given wifi data structured xml file
def get_coords(file, num_grid_points):

    #parse xml file into tree
    tree = ET.parse(file)
    root = tree.getroot()

    coord_list = []
    for i in range(num_grid_points):
        grid = root[i]
        x = int(grid.find("X").text)
        y = int(grid.find("Y").text)
        coord_list.append([x, y])

    return coord_list

