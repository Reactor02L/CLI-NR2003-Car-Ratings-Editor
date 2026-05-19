'''
by Reactor02

17.05.2026 (End Date)

refer to readme.md for help on how to use
'''

import random, os, sys

# does the thing to modify the car

def modifyCar(carFile,modifyList):
    global modifyMin
    global modifyMax

    # opens the .car file as read, copies the data to a list, then closes the car file
    openedCar = open("imports/" + carFile, "br")
    carData = openedCar.readlines()
    openedCar.close()

    # copying the data I want to modify to a seperate list
    importList = []
    for i in range(2,17):
        importList.append([carData[i][-10:-2],carData[i+17][-10:-2]])

    # taking bytes and converting them into the integer min/max format
    for i in range(15):
        for n in range(2):
            importList[i][n] = float(importList[i][n].decode("utf-8")) # this converts the byte data into a string and then a float
        # converting the float into the integer min/max format
        # see index 1 at the bottom
        tempMean = importList[i][1] * 50
        tempDev = [i][0] * 100
        importList[i][1] = int(tempMean + tempDev)
        importList[i][0] = int(tempMean - tempDev)

    # I know it is inefficient to do this in a seperate loop, but it was slightly easier to code/debug it this way
    # changing the min/max values
    consentList = ['0','1','2','3','4','5','6','7','8','9','A','a','B','b','C','c','D','d','E','e']
    for i in range(len(modifyList)):
        if modifyList[i] in consentList:
            match modifyMin[0]:
                case 0: # no change
                    pass
                case 1: # set
                    importList[i][0] = modifyMin[1]
                case 2: # increment
                    importList[i][0] += modifyMin[1]
                case 3: # random
                    importList[i][0] = random.randint(modifyMin[1]-1,modifyMin[2])
            match modifyMax[0]:
                case 0: # no change
                    pass
                case 1: # set
                    importList[i][1] = modifyMax[1]
                case 2: # increment
                    importList[i][1] += modifyMax[1]
                case 3: # random
                    importList[i][1] = random.randint(modifyMax[1]-1,modifyMax[2])
        importList[i].sort()

    # converting the min/max back into bytes
    for i in range(15):
        # converting to mean/dev
        tempMean = (importList[i][0] + importList[i][1]) * 0.5
        tempDev = importList[i][1] - tempMean
        importList[i][0] = tempDev * 0.01
        importList[i][1] = tempMean * 0.02

        # converting the mean/dev into bytes
        for n in range(2):
            # turns the float into string length 8
            importList[i][n] = str(importList[i][n])
            while len(importList[i][n]) != 8:
                if len(importList[i][n]) > 8:
                    tempStr = ""
                    for x in range(8):
                        tempStr = tempStr + importList[i][n][x]
                    importList[i][n] = tempStr
                else:
                    importList[i][n] = importList[i][n] + "0"

            # adding extra bits to the string for formatting
            importList[i][n] = carData[i+2][0:-11].decode("utf-8") + importList[i][n] + "\r\n" # yes, the \r is necessary because the .car files are Windows files and we are directly editing the byte data
            # turns the string into bytes
            importList[i][n] = importList[i][n].encode("utf-8")

    # re-adding bytes to the carData list
    for i in range(15):
        carData[i+2] = importList[i][0]
        carData[i+19] = importList[i][1]

    # finally writing to the file
    openedCar = open("imports/" + carFile, "bw") # re-opening the .car file as write
    openedCar.writelines(carData)
    openedCar.close()

    print("Succesfully edited " + carFile)


# used to determine what ratings the user wants to modify and how

def modifyMenu(carFile,bulk=False):
    global modifyMin
    global modifyMax

    print("\nWhat would you like to modify?\n\nDriver -\n0: Agression\n1: Consistency\n2: Finishing\n3: Qualifying\n4: Road Course\n5: Short Track\n6: Speedway\n7: Superspeedway\n\nPitcrew -\n8: Consistency\n9: Speed\nA: Strategy\n\nVehicle -\nB: Aero\nC: Chassis\nD: Engine\nE: Reliability\n")

# forcing a valid input

    tempInput = "NO"
    while testTempInput(tempInput):
        tempInput = str(input())

# cleaning up the input
    
    modifyList = []
    for i in tempInput:
        modifyList.append(i)
    modifyList = list(set(modifyList))
    modifyList.sort()

# asking what modifications are wanted
    
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
            modifyCar(i,modifyList)
    else:
        modifyCar(carFile,modifyList)


# used to verify and return a value for tempInput in modifyMenu

def testTempInput(tempInput):
    if len(tempInput) == 0 or len(tempInput) > 15:
        return True

# returns True if a character is not a digit and not in the first 5 letters of the alphabet
    
    tempList = ["A","B","C","D","E","a","b","c","d","e"]
    for i in tempInput:
        if not i.isdigit() and not i in tempList:
            return  True
    return False

# asks for a Y/n question and returns T/F

def yesNo(text):
    answer = 1
    while answer != "y" and answer != "Y" and answer != "N" and answer != "n":
        answer = str(input(text + " (y/n): "))
    if answer == "y" or answer == "Y":
        return True
    else:
        return False

# for determining what modification to a rating is wanted

def threeChoice(text):
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

    print("\nWhen asked for file names, do include file extensions like gns.car and .lst\n\nWhat would you like to do?\n\n0: Exit\n1: Modify one car\n2: Bulk Modify\n")

    tempInput = 6
    while tempInput > 2 or tempInput < 0:
        tempInput = int(input())

    match tempInput:
        case 0:
            print("\nExiting program")
            sys.exit()
        case 1:
            # asks user for input file then executes program

            carFile = str(input("\nName of the car file: "))

            while not os.path.isfile("imports/" + carFile):
                print("\n" + carFile + " does not exist in the imports folder")
                carFile = str(input("Name of the car file: "))

            modifyMenu(carFile)
        case 2:

            # asks user for input file then gets a list of all valid cars in that list

            listName = str(input("\nName of the list file: "))

            while not os.path.isfile("imports/" + listName):
                print("\n" + listName + " does not exist in the imports folder")
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
                        print(i[1:-1] + " does not exist in imports folder")
                        inValidCars += 1
                
            openedList.close()
            print("\n" + str(len(validCars)) + " cars found")
            print(str(inValidCars) + " cars do not exist in imports folder")
            modifyMenu(validCars,True)

'''
Indexs for notes

Index 1

If you edit the rating via NRatings or in-game, you will see each rating is represented with integer min/max values
In the actual files ratings are represented with floats and mean (average) and deviation values
After minimal testing, I found a formula to convert between the min/max format and the mean/deviation format
'''
