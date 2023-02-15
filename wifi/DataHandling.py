#Calculates the sum of errors between corresponding MAC Address of
# data and test locations
#Returns a list of the size len(post_list)
# of rssi numericals differences between matching MAC Addresses of every pos_point and every grid_point
#
#example: len(pos_list) = 5, len(grid_list=10)
# all_errors = [[len=10],[len=10],[len=10],[len=10],[len=10]]
#
#grid_list = list of GridPoints grid data
#pos_list = list of GridPoints position data
#Can only be run as a module

import GridPoint as gd
import pandas as pd

def all_rssi_errors(grid_list, pos_list):

    #list of the Sum of all Errors
    all_errors = []

    #Match every position point with every grid_point.
    #MAC Addresses that do not match are currently not used as extra data
    for pos_point in pos_list:

        #List to hold all rssi difference errors for every grid_point
        errors = []
        for grid_point in grid_list:
            df_pos = pos_point.df
            df_grid = grid_point.df

            #dicts are not labelled as it does not matter
            #Dictionaries to set unique key-value pairs from mac address to rssi for both lists
            dict_1 = df_grid.set_index("mac_ad").to_dict()["rssi"]
            dict_2 = df_pos.set_index("mac_ad").to_dict()["rssi"]
            #dict_1 will add on any rssi values onto the existing key-value pair
            # for any matching MAC Address between both dicts
            for key, value in dict_2.items():
                if key in dict_1:
                    if isinstance(dict_1[key], list):
                        dict_1[key].append(value)
                    else:
                        temp_list = [dict_1[key]]
                        temp_list.append(value)
                        dict_1[key] = temp_list
                else:
                    dict_1[key] = value

            #This list is all key value pairs that did not match. Will be used for later
            rejects = {}

            #Function that returns the difference between key value pairs that have two values
            # and adds any key-value pairs that do not 2 values to a different list
            def f(k, v):
                if isinstance(v, list):
                    return abs(int(v[0]) - int(v[1]))
                else:
                    rejects[k] = v
                    return v

            #Apply the above function to every key in dict_1
            dict = {k: f(k, v) for k, v in dict_1.items()}
            #Remove all keys that weren't used in the above function
            [dict.pop(key) for key in rejects.keys()]

            #Sum up all the values in dict and append them to the errors list
            total_error = sum(dict.values())
            errors.append(total_error)

        all_errors.append(errors)

    return all_errors
#WARNING!!!!
#WARNING!!!!
#ACHTUNG!!!
#Error values are skewed as values that don't have matching MAC Address are ignored


#Get all mac_address that were recorded in data
#def get_relevevant_mac_addresses(gridPoints_list){

   # mac_ads = {}
  #  for grid_point in gridPoints_list:
 #       for df in grid_point.df:
            
#}