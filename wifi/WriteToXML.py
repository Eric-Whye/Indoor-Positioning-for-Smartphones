#write_wifi() = reads Wifi Data from a csv file and appends the data to a single branch of an existing xml file
#write_coords() = Writes Coordinates in config.ini to specified xml file
#sys.argv[1] = filename of raw input data
#sys.argv[2] = filename to output xml data
#sys.argv[3] = grid_id/branch_id
#Can be run as a module or as a script

import pandas as pd
import xml.etree.ElementTree as ET
import configparser
import sys


def write_wifi(input_file, output_file, grid_id):

    #input_file = filename of raw input data
    #out_file = filename to output xml data
    #grid_id = grid_id


    #parse tree from xml file
    tree = ET.parse(output_file)
    root = tree.getroot()

    # read raw data from csv
    df = pd.read_csv(input_file)

    #fucntion applied to every row of dataframe
    def fillXML(row):
        ap = ET.Element("rssi")
        ap.text = str(row["RSSI"])
        ap.set("ssid", str(row["SSID"]))
        ap.set("mac_ad", str(row["MAC Address"]))
        root[grid_id].find("wifi").append(ap)
        return row

    df.apply(fillXML, axis=1)

    #append to xml tree
    ET.indent(tree, space="\t", level=0)
    tree.write(output_file)

def write_coords(file, grid_id):

    #read config file
    config = configparser.ConfigParser()
    config.read("config.ini")
    config_grid_points = config["grid_points"]

    # parse tree from xml file
    tree = ET.parse(file)
    root = tree.getroot()
    grid = root[grid_id]

    x = grid.find("X")
    x.text = str(eval(config_grid_points[str(grid_id)])["x"])
    y = grid.find("Y")
    y.text = str(eval(config_grid_points[str(grid_id)])["y"])

    # append to xml tree
    ET.indent(tree, space="\t", level=0)
    tree.write(file)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("invalid script arguments")
        quit()
    write_wifi(sys.argv[1], sys.argv[2], sys.argv[3])