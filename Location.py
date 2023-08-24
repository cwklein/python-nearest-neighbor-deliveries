import csv


class Location:
    def __init__(self, ID, fullAddress, address):
        self.ID = ID
        self.fullAddress = fullAddress
        self.address = address

    def __str__(self):  # overwrite print(Location) otherwise it will print object reference
        return "%s, %s, %s, %s" % (
            self.ID, self.fullAddress, self.address)


def loadLocationData(fileName, locationHash):
    with open(fileName) as locationList:
        locationData = csv.reader(locationList, delimiter=',')
        next(locationData)
        next(locationData)
        for location in locationData:
            ID = int(location[0])
            fullAddress = location[1]
            address = location[2]

            # create location object
            newLocation = Location(ID, fullAddress,address)

            # insert location object into the hash table
            locationHash.insert(ID, newLocation)
