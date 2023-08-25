import csv
import datetime

from Driver import driverHash
from Location import locationHash
from Package import packageHash, unsentPackages
from Truck import truckHash
from Scheduler import firstOutTime, secondOutTime, thirdOutTime


def sendTruck(currentTruck, startDateTime, stagedPackages):
    currentTruck.status = "loading"
    trackTruckStartTime(currentTruck, startDateTime)
    truckLocations = fillTruck(currentTruck, startDateTime, stagedPackages)

    # Test start
    print("Truck #" + str(currentTruck.ID) + " load size: " + str(len(currentTruck.packageList)))
    for package in currentTruck.packageList:
        print(package)
    # Test end

    milesToDrive = orderLocations(truckLocations, currentTruck)
    deliverPackages(currentTruck, milesToDrive)


# Test start
#     print(milesToDrive)
# Test end

def fillTruck(currentTruck, startDateTime, stagedPackages):
    truckCapacity = 16
    currentlyUnsent = stagedPackages.copy()
    truckLocations = []

    # Determining which packages will go on the truck
    # if captures when all packages will fit on last truck
    if len(currentlyUnsent) <= truckCapacity:
        for package in currentlyUnsent:
            packageLocation = locationHash.search(package.locationID)
            if packageLocation not in truckLocations:
                truckLocations.append(packageLocation)
    # else captures when all packages won't fit on last truck
    else:
        for package in currentlyUnsent:
            packageLocation = locationHash.search(package.locationID)
            if (package.ID == 19 or package.deliveryDeadline != "EOD" or (
                    ("truck 2" in package.specialNotes) and (currentTruck.ID == 2))) and (
                    packageLocation not in truckLocations):
                truckLocations.append(packageLocation)

    # package list is determined for this truck, now putting packages on truck and updating package status
    for location in truckLocations:
        ready = True
        for package in currentlyUnsent:
            if (location.ID == package.locationID) and (("Delayed" in package.specialNotes) and (startDateTime.time() < datetime.time(hour=9, minute=5)) or (("truck 2" in package.specialNotes) and (currentTruck.ID != 2))):
                ready = False
        if ready:
            for package in currentlyUnsent:
                if (location.ID == package.locationID) and (("Wrong" not in package.specialNotes) or (
                        startDateTime.time() > datetime.time(hour=10, minute=20))):
                    package.status = "in truck #" + str(currentTruck.ID)
                    currentTruck.packageList.append(package)
                    stagedPackages.remove(package)
                    truckCapacity -= 1
    return truckLocations


def orderLocations(truckLocations, currentTruck):
    mileageList = []
    closestLocationID = None
    closestLocationDistance = None
    currentLocation = locationHash.search(0)
    currentTruck.visitedLocationList.append(currentLocation)

    while len(truckLocations) > 0:
        for location in truckLocations:
            ID = location.ID
            distance = currentLocation.distanceList[ID]
            if closestLocationDistance is None or distance < closestLocationDistance:
                closestLocationDistance = distance
                closestLocationID = ID

        mileageList.append(closestLocationDistance)
        nextLocation = locationHash.search(closestLocationID)
        currentTruck.toVisitLocationList.append(nextLocation)
        truckLocations.remove(nextLocation)
        currentLocation = nextLocation
        closestLocationID = None
        closestLocationDistance = None

    distance = currentLocation.distanceList[0]
    mileageList.append(distance)
    nextLocation = locationHash.search(0)
    currentTruck.toVisitLocationList.append(nextLocation)

    return mileageList


def deliverPackages(currentTruck, milesToDrive):
    currentTruck.status = "delivering"
    loadedPackages = currentTruck.packageList.copy()
    for tripDistance in milesToDrive:
        currentTruck.milesDriven += tripDistance
        deliveryDateTime = trackTruckTime(currentTruck, tripDistance)
        currentAddress = currentTruck.toVisitLocationList.pop(0)
        currentTruck.visitedLocationList.append(currentAddress)

        for package in loadedPackages:
            if package.locationID == currentAddress.ID:
                currentTruck.packageList.remove(package)
                package.status = "Delivered at: " + deliveryDateTime.strftime("%H:%M:%S") + ", by Truck# " + str(
                    currentTruck.ID)

    currentTruck.status = "at the hub"


def trackTruckStartTime(currentTruck, startDateTime):
    currentTruck.milestoneList.append(startDateTime)


def trackTruckTime(currentTruck, tripDistance):
    tripMinutes = tripDistance / 18 * 60
    currentDateTime = currentTruck.milestoneList[-1]
    newDateTime = currentDateTime + datetime.timedelta(minutes=tripMinutes)
    currentTruck.milestoneList.append(newDateTime)
    return newDateTime


sendTruck(truckHash.search(1), firstOutTime, unsentPackages)
sendTruck(truckHash.search(2), secondOutTime, unsentPackages)
sendTruck(truckHash.search(1), thirdOutTime, unsentPackages)
print(truckHash.search(1).milestoneList)
print(truckHash.search(2).milestoneList)
print(str(truckHash.search(1).milesDriven + truckHash.search(2).milesDriven + truckHash.search(3).milesDriven))
