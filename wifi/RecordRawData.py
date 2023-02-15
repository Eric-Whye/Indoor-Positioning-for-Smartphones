#To Do To be changed to record grid AND position data
#Record raw wifi date using WifiInfoView program
#sys.argv[1] = grid_id
#Currently only runnable as a script.  Will in future be run as a module as well

import subprocess
import configparser
import sys


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("invalid script arguments")
        quit()

    # Read config file
    config = configparser.ConfigParser()
    config.read("config.ini")
    config_paths = config["paths"]
    config_grid = config["grid"]

    #config params
    filename = config_grid["filename"]
    #Call to WifiInfoView.exe tool to record wifi
    subprocess.call(f"WifiInfoView.exe /scomma \"{filename}{sys.argv[1]}.csv\"")
    print(f"Raw Wifi Data recorded in \"{filename}{sys.argv[1]}.csv\"")
