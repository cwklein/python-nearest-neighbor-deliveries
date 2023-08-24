import csv


class Package:
    def __init__(self, ID, address, city, state, zip, deliveryDeadline, weightKILO, specialNotes, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deliveryDeadline = deliveryDeadline
        self.weightKILO = weightKILO
        self.specialNotes = specialNotes
        self.status = status

    def __str__(self):  # overwrite print(Package) otherwise it will print object reference
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (
            self.ID, self.address, self.city, self.state, self.zip, self.deliveryDeadline, self.weightKILO,
            self.specialNotes, self.status)


def loadPackageData(fileName, packageHash, unsentPackageIDs):
    with open(fileName) as packageList:
        packageData = csv.reader(packageList, delimiter=',')
        next(packageData)
        for package in packageData:
            ID = int(package[0])
            address = str(package[1])
            city = package[2]
            state = package[3]
            zip = package[4]
            deliveryDeadline = package[5]
            weightKILO = package[6]
            specialNotes = package[7]
            status = "at the hub"

            # package object
            newPackage = Package(ID, address, city, state, zip, deliveryDeadline, weightKILO, specialNotes, status)

            # insert it into the hash table
            packageHash.insert(ID, newPackage)

            # insert package ID into list of unsent packages
            unsentPackageIDs.append(ID)
