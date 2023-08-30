# Location.py

import csv
from Hash import ChainingHashTable


class Location:
    def __init__(self, ID, fullAddress, address, distanceList):
        self.ID = ID
        self.fullAddress = fullAddress
        self.address = address
        self.distanceList = distanceList

    def __str__(self):
        return "%s, %s, %s" % (
            self.ID, self.fullAddress, self.address)


def loadLocationData(fileName, targetHash):
    with open(fileName) as locationList:
        locationData = csv.reader(locationList, delimiter=',')
        next(locationData)
        next(locationData)
        for location in locationData:
            ID = int(location[0])
            fullAddress = location[1]
            address = location[2]
            distanceList = [float(location[3]), float(location[4]), float(location[5]), float(location[6]),
                            float(location[7]), float(location[8]), float(location[9]), float(location[10]),
                            float(location[11]), float(location[12]), float(location[13]), float(location[14]),
                            float(location[15]), float(location[16]), float(location[17]), float(location[18]),
                            float(location[19]), float(location[20]), float(location[21]), float(location[22]),
                            float(location[23]), float(location[24]), float(location[25]), float(location[26]),
                            float(location[27]), float(location[28]), float(location[29])]

            # create location object
            newLocation = Location(ID, fullAddress, address, distanceList)

            # insert location object into the hash table
            targetHash.insert(ID, newLocation)


locationHash = ChainingHashTable()

loadLocationData('WGUPS Distance File.csv', locationHash)
