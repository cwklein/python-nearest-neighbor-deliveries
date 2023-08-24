import csv
import datetime

from Hash import ChainingHashTable
from Package import loadPackageData
from Location import loadLocationData
from Driver import Driver
from Truck import Truck, fillTruck

# Hash table instances
packageHash = ChainingHashTable()
locationHash = ChainingHashTable()
truckHash = ChainingHashTable()
driverHash = ChainingHashTable()

# Array of ID's for tracking unsent package
unsentPackageIDs = []

# Current Time
currentTime = datetime.time(hour= 8, minute=0)

# Driver instances in driverHash
driver_1 = Driver(1, 'Han Solo', 1, 'Ready')
driver_2 = Driver(2, 'Chewbacca', 2,'Ready')
driverHash.insert(driver_1.ID, driver_1)
driverHash.insert(driver_2.ID,driver_2)

# Truck instances in truckHash
truck_1 = Truck(1,1,'at the hub', None)
truck_2 = Truck(2,2, 'at the hub',None)
truck_3 = Truck(3,None, 'at the hub', None)
truckHash.insert(truck_1.ID, truck_1)
truckHash.insert(truck_2.ID, truck_2)
truckHash.insert(truck_3.ID, truck_3)

# Load packages to Hash Table
loadLocationData('WGUPS Distance File.csv',locationHash)
loadPackageData('WGUPS Package File.csv', packageHash, unsentPackageIDs)


for i in range (1,truckHash.size+1):
    nextTruck = truckHash.search(i)
    truckLoad = fillTruck(packageHash, unsentPackageIDs, currentTime,nextTruck.ID)
    nextTruck = truckHash.search(i)
    nextTruck.packageList = truckLoad

    print("Truck #" + str(i)+ " load size: " + str(len(truckLoad)))
    for package in nextTruck.packageList:
        print(package)


'''
print("Unassigned Packages: " + str(len(unsentPackageIDs)))
for packageID in unsentPackageIDs:
    print(packageHash.search(packageID))

print(currentTime)

'''