class Driver:
    def __init__(self, ID, name, truck,status):
        self.ID = ID
        self.name = name
        self.truck = truck
        self.status = status

    def __str__(self):  # overwrite print(Location) otherwise it will print object reference
        return "%s, %s, %s, %s" % (
            self.ID, self.name, self.truck, self.status)