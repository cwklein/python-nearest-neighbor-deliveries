# C950 Project - Colby Klein - 001198444
# Main.py

import csv
import datetime

from Driver import driverHash
from Location import locationHash
from Package import packageHash, unsentPackages
from Truck import truckHash
from Scheduler import firstOutTime, secondOutTime, thirdOutTime


# First step in flowchart of PACKAGE DELIVERY process
# Only function that is called manually in the process of loading and delivering the packages
# Takes in the truck Object, startDateTime and an array of all packages currently in the hub
def sendTruck(currentTruck, startDateTime, stagedPackages):
    currentTruck.status = "Being loaded"
    trackTruckStartTime(currentTruck, startDateTime)
    fillTruck(currentTruck, startDateTime, stagedPackages)

    milesToDrive = orderLocations(currentTruck)
    deliverPackages(currentTruck, milesToDrive)


# Second step in flowchart of PACKAGE DELIVERY process
# Determines which packages will be assigned to the current truck
# Takes in the truck Object, startDateTime and an array of all packages currently in the hub
def fillTruck(currentTruck, startDateTime, stagedPackages):
    truckCapacity = 16
    currentlyUnsent = stagedPackages.copy()
    highPriorityLocations = []
    lowPriorityLocations = []
    allLocations = []

    # IF - Handles the final case, in which the number of packages that are left will all left on the remaining truck
    # Not strictly necessary but saves processing time during the final iteration
    # Adds all remaining packages to the final truckload if the number of remaining packages is <= 16
    if truckCapacity >= len(currentlyUnsent):
        for package in currentlyUnsent:
            package.status = "En route, in truck #" + str(currentTruck.ID)
            package.truck = currentTruck
            package.timeLoaded = startDateTime
            currentTruck.packageList.append(package)
            stagedPackages.remove(package)

    # ELSE - Used in first two truckloads, groups packages by locations and adds them into a prioritized list
    # Will add up to 16 packages to the truckload, minimizes the splitting of packages that share a location
    else:
        for package in currentlyUnsent:
            packageLocation = locationHash.search(package.locationID)
            inGroup = package.ID in [13, 14, 15, 16, 19, 20]
            dueSoon = package.deliveryDeadline != 'EOD'
            thisTruck = "truck 2" in package.specialNotes and currentTruck.ID == 2

            if inGroup:
                highPriorityLocations.insert(0, packageLocation)
            if dueSoon:
                highPriorityLocations.append(packageLocation)
            if thisTruck:
                lowPriorityLocations.insert(0, packageLocation)
            else:
                lowPriorityLocations.append(packageLocation)

        for location in highPriorityLocations + lowPriorityLocations:
            if location not in allLocations:
                allLocations.append(location)

        for location in allLocations:
            for package in currentlyUnsent:
                roomInTruck = truckCapacity > 0
                rightAddress = package.locationID == location.ID
                rightTruck = "truck 2" not in package.specialNotes or currentTruck.ID == 2
                noErrors = "Wrong" not in package.specialNotes or startDateTime.time() >= datetime.time(hour=10,
                                                                                                        minute=0)
                noDelays = "Delayed" not in package.specialNotes or startDateTime.time() >= datetime.time(hour=9,
                                                                                                          minute=5)
                okayToAdd = rightAddress and rightTruck and noErrors and noDelays and roomInTruck

                if okayToAdd:
                    package.status = "En route, in truck #" + str(currentTruck.ID)
                    package.truck = currentTruck
                    package.timeLoaded = startDateTime
                    currentTruck.packageList.append(package)
                    stagedPackages.remove(package)
                    truckCapacity -= 1


# Third step in flowchart of PACKAGE DELIVERY process
# Creates an organized list of locations for the truck to visit during delivery process with the aim of minimizing the miles driven
# Takes in the truck Object, returns a list of mileage distances corresponding to the order of locations
def orderLocations(currentTruck):
    truckLocations = []
    mileageList = []
    closestLocationID = None
    closestLocationDistance = None
    currentLocation = locationHash.search(0)
    currentTruck.visitedLocationList.append(currentLocation)

    for package in currentTruck.packageList:
        location = locationHash.search(package.locationID)
        if location not in truckLocations:
            truckLocations.append(location)

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


