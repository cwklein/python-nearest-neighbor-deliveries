import csv
from Hash import ChainingHashTable


class Package:
    def __init__(self, ID, locationID, address, city, state, zipcode,
                 deliveryDeadline, weightKILO, specialNotes, status):
        self.ID = ID
        self.locationID = locationID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deliveryDeadline = deliveryDeadline
        self.weightKILO = weightKILO
        self.specialNotes = specialNotes
        self.status = status
        self.truck = None
        self.timeLoaded = None
        self.timeDelivered = None

    def __str__(self):  # overwrite print(Package) otherwise it will print object reference
        return "Package %s: (%s, %s, %s, %s) deadline: %s, weight: %s, special note: %s, status: %s" % (
            self.ID, self.address, self.city, self.state, self.zipcode, self.deliveryDeadline, self.weightKILO,
            self.specialNotes, self.status)


def loadPackageData(fileName, targetHash):
    with open(fileName) as packageList:
        packageData = csv.reader(packageList, delimiter=',')
        next(packageData)
        for package in packageData:
            ID = int(package[0])
            locationID = int(package[1])
            address = str(package[2])
            city = package[3]
            state = package[4]
            zipcode = package[5]
            deliveryDeadline = package[6]
            weightKILO = package[7]
            specialNotes = package[8]
            status = "at the hub"

            # package object
            newPackage = Package(ID, locationID, address, city, state, zipcode,
                                 deliveryDeadline, weightKILO, specialNotes, status)

            # insert package into the hash table
            targetHash.insert(ID, newPackage)

            # insert package into list of unsent packages
            unsentPackages.append(newPackage)


unsentPackages = []
packageHash = ChainingHashTable()

loadPackageData('WGUPS Package File.csv', packageHash)
