import configparser

import DataHandling
import WriteToXML
import GenXML
import ReadFromXML
import Predict

if __name__ == "__main__":
    # Read config file
    config = configparser.ConfigParser()
    config.read("config.ini")
    config_paths = config["paths"]
    config_grid = config["grid"]
    config_pos = config["positions"]

    #config params
    #Grid
    numGridPoints = int(config_grid["numGridPoints"])
    grid_file = config_grid["filepath"]#Naming convention of data files
    grid_ext = config_grid["ext"]#File Extension

    #Positions
    num_positions = int(config_pos["num_positions"])
    pos_file = config_pos["filepath"]
    pos_ext = config_pos["ext"]#File Extension

    #Paths
    xml_data = config_paths["xml_data"]
    xml_pos = config_paths["xml_pos"]

    n_neighbours = 2

    #Steps of Program:

    #Step 1:
    #Must be done beforehand
    #Record Raw Data using RecordRawData for every grid point on grid
    #Record Raw Data of test locations using RecordRawData which must be edited for this use case
    #definetly using an interface of some sort

    #Step 1.5:
    #Must be done beforehand:
    #Generate xml file usiing GenXML.py to generate an empty xml file
    GenXML.createFile(file=xml_data, num_grid_points=numGridPoints)
    GenXML.createFile(file=xml_pos, num_grid_points=num_positions)



    #Step 2:
    #Write Raw data to xml file after data has been recorded
    for i in range(numGridPoints):
        WriteToXML.write_wifi(input_file=f"{grid_file}{i}{grid_ext}",#filename-i
                         output_file=xml_data,
                         grid_id=i)

    #Step 2.5:
    #Write X Coordinates to xml file
    for i in range(numGridPoints):
        WriteToXML.write_coords(file=xml_data,
                                grid_id=i)

    #Step 3:
    #Write Raw data of test locations to xml file
    for i in range(num_positions):
        WriteToXML.write_wifi(input_file=f"{pos_file}{i}{pos_ext}",#filename-i
                         output_file=xml_pos,
                         grid_id=i)



    #Step 4:
    #Generate Data Model of grid xml data
    grid_points = ReadFromXML.DataModel(file=xml_data,
                                      num_grid_points=numGridPoints)

    #Step 5:
    #Generate Data Model of position xml data
    position_points = ReadFromXML.DataModel(file=xml_pos,
                                          num_grid_points=num_positions)


    #Step 6:
    #Caluate rssi difference errors between
    # grid_points and position_points using matching MAC Address
    rssi_differences = DataHandling.all_rssi_errors(grid_list=grid_points,
                                                    pos_list=position_points)


    #Step 7:
    #Predict locations using different methods
    coords_list = ReadFromXML.get_coords(xml_data, numGridPoints)

    #Method 1: K-Nearest Neighbour
    pred_coords = Predict.KNN(rssi_differences, coords_list, n_neighbours)


    print(pred_coords)