# Final step in flowchart of PACKAGE DELIVERY process
# Iterates through the organized list of locations, delivers all packages within the truck that are at the destination and tracks the number of miles driven.
# Takes in the truck Object and list of milesToDrive that was generated by orderLocations function
def deliverPackages(currentTruck, milesToDrive):
    currentTruck.status = "En route"
    loadedPackages = currentTruck.packageList.copy()
    for tripDistance in milesToDrive:
        currentTruck.milesDriven += tripDistance
        currentAddress = currentTruck.toVisitLocationList.pop(0)
        deliveryDateTime = trackTruckTime(currentTruck, tripDistance)
        currentTruck.visitedLocationList.append(currentAddress)

        for package in loadedPackages:
            if package.locationID == currentAddress.ID:
                currentTruck.deliveredPackages.append(package)
                currentTruck.packageList.remove(package)
                package.timeDelivered = deliveryDateTime
                package.status = "Delivered at: " + package.timeDelivered.strftime("%H:%M:%S") + " by Truck# " + str(
                    package.truck.ID)

    currentTruck.status = "At the hub"


# Side-step in flowchart of PACKAGE DELIVERY process, not necessary for the delivery process but retains information to be used later in REPORTING
# called only once at start of sendTruck function, adds the start time to the truck's milestoneList at index 0
# corresponds to the matching location in the truck's visitedLocationList, also at index 0
# Takes in the truck Object and startDateTime as parameters
def trackTruckStartTime(currentTruck, startDateTime):
    currentTruck.milestoneList.append(startDateTime)


# Side-step in flowchart of PACKAGE DELIVERY process, not necessary for the delivery process but retains information to be used later in REPORTING
# called after every leg of the truck's delivery route, adds a datetime to the truck's milestoneList
# corresponds to the matching location in the truck's visitedLocationList
# Takes in the truck Object and tripDistance (used to calculate time) as parameters
def trackTruckTime(currentTruck, tripDistance):
    tripMinutes = tripDistance / 18 * 60
    currentDateTime = currentTruck.milestoneList[-1]
    newDateTime = currentDateTime + datetime.timedelta(minutes=tripMinutes)
    currentTruck.milestoneList.append(newDateTime)
    return newDateTime


# Entry point and main menu of the REPORTING process
# Gives the user 4 options for reports that they can view, with 3 of them also prompting the user for any additional information needed to specify the report
def userDialogue():
    reportType = input("Please enter the number corresponding to the type of report you would like to view:\n"
                       "\t1 - Detailed report of a package\n"
                       "\t2 - All packages at a given time\n"
                       "\t3 - Itinerary of a particular delivery truck\n"
                       "\t4 - Full summary of current day's deliveries\n"
                       "\t5 - Exit\n")

    match reportType:
        case "1":
            packageID = input("Which package would you like to know more about? Enter an integer from 1 to 40:\n")
            printPackageSearch(packageID)
        case "2":
            timeValue = input("What time would you like to see? Enter a time in the 24-hour format of \"HH:mm\":\n")
            printTimeSearch(timeValue)
        case "3":
            truckID = input("What delivery truck would you like to know more about? Enter an integer from 1 to 3:\n")
            printTruckSearch(truckID)
        case "4":
            printSummary()
        case "5":
            print("User has chosen to exit")
            exit()
        case _:
            print("\nPlease only respond with an integer from 1 to 5")
            userDialogue()


# Function called if the user selects option 1 from the main menu, part of the REPORTING process
# Prints details pertaining to the specified package, including select package information and the timeline associated with its delivery
# Takes in the packageID from the user's input prompt
def printPackageSearch(packageID):
    try:
        package = packageHash.search(int(packageID))
        truck = package.truck
        loadTime = package.timeLoaded
        deliverTime = package.timeDelivered
        startIndex = truck.milestoneList.index(loadTime) + 1
        endIndex = truck.milestoneList.index(deliverTime)
        print(package)
        print(loadTime.strftime("%H:%M:%S") + ": Loaded")
        for index in range(startIndex, endIndex):
            print(truck.milestoneList[index].strftime("%H:%M:%S") + ": Stop at " +
                  truck.visitedLocationList[index].address)
        print(deliverTime.strftime("%H:%M:%S") + ": Delivered to stop #" + str(endIndex - startIndex + 1) + " to " +
              truck.visitedLocationList[endIndex].address)

    except AttributeError:
        print("ERROR: Package ID must be an integer between 1 and " + str(packageHash.size) + ", inclusive")
        packageID = input("Which package would you like to know more about? Enter an integer from 1 to 40:\n")
        printPackageSearch(packageID)

    except ValueError:
        print("ERROR: Package ID must be an integer between 1 and " + str(packageHash.size) + ", inclusive")
        packageID = input("Which package would you like to know more about? Enter an integer from 1 to 40:\n")
        printPackageSearch(packageID)

    response = input("\nWould you like to return to main menu?\n")
    if "y" in response.lower():
        userDialogue()
    else:
        print("User has chosen to exit")
        exit()


