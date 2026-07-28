'''
by Reactor02

17.05.2026 (End Date)
27.07.2026 (Update v1.2)

refer to README.md for help on how to use (not help with reading it)

If you try to read this code
you may need some tomato sauce for this spaghetti
and maybe your Blåhaj too (I certainly did when making v1.2)
'''

import random, os, sys

def clear(): # clears the teriminal with 'cls' if on Windows and 'clear' otherwise
    os.system("cls" if os.name == "nt" else "clear")

def changeCar(carFile,modifyList): # rewriting the modifyCar() code now that I am a better programmer (maybe)
    global modifyMin, modifyMax

    # opening the .car file as byte read and copying the data to a list, then closing the file
    tempFile = open("imports/" + carFile, "br")
    carData = tempFile.readlines()
    tempFile.close()

    # copying the 10(?) bytes (exluding the two bytes for ending a line) of lines 3-17 and 20-34 into a list, this has the needed data)
    # also putting them into a 2D array, column 1 will be for deviation/min and column 2 will be for mean/max
    importList = []
    for i in range(2,17):
        importList.append([carData[i][-10:-2], carData[i + 17][-10:-2]])

    # filtering through the array for only the data I actually need (ones getting modified)

    # this array has all the inputs for each rating and labels (I don't know how to explain this, just look at it)
    # ignore the minorly weird format
    ratingList = [
            ['0','aiParamDriverAgression'],
            ['1','aiParamDriverConsistency'],
            ['2','aiParamDriverFinishing'],
            ['3','aiParamDriverQualifying'],
            ['4','aiParamDriverRoadCourse'],
            ['5','aiParamDriverShortTrack'],
            ['6','aiParamDriverSpeedway'],
            ['7','aiParamDriverSuperspeedway'],
            ['8','aiParamPitcrewConsistency'],
            ['9','aiParamPitcrewSpeed'],
            ['A','aiParamPitcrewStrategy','a'],
            ['B','aiParamVehicleAero','b'],
            ['C','aiParamVehicleChassis','c'],
            ['D','aiParamVehicleEngine','d'],
            ['E','aiParamVehicleReliability','e'],
            ]
    # now it's time to actually filter the data

    exportList = importList
    importList = []

    # goes through 'exportList' (formerly 'importList') and adds it to importList if it was requested
    for i in range(15):
        for n in modifyList:
            if n in ratingList[i]:
                importList.append(exportList[i])

    # this next section is for converting the byte data into min/max format seen in game

    for i in range(len(importList)): 
        for n in range(2):
            importList[i][n] = float(importList[i][n].decode("utf-8")) # this converts the byte data into a string and then a float usable by python

        # the ratings are stored as deviation and mean (dev/mean) in the .car file, so we need to convert from that next
        # conversion from dev/mean to min/max is as follows (reverse will be later)
        # min = (mean * 50) - (dev * 100)
        # max = (mean * 50) + (dev * 100)
        tempMean = importList[i][1] * 50
        tempDev = importList[i][0] * 100
        importList[i] = [int(tempMean - tempDev),int(tempMean + tempDev)]

    # Time to actually modify the values
    for i in range(len(importList)):
        match modifyMin[0]:
            case 1: # set
                importList[i][0] = modifyMin[1]
            case 2: # increment
                importList[i][0] += modifyMin[1]
            case 3: # random
                importList[i][0] = random.randint(modifyMin[1]-1,modifyMin[2])
            case _: # other / no change
                pass # I think it is necessary to have this last case despite doing literally nothing
            
            # same as above but with the maximum, so no comments
        match modifyMax[0]:
            case 1:
                importList[i][1] = modifyMax[1]
            case 2:
                importList[i][1] += modifyMax[1]
            case 3:
                importList[i][1] = random.randint(modifyMax[1] - 1,modifyMax[2])
            case _:
                pass
        importList[i].sort() # just incase the min is greater than the max, swap them
    
    # converting the modified values back into the original byte data
    for i in range(len(importList)):
        # first converting the min/max into dev/mean
        # formula is as follows
        # deviation = ( max - ( min + max ) * 0.5) * 0.01
        # mean = ( min + max ) * 0.01
        importList[i][0],importList[i][1] = (importList[i][1] - (importList[i][0] + importList[i][1]) * 0.5 ) * 0.01, (importList[i][0] + importList[i][1]) * 0.01

        # converting back into bytes, first by making them strings
        for n in range(2):
            importList[i][n] = str(importList[i][n])
            while len(importList[i][n]) != 8: # if the string has a length more than 8, truncate it down to 8, otherwise keep appending '0' until it is length 8
                if len(importList[i][n]) > 8:
                    importList[i][n] = importList[i][n][0:8]
                else:
                    importList[i][n] = importList[i][n] + "0"
            # now turning it into bytes
            importList[i][n] = importList[i][n].encode("utf-8")

    # bringing the modified data back into the exportList similarly to how I filtered them out
    # also adding some additional things to prepare for actually exporting (like "\r\n" at the end of each line)
    for i in range(15):
        for n in modifyList:
            if n in ratingList[i]:
                exportList[i] = importList[0]
                del importList[0]
        for n in range(2):
            exportList[i][n] = ratingList[i][1] + "=" + exportList[i][n].decode("utf-8") + "\r\n"
            exportList[i][n] = exportList[i][n].encode("utf-8")

    # re-adding exportList to carData
    for i in range(15):
        carData[i + 2] = exportList[i][0]
        carData[i + 19] = exportList[i][1]

    # now exporting to a .car file
    tempFile = open("exports/" + carFile , "bw") # opening a the .car file (in exports/) as write
    tempFile.writelines(carData)
    tempFile.close()

    print("Succesfully edited " + carFile)

