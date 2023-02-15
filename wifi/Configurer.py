#Configuration parameters of whole project
#Must be run as a script with no arguments taken

import configparser

if __name__ == "__main__":
    config = configparser.ConfigParser()

    xml_dir = "xml"
    config["paths"] = {"xml_data": f"{xml_dir}\\data.xml",
                       "xml_pos": f"{xml_dir}\\positions.xml"
                       }

    config["relevant_ssid"] = {0: "eduroam",
                               1: "UCD Wireless"}

    rawDataDir = "raw data files"
    #Name convention of position data files
    pos_name = "positions-"
    config["positions"] = {"num_Positions": 5,
                           "filepath": f"{rawDataDir}\\{pos_name}",
                           "ext": ".csv"}

    #Name convention of raw data files
    data_name = "Grid-Data2"
    config["grid"] = {"numGridPoints": 10,
                      "filepath": f"{rawDataDir}\\{data_name}",
                      "ext": ".csv"}

    config["grid_points"] = {0: {"x": 4,"y": 18},
                             1: {"x": 6,"y": 18},
                             2: {"x": 4,"y": 20},
                             3: {"x": 6,"y": 20},
                             4: {"x": 4,"y": 22},
                             5: {"x": 6,"y": 22},
                             6: {"x": 4,"y": 24},
                             7: {"x": 6,"y": 24},
                             8: {"x": 4,"y": 26},
                             9: {"x": 6,"y": 26}
                             }

    with open("config.ini", "w") as configfile:
        config.write(configfile)