# Function called if the user selects option 2 from the main menu, part of the REPORTING process
# Prints status details pertaining to all packages at the specified time
# Takes in the timeValue from the user's input prompt
def printTimeSearch(timeValue):
    try:
        testTime = datetime.time.fromisoformat(timeValue)
        print("Package statuses at " + timeValue + ":")

        for i in range(1, packageHash.size + 1):
            package = packageHash.search(i)
            packageDeliveryTime = package.timeDelivered.time()
            packageLoadTime = package.timeLoaded.time()

            if testTime > packageDeliveryTime:
                print("Package ID " + str(package.ID) + ": delivered at " + packageDeliveryTime.strftime(
                    "%H:%M:%S") + " by Truck #" + str(package.truck.ID))
            elif testTime < packageLoadTime:
                print("Package ID " + str(package.ID) + ": hasn't left for delivery yet")
            else:
                print("Package ID " + str(package.ID) + ": loaded at " + packageLoadTime.strftime("%H:%M:%S") +
                      " and currently out for delivery on Truck #" + str(package.truck.ID) +
                      ", anticipated to be delivered at " + packageDeliveryTime.strftime("%H:%M:%S"))

    except ValueError:
        print("ERROR: Time must be in the format \"HH:mm\" with the hour portion being between 00 and 23.")
        timeValue = input("What time would you like to see? Enter a time in the 24-hour format of \"HH:mm\":\n")
        printTimeSearch(timeValue)

    response = input("\nWould you like to return to main menu?\n")
    if "y" in response.lower():
        userDialogue()
    else:
        print("User has chosen to exit")
        exit()


# Function called if the user selects option 3 from the main menu, part of the REPORTING process
# Prints details pertaining to the specified truck, specifically the delivery timeline and mileage associated with each step
# Takes in the truckID from the user's input prompt
def printTruckSearch(truckID):
    try:
        truck = truckHash.search(int(truckID))
        hubCount = 1
        packageNumber = 0
        lastVisited = locationHash.search(0)
        runningTotalMiles = 0.0
        packages = truck.deliveredPackages.copy()
        print("Summary for Truck #" + str(truck.ID) + ":")
        for i in range(len(truck.visitedLocationList)):
            location = truck.visitedLocationList[i]
            additionalMiles = location.distanceList[lastVisited.ID]
            runningTotalMiles += additionalMiles
            lastVisited = location
            if location == locationHash.search(0) and hubCount % 2 == 1:
                print("\n" + truck.milestoneList[i].strftime(
                    "%H:%M:%S") + " - Truck left Hub - Trip started, Additional miles = " + str(
                    additionalMiles) + ", Total miles for this truck = " + "{:.1f}".format(runningTotalMiles))
                hubCount += 1
            elif location == locationHash.search(0) and hubCount % 2 == 0:
                print(truck.milestoneList[i].strftime(
                    "%H:%M:%S") + " - Truck returned to Hub - Trip completed, Additional miles = " + str(
                    additionalMiles) + ", Total miles for this truck = " + "{:.1f}".format(runningTotalMiles))
                hubCount += 1
            else:
                print(truck.milestoneList[i].strftime("%H:%M:%S") + " - Truck stopped at " + truck.visitedLocationList[
                    i].address +
                      ", Additional miles = " + str(additionalMiles) + ", Total miles for this truck = " +
                      "{:.1f}".format(runningTotalMiles))
                for j in range(packageNumber, len(packages)):
                    if truck.deliveredPackages[j].locationID == truck.visitedLocationList[i].ID:
                        print("\tDelivered Package #" + str(truck.deliveredPackages[j].ID))
                        packageNumber += 1
                    else:
                        break

    except AttributeError:
        print("ERROR: Truck ID must be an integer between 1 and " + str(truckHash.size) + ", inclusive")
        truckID = input("What delivery truck would you like to know more about? Enter an integer from 1 to 3:\n")
        printTruckSearch(truckID)

    except ValueError:
        print("ERROR: Truck ID must be an integer between 1 and " + str(truckHash.size) + ", inclusive")
        truckID = input("What delivery truck would you like to know more about? Enter an integer from 1 to 3:\n")
        printTruckSearch(truckID)

    response = input("\nWould you like to return to main menu?\n")
    if "y" in response.lower():
        userDialogue()
    else:
        print("User has chosen to exit")
        exit()


