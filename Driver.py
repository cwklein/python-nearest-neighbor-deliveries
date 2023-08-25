from Hash import ChainingHashTable


class Driver:
    def __init__(self, ID, name, truck, status):
        self.ID = ID
        self.name = name
        self.truck = truck
        self.status = status

    def __str__(self):  # overwrite print(Location) otherwise it will print object reference
        return "%s, %s, %s, %s" % (
            self.ID, self.name, self.truck, self.status)


driverHash = ChainingHashTable()

# Driver instances in driverHash
driver_1 = Driver(1, 'Han Solo', 1, 'Assigned')
driver_2 = Driver(2, 'Chewbacca', 2, 'Assigned')
driverHash.insert(driver_1.ID, driver_1)
driverHash.insert(driver_2.ID, driver_2)
