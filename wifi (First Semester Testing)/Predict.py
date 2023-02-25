#File of localisation prediction methods

#K-Nearest Neighbour
#2D list of rssi difference errors where each index of the larger list corresponds to test position id
# and each index of smaller lists corresponds grid data id
def KNN(all_grid_errors_list, coord_list, n_neighbours):

    predicated_coords_list = []
    for errors_list in all_grid_errors_list:

        #Sort list of errors as index
        #eg. list=[8,9,7] sorted_list=[2,0,1]
        sorted_errors_index = sorted(range(len(errors_list)),
                            key=lambda k: errors_list[k])


        x=0
        y=0
        #Acquire average using midpoint method
        #  ( (x1+x2+...+xn) / n  ) , (y1...
        for i in range(n_neighbours):
            index = sorted_errors_index[i]
            x += coord_list[index][0]
            y += coord_list[index][1]
        x /= n_neighbours
        y /= n_neighbours
        predicated_coords_list.append([x,y])


    return predicated_coords_list