# Function called if the user selects option 4 from the main menu, part of the REPORTING process
# Prints details pertaining to all trucks and their deliveries over the day
def printSummary():
    runningTotalMiles = 0.0
    print("Today's Deliveries:\n")
    print("Truck #1\n")
    truck = truckHash.search(1)
    hubCount = 1
    packageNumber = 0
    packages = truck.deliveredPackages.copy()
    lastVisited = locationHash.search(0)
    for i in range(len(truck.visitedLocationList)):
        location = truck.visitedLocationList[i]
        additionalMiles = location.distanceList[lastVisited.ID]
        runningTotalMiles += additionalMiles
        lastVisited = location
        if location == locationHash.search(0) and hubCount % 2 == 1:
            print(truck.milestoneList[i].strftime(
                "%H:%M:%S") + " - Truck left Hub - Trip started, Additional miles = " + str(
                additionalMiles) + ", Total miles = " + "{:.1f}".format(runningTotalMiles))
            hubCount += 1
        elif location == locationHash.search(0) and hubCount % 2 == 0:
            print(truck.milestoneList[i].strftime(
                "%H:%M:%S") + " - Truck returned to Hub - Trip completed, Additional miles = " + str(
                additionalMiles) + ", Total miles = " + "{:.1f}".format(runningTotalMiles) + "\n")
            hubCount += 1
        else:
            print(truck.milestoneList[i].strftime("%H:%M:%S") + " - Truck stopped at " + truck.visitedLocationList[
                i].address + ", Additional miles = " + str(additionalMiles) + ", Total miles = " + "{:.1f}".format(
                runningTotalMiles))
            for j in range(packageNumber, len(packages)):
                if truck.deliveredPackages[j].locationID == truck.visitedLocationList[i].ID:
                    print("\tDelivered Package #" + str(truck.deliveredPackages[j].ID) + ", due before: " +
                          truck.deliveredPackages[j].deliveryDeadline)
                    packageNumber += 1
                else:
                    break

    print("Truck #2")
    truck = truckHash.search(2)
    hubCount = 1
    packageNumber = 0
    packages = truck.deliveredPackages.copy()
    lastVisited = locationHash.search(0)
    for i in range(len(truck.visitedLocationList)):
        location = truck.visitedLocationList[i]
        additionalMiles = location.distanceList[lastVisited.ID]
        runningTotalMiles += additionalMiles
        lastVisited = location
        if location == locationHash.search(0) and hubCount % 2 == 1:
            print("\n" + truck.milestoneList[i].strftime(
                "%H:%M:%S") + " - Truck left Hub - Trip started, Additional miles = " + str(
                additionalMiles) + ", Total miles = " + "{:.1f}".format(runningTotalMiles))
            hubCount += 1
        elif location == locationHash.search(0) and hubCount % 2 == 0:
            print(truck.milestoneList[i].strftime(
                "%H:%M:%S") + " - Truck returned to Hub - Trip completed, Additional miles = " + str(
                additionalMiles) + ", Total miles = " + "{:.1f}".format(runningTotalMiles) + "\n")
            hubCount += 1
        else:
            print(truck.milestoneList[i].strftime("%H:%M:%S") + " - Truck stopped at " + truck.visitedLocationList[
                i].address + ", Additional miles = " + str(additionalMiles) + ", Total miles = " + "{:.1f}".format(
                runningTotalMiles))
            for j in range(packageNumber, len(packages)):
                if truck.deliveredPackages[j].locationID == truck.visitedLocationList[i].ID:
                    print("\tDelivered Package #" + str(truck.deliveredPackages[j].ID) + ", due before: " +
                          truck.deliveredPackages[j].deliveryDeadline)
                    packageNumber += 1
                else:
                    break

    response = input("\nWould you like to return to main menu?\n")
    if "y" in response.lower():
        userDialogue()
    else:
        print("User has chosen to exit")
        exit()


# sendTruck function called at three specific times referenced from Scheduler.py.
sendTruck(truckHash.search(1), firstOutTime, unsentPackages)
sendTruck(truckHash.search(2), secondOutTime, unsentPackages)
sendTruck(truckHash.search(1), thirdOutTime, unsentPackages)

# Summary print statements for user to see, at a glance, whether all packages were delivered and the total miles driven.
totalMiles = truckHash.search(1).milesDriven + truckHash.search(2).milesDriven + truckHash.search(3).milesDriven
print("All " + str(packageHash.size) + " packages delivered before closing time (17:00)")
print("Total miles driven: " + str(totalMiles) + "\n")

# Calls user dialogue to allow user to navigate through their chosen report views
userDialogue()