# used to determine what ratings the user wants to modify and how

def modifyMenu(carFile,bulk=False):
    global modifyMin
    global modifyMax

    clear()
    print("\nWhat would you like to modify?\n\nDriver -\n0: Agression\n1: Consistency\n2: Finishing\n3: Qualifying\n4: Road Course\n5: Short Track\n6: Speedway\n7: Superspeedway\n\nPitcrew -\n8: Consistency\n9: Speed\nA: Strategy\n\nVehicle -\nB: Aero\nC: Chassis\nD: Engine\nE: Reliability\n")

# forcing a valid input

    tempInput = "NO"
    while testTempInput(tempInput):
        tempInput = str(input())

# cleaning up the input by putting it into a list, removing dupes, and sorting it
    
    modifyList = []
    for i in tempInput:
        modifyList.append(i)
    modifyList = list(set(modifyList))
    modifyList.sort()

# asking what modifications are wanted
    
    # 'modifyMin' / 'modifyMax' are lists with the first item identifying what it is for and the 2nd (and 3rd) being int values

    if yesNo("\nDo you want to modify the minimum?"):
        match threeChoice("How do you want to modifiy the minimum?"):
            case 0:
                modifyMin = [1,int(input("\nWhat number is the minimum?: "))]
            case 1:
                modifyMin = [2,int(input("\nHow much to increase/decrease by?: "))]
            case 2:
                modifyMin = [3,int(input("\nWhat is the minimum of the range?: ")),int(input("What is the maximum of the range?: "))]
    else:
        modifyMin = [0]

    if yesNo("\nDo you want to modify the maximum?"):
        match threeChoice("How do you want to modify the maximum?"):
            case 0:
                modifyMax = [1,int(input("\nWhat number is the maximum?: "))]
            case 1:
                modifyMax = [2,int(input("\nHow much to increase/decrease by?: "))]
            case 2:
                modifyMax = [3,int(input("\nWhat is the minimum of the range?: ")),int(input("What is the maximum of the range?: "))]
    else:
        modifyMax = [0]

# modifying the cars now
    print()

    if bulk:
        for i in carFile:
            changeCar(i,modifyList)
    else:
        changeCar(carFile,modifyList)


# used to verify and return a value for tempInput in modifyMenu

def testTempInput(tempInput): # if 'tempInput' does not follow the rules, returns True, otherwise returns False
    if len(tempInput) == 0 or len(tempInput) > 15:
        return True

# returns True if a character is not a digit and not in the first 5 letters of the alphabet
    
    tempList = ["A","B","C","D","E","a","b","c","d","e"]
    for i in tempInput:
        if not i.isdigit() and not i in tempList:
            return  True
    return False

# asks for a y/n question and returns T/F

def yesNo(text):
    answer = 1
    possible = ["y","Y","N","n"]
    while not(answer in possible):
        answer = str(input(text + " (y/n): "))
    if answer == "y" or answer == "Y":
        return True
    else:
        return False

# for determining what modification to a rating is wanted

def threeChoice(text): # returns int 0, 1, or 2
    answer = 6
    print("\n" + text + "\n0: Set\n1: Increase/Decrease\n2: Random between\n")
    while answer > 2 or answer < 0:
        answer = int(input())
    return answer

# global variables

modifyMin = [0]
modifyMax = [0]

# basic code loop

while True:

    # determining what process to start via user input
    clear()
    print("\nWhen asked for file names, do include file extensions like gns.car and .lst\n\nWhat would you like to do?\n\n0: Exit\n1: Modify one car\n2: Bulk Modify\n")

    tempInput = 6
    while tempInput > 2 or tempInput < 0:
        tempInput = int(input())

    match tempInput:
        case 0:
            clear()
            sys.exit()
        case 1:
            # asks user for input file then executes program

            carFile = str(input("\nName of the car file: "))

            while not os.path.isfile("imports/" + carFile):
                print("\n'" + carFile + "' does not exist in the imports folder")
                carFile = str(input("Name of the car file: "))

            modifyMenu(carFile)
        case 2:

            # asks user for input file then gets a list of all valid cars in that list

            listName = str(input("\nName of the list file: "))

            while not os.path.isfile("imports/" + listName):
                print("\n'" + listName + "' does not exist in the imports folder")
                listName = str(input("\nName of the list file: "))

            openedList = open("imports/" + listName)

            validCars = []
            inValidCars = 0
            print("\n")
            for i in openedList:
                if i[0] == "+":
                    if os.path.isfile("imports/" + i[1:-1]):
                        validCars.append(i[1:-1])
                        print(i[1:-1] + " found")
                    else:
                        print("'" + i[1:-1] + "' does not exist in imports folder")
                        inValidCars += 1
                
            openedList.close()
            print("\n" + str(len(validCars)) + " cars found")
            print(str(inValidCars) + " cars do not exist in imports folder")
            modifyMenu(validCars,True)

'''
Indexs for notes

Index 1

If you edit the rating via NRatings or in-game, you will see each rating is represented with integer min/max values
In the actual files ratings are represented with floats as mean (average) and deviation values
After minimal testing, I found a formula to convert between the min/max format and the mean/deviation format
'''
