from Hash import ChainingHashTable


class Truck:
    def __init__(self, ID, driver, status):
        self.ID = ID
        self.driver = driver
        self.status = status
        self.packageList = []
        self.deliveredPackages = []
        self.milesDriven = 0.0
        self.milestoneList = []
        self.visitedLocationList = []
        self.toVisitLocationList = []

    def __str__(self):  # overwrite print(Location) otherwise it will print object reference
        return "%s, %s, %s, Last location: %s, Next Locations: %s, Miles driven: %s, Number of Packages: %s" % (
            self.ID, self.driver, self.status, locationHash.search(self.visitedLocationList[0]).address,
            self.toVisitLocationList, self.milesDriven,  str(len(self.packageList)))


truckHash = ChainingHashTable()

# Truck instances in truckHash
truck_1 = Truck(1, 1, "at the hub")
truck_2 = Truck(2, 2, "at the hub")
truck_3 = Truck(3, None, "at the hub")
truckHash.insert(truck_1.ID, truck_1)
truckHash.insert(truck_2.ID, truck_2)
truckHash.insert(truck_3.ID, truck_3)
