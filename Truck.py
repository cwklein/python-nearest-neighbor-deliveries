import datetime


class Truck:
    def __init__(self, ID, driver, status,packageList):
        self.ID = ID
        self.driver = driver
        self.status = status
        self.packageList = packageList
        self.milesDriven = 0

    def __str__(self):  # overwrite print(Location) otherwise it will print object reference
        return "%s, %s, %s, Miles driven: %5, Number of Packages: %s" % (
            self.ID, self.driver, self.status, self.milesDriven,  str(len(self.packageList)))


def fillTruck(packageHash, unsentPackageIDs, currentTime, truckID):
    truckCapacity = 16
    truckLoad = []
    truckAddresses = []
    tempUnsent = unsentPackageIDs.copy()

    for packageID in tempUnsent:
        package = packageHash.search(packageID)
        if (package.deliveryDeadline != "EOD" or (("truck 2" in package.specialNotes) and (truckID == 2) )) and package.address not in truckAddresses:
            truckAddresses.append(package.address)

    if 19 in unsentPackageIDs:
        truckAddresses.append(packageHash.search(19).address)

    for address in truckAddresses:
        ready = True
        for packageID in tempUnsent:
            package = packageHash.search(packageID)
            if (address in package.address) and (("Delayed" in package.specialNotes) and (currentTime < datetime.time(hour= 9, minute=5)) or (("truck 2" in package.specialNotes) and (truckID != 2) )):
                ready = False
        if ready:
            for packageID in tempUnsent:
                package = packageHash.search(packageID)
                if (address in package.address) and (("Wrong" not in package.specialNotes) or (currentTime > datetime.time(hour= 10, minute=20))):
                    package.status = "loaded and waiting to leave"
                    truckLoad.append(package)
                    unsentPackageIDs.remove(packageID)
                    truckCapacity -= 1

    tempUnsent = unsentPackageIDs.copy()


    return truckLoad


    # for packageID in unsentPackageIDs:
    #     package = packageHash.search(packageID)
    #     if package.deliveryDeadline != "EOD" and ("Delayed" and "Wrong") not in package.specialNotes:
    #         if truckCapacity > 0:
    #             truckLoad.append(package)
    #             truckAddresses.append(package.address)
    #             package.status = "en route"
    #             unsentPackageIDs.remove(packageID)
    #             truckCapacity -= 1
    #
    # for refPackage in truckLoad:
    #     if truckCapacity > 0 and "Must be delivered with" in refPackage.specialNotes:
    #         specialNotes = str(refPackage.specialNotes)
    #         try:
    #             commaIndex = specialNotes.index(',')
    #             id1 = specialNotes[commaIndex-2: commaIndex]
    #             id2 = specialNotes[commaIndex+2:]
    #             if truckCapacity > 0 and id1 in unsentPackageIDs:
    #                 package = packageHash.search(id1)
    #                 truckLoad.append(package)
    #                 truckAddresses.append(package.address)
    #                 package.status = "en route"
    #                 unsentPackageIDs.remove(id1)
    #                 truckCapacity -= 1
    #             if truckCapacity > 0 and id2 in unsentPackageIDs:
    #                 package = packageHash.search(id2)
    #                 truckLoad.append(package)
    #                 truckAddresses.append(package.address)
    #                 package.status = "en route"
    #                 unsentPackageIDs.remove(id2)
    #                 truckCapacity -= 1
    #         except:
    #             id = specialNotes[-2:]
    #             if truckCapacity > 0 and id in unsentPackageIDs:
    #                 package = packageHash.search(id)
    #                 truckLoad.append(package)
    #                 truckAddresses.append(package.address)
    #                 package.status = "en route"
    #                 unsentPackageIDs.remove(id)
    #                 truckCapacity -= 1
    #
    # for packageID in unsentPackageIDs:
    #     package = packageHash.search(packageID)
    #     if package.address in truckAddresses and truckCapacity>0:
    #         truckLoad.append(package)
    #         package.status = "en route"
    #         unsentPackageIDs.remove(packageID)
    #         truckCapacity -= 1
