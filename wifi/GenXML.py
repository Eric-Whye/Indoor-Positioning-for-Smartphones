#Generate wifi data grid structure to new xml file
#sys.argv[1] = file path
#sys.argv[2] = number of grid points
#Can be run as a script or as a module


import xml.etree.ElementTree as ET
import sys




def createFile(file, num_grid_points):
    #Creating "data" root
    root = ET.Element("data")

    #Adding branches and sub_branches to root
    for i in range(num_grid_points):

        grid = ET.Element("grid")
        root.append(grid)

        #<root>
        #   <grid id="0">
        #       <X />
        #       <Y / >
        #       <wifi>
        #           <rssi mac_ad="" ssid="">""</rssi>
        #      </wifi>
        #   </grid>
        #   <grid id="1">
        #   ...
        #   ...
        #</root>
        grid.set("id", str(i))
        x = ET.SubElement(grid, "X")
        y = ET.SubElement(grid, "Y")
        wifi = ET.SubElement(grid, "wifi")


    #Writing to xml file
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    with open(file, "wb") as files:
        tree.write(files)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("invalid script arguments")
        quit()
    createFile(sys.argv[1], int(sys.argv[2]))
