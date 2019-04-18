#    _           __  __                 ____                      _     
#   / \  __/\__ |  \/  | __ _ _______  / ___|  ___  __ _ _ __ ___| |__  
#  / _ \ \    / | |\/| |/ _` |_  / _ \ \___ \ / _ \/ _` | '__/ __| '_ \ 
# / ___ \/_  _\ | |  | | (_| |/ /  __/  ___) |  __/ (_| | | | (__| | | |
#/_/   \_\ \/   |_|  |_|\__,_/___\___| |____/ \___|\__,_|_|  \___|_| |_|
#                                                                       
#Bradly Morton, George Meier, Andrew Adler
#Inputs     maze1.txt       0=Free_Space, 1=Wall, 2=Start, 3=End
#Outputs    MazeResult1.txt containing path string and step count || IMPOSSIBLE 
#change the name and number of the maze on lines 23 and 285
import math

class Node:
    def __init__(self, row, col, value):
        self.value = value
        self.row = row
        self.col = col
        self.gscore = math.inf
        self.fscore = math.inf
        self.cameFrom = Node

    def getNeighbors(self, nodeArray):
        neighbors = []
        if self.row != 0:
            neighbors.append(nodeArray[self.row - 1][self.col])

        if self.row != len(nodeArray) - 1:
            neighbors.append(nodeArray[self.row + 1][self.col])

        if self.col != 0:
            neighbors.append(nodeArray[self.row][self.col - 1])

        if self.col != len(nodeArray[0]) - 1:
            neighbors.append(nodeArray[self.row][self.col + 1])
        return neighbors


class Agent:
    def __init__(self):
        self.maze = readFiles(5)
        self.openList = []
        self.closedList = []
        self.cameFrom = []

    def sense(self):
        self.nodeArray = makeNodeArray(5)
        self.startNode = locateStart(self.nodeArray)
        self.startNode.gscore = 0
        self.endNode   = locateEnd(self.nodeArray)
        self.openList.append(self.startNode)

        self.think()
    
    def think(self):
        #print("start node:", self.startNode.row, self.startNode.col)
        while self.openList:
            currentNode = self.openList[0]
            for eachNode in self.openList:
                if eachNode.fscore < currentNode.fscore:
                    currentNode = eachNode
            
            print("current node: ",currentNode.row,currentNode.col)
            #print("current node fscore:",currentNode.fscore)
            if currentNode.value == 3:
                break

            self.openList.remove(currentNode)
            self.closedList.append(currentNode)

            neighbors = currentNode.getNeighbors(self.nodeArray)
            for child in neighbors:
                if child in self.closedList:
                    continue

                tentative_gscore = currentNode.gscore + 1 #This could be something other than 1 if moves are weighted

                if child not in self.openList:
                    self.openList.append(child)

                elif tentative_gscore >= child.gscore:
                    continue
                
                #print("child node: ",child.row,child.col)
                child.cameFrom = currentNode
                child.gscore = tentative_gscore
                child.fscore = child.gscore + self.heuristicEstimate(child)
                #print("child fscore:",child.fscore)

        print("end node at:",self.endNode.row,self.endNode.col)
        self.action()

    def action(self):
        '''action'''

    def heuristicEstimate(self, fromNode):
        #print (file_infos["ManX"][fromNode.row][fromNode.col])
        #return file_infos["ManX"][fromNode.row][fromNode.col]
        return abs(fromNode.row - self.endNode.row) + abs(fromNode.col + self.endNode.col)


#!/usr/local/bin/python3

#Initialisation of a dictionary to store the file's informations
file_infos = {"map": [], "startPos": {"x": "", "y": ""}, "endPos": {"x": "", "y": ""}, "Fx": [], "ManX": [], "aGx": [], "amountSteps": "", "reverseWinningPath": []}

#Function that takes the file'S content inside the "map" proprety of file_infos
def readFiles(num):
    tempStr = []
    tempInt = []
    #Read the file's content
    tempMap = open("./maze" + str(num) + ".txt", "r").readlines()

    #Loop through all the lines of the file's content
    for line in range(0, len(tempMap)):
        tempMap[line] = tempMap[line].replace("\n", "")
        tempStr.append(list(tempMap[line]))

    #Loop through all the numbers in each line of the file's content
    for line in range(0, len(tempStr)):
        for case in range(0, len(tempStr[line])):
            tempStr[line][case] = float(tempStr[line][case])

    #Store the information inside the "map" proprety of file_infos
    file_infos["map"] = tempStr
    return tempStr

def makeNodeArray(fileIndex):
    tempStr = []
    nodeArray = []
    #Read the file's content
    tempMap = open("./maze" + str(fileIndex) + ".txt", "r").readlines()

    #Loop through all the lines of the file's content
    for line in range(0, len(tempMap)):
        tempMap[line] = tempMap[line].replace("\n", "")
        tempStr.append(list(tempMap[line]))

    #Loop through all the numbers in each line of the file's content
    for line in range(0, len(tempStr)):
        nodeArray.append([])
        for case in range(0, len(tempStr[line])):

            # Make a node at each position with the right value
            nodeArray[line].append(Node(line,case,int(tempStr[line][case])))
    
    #Return the node array
    return nodeArray

#Function to locate both START and END positions from the "map"
def locateStartEnd():

    #Loop through all the lines of the "map"
    for line in range(0, len(file_infos["map"])):

        #Loop through all the numbers of each line of the "map"
        for case in range(0, len(file_infos["map"][line])):

            #If the current case is the START position
            if file_infos["map"][line][case] == 2:

                #Save the X and Y coordinates of the START position
                file_infos["startPos"]["x"] = case
                file_infos["startPos"]["y"] = line

            #If the current case of the END position
            if file_infos["map"][line][case] == 3:

                #Save the X and Y coordinates of the END position
                file_infos["endPos"]["x"] = case
                file_infos["endPos"]["y"] = line

def locateStart(nodeArray):

    #Loop through all the lines of the "map"
    for line in range(0, len(nodeArray)):

        #Loop through all the numbers of each line of the "map"
        for case in range(0, len(nodeArray[line])):

            #If the current case is the START position
            if nodeArray[line][case].value == 2:

                #Save the X and Y coordinates of the START position
                return nodeArray[line][case]

def locateEnd(nodeArray):

    #Loop through all the lines of the "map"
    for line in range(0, len(nodeArray)):

        #Loop through all the numbers of each line of the "map"
        for case in range(0, len(nodeArray[line])):

            #If the current case is the START position
            if nodeArray[line][case].value == 3:

                #Save the X and Y coordinates of the START position
                return nodeArray[line][case]

#Function that initializes the Manhattan map
def createManX():
    manhat = []

    #Loop through all the lines of the "map"
    for line in range(0, len(file_infos["map"])):
        row = []

        #Loop through all the numbers of each line of the "map"
        for case in range(0, len(file_infos["map"][line])):

            #Fill each case with |X1 - X2| + |Y1 - Y2|
            row.append((abs(case - file_infos["endPos"]["x"]) + abs(line - file_infos["endPos"]["y"])))
        manhat.append(row)

    #Store the Manhattan map in the "ManX" proprety of file_infos
    file_infos["ManX"] = manhat

#Function that initializes the Fx map
def createFx():
    Fx = []

    #Loop through all the lines of the "map"
    for line in range(0, len(file_infos["map"])):
        row = []

        #Loop through all the numbers of each line of the "map"
        for case in range(0, len(file_infos["map"][line])):

            #Insert -1 at the starting position coordinates in "Fx"
            if case == file_infos["startPos"]["x"] and line == file_infos["startPos"]["y"]:
                row.append(-1.0)

            #Insert FALSE everywhere else
            else: row.append(False)
        Fx.append(row)

    #Store the Fx map in the "Fx" proprety of the file_infos
    file_infos["Fx"] = Fx

#Function that initializes the aGx map
def createaGx(a):
    aGx = []

    #Loop through all the lines of the "map"
    for line in range(0, len(file_infos["map"])):
        row = []

        #Loop through all the numbers of each line of the "map"
        for case in range(0, len(file_infos["map"][line])):

            #Insert "alpha" * the value of "Fx" at the starting position in "aGx"
            if case == file_infos["startPos"]["x"] and line == file_infos["startPos"]["y"]:
                row.append(a * file_infos["ManX"][line][case])

            #Insert FALSE everywhere else
            else: row.append(False)
        aGx.append(row)

    #Store the aGx map in the "aGx" proprety of file_infos
    file_infos["aGx"] = aGx

#Function to go from the starting point, move around following our heuristic
def moveAround(a):
    steps = 0
    minimum = {"x": "", "y": "", "value": ""}
    isNumber = False

    #Check if the case to the left is a valid case
    def getLeft():
        if file_infos["map"][minimum["y"]][minimum["x"] - 1] != 1.0 and file_infos["aGx"][minimum["y"]][minimum["x"] - 1] == False:
            if file_infos["Fx"][minimum["y"]][minimum["x"]] == - 1:
                file_infos["Fx"][minimum["y"]][minimum["x"] - 1] = file_infos["Fx"][minimum["y"]][minimum["x"]] + 2
            else: file_infos["Fx"][minimum["y"]][minimum["x"] - 1] = file_infos["Fx"][minimum["y"]][minimum["x"]] + 1
            file_infos["aGx"][minimum["y"]][minimum["x"] - 1] = (a * file_infos["ManX"][minimum["y"]][minimum["x"] - 1]) + (file_infos["Fx"][minimum["y"]][minimum["x"] - 1])

    #Check if the case to the right is a valid case
    def getRight():
        if file_infos["map"][minimum["y"]][minimum["x"] + 1] != 1.0 and file_infos["aGx"][minimum["y"]][minimum["x"] + 1] == False:
            if file_infos["Fx"][minimum["y"]][minimum["x"]] == - 1:
                file_infos["Fx"][minimum["y"]][minimum["x"] + 1] = file_infos["Fx"][minimum["y"]][minimum["x"]] + 2
            else: file_infos["Fx"][minimum["y"]][minimum["x"] + 1] = file_infos["Fx"][minimum["y"]][minimum["x"]] + 1
            file_infos["aGx"][minimum["y"]][minimum["x"] + 1] = (a * file_infos["ManX"][minimum["y"]][minimum["x"] + 1]) + (file_infos["Fx"][minimum["y"]][minimum["x"] + 1])

    #Check if the case on top is a valid case
    def getUp():
        if file_infos["map"][minimum["y"] - 1][minimum["x"]] != 1.0 and file_infos["aGx"][minimum["y"] - 1][minimum["x"]] == False:
            if file_infos["Fx"][minimum["y"]][minimum["x"]] == - 1:
                file_infos["Fx"][minimum["y"] - 1][minimum["x"]] = file_infos["Fx"][minimum["y"]][minimum["x"]] + 2
            else: file_infos["Fx"][minimum["y"] - 1][minimum["x"]] = file_infos["Fx"][minimum["y"]][minimum["x"]] + 1
            file_infos["aGx"][minimum["y"] - 1][minimum["x"]] = (a * file_infos["ManX"][minimum["y"] - 1][minimum["x"]]) + (file_infos["Fx"][minimum["y"] - 1][minimum["x"]])

    #Check if the case on the bottom is a valid case
    def getDown():
        if file_infos["map"][minimum["y"] + 1][minimum["x"]] != 1.0 and file_infos["aGx"][minimum["y"] + 1][minimum["x"]] == False:
            if file_infos["Fx"][minimum["y"]][minimum["x"]] == - 1:
                file_infos["Fx"][minimum["y"] + 1][minimum["x"]] = file_infos["Fx"][minimum["y"]][minimum["x"]] + 2
            else: file_infos["Fx"][minimum["y"] + 1][minimum["x"]] = file_infos["Fx"][minimum["y"]][minimum["x"]] + 1
            file_infos["aGx"][minimum["y"] + 1][minimum["x"]] = (a * file_infos["ManX"][minimum["y"] + 1][minimum["x"]]) + (file_infos["Fx"][minimum["y"] + 1][minimum["x"]])

    #While we're not on the end position, keep going
    while not file_infos["aGx"][file_infos["endPos"]["y"]][file_infos["endPos"]["x"]]:

        minimum = {"x": "", "y": "", "value": ""}

        #Loop through all the lines of the "map"
        for line in range(0, len(file_infos["map"])):

            #Loop through all the numbers of each line of the "map"
            for case in range(0, len(file_infos["map"][line])):

                #Check if current case is a number
                if isinstance(file_infos["aGx"][line][case], float):

                    #If we don't already have a minimum value, take the first one we find
                    if minimum["value"] == "":
                        minimum.update({"x": case, "y": line, "value": file_infos["aGx"][line][case]})

                    #If we already have one, check if the value is smaller that our minimum
                    elif file_infos["aGx"][line][case] < minimum["value"]:

                        #If it is, make it our new minimum
                        minimum.update({"x": case, "y": line, "value": file_infos["aGx"][line][case]})

        #If we don't have a minimum, it means that we're stuck and the map is IMPOSSIBLE
        if minimum["value"] == "":
            file_infos["numberSteps"] = "IMPOSSIBLE"
            file_infos["reverseWinningPath"] = "IMPOSSIBLE"
            return
        steps += 1

        #If the current case is in the middle columns
        if 0 < minimum["x"] < len(file_infos["map"][0]) - 1:
            getLeft()
            getRight()

        #If the current case is in the first column
        elif minimum["x"] == 0:
            getRight()

        #Id the current case is on the last column
        else:
            getLeft()

        #If the current case is on the middle rows
        if 0 < minimum["y"] < len(file_infos["map"]) - 1:
            getUp()
            getDown()

        #If the current case is on the first row
        elif minimum["y"] == 0:
            getDown()

        #If the current case is on the last row
        else:
            getUp()

        #The case we were previously on, becomes TRUE
        file_infos["aGx"][minimum["y"]][minimum["x"]] = True

    #Store the amount of steps required to find the exit in the "numberSteps" proprety of file_infos
    file_infos["numberSteps"] = steps

#Function to go from the END to the START using the shortest path possible
def trackBack():
    currentPosition = {"x": file_infos["endPos"]["x"],"y": file_infos["endPos"]["y"],"value": file_infos["Fx"][file_infos["endPos"]["y"]][file_infos["endPos"]["x"]]}
    while True:

        #If current file is IMPOSSIBLE, stop here
        if currentPosition["value"] == - 1 or file_infos["numberSteps"] == "IMPOSSIBLE":
            break
        minimum = {"x": "", "y": "", "value": ""}

        #If current position is not on first row
        if currentPosition["y"] != 0 and file_infos["aGx"][currentPosition["y"] - 1][currentPosition["x"]]:

            #If we don't already have a minimum value, take the first one we see
            if minimum["value"] == "":
                minimum.update({"x": currentPosition["x"], "y": currentPosition["y"] - 1, "value": file_infos["Fx"][currentPosition["y"] - 1][currentPosition["x"]]})

            #If we already have one, check if the value is smaller that our minimum
            elif file_infos["Fx"][currentPosition["y"] - 1][currentPosition["x"]] < minimum["value"]:
                minimum.update({"x": currentPosition["x"], "y": currentPosition["y"] - 1, "value": file_infos["Fx"][currentPosition["y"] - 1][currentPosition["x"]]})

        #If current position is not on the first column
        if currentPosition["x"] != 0 and file_infos["aGx"][currentPosition["y"]][currentPosition["x"] - 1]:

            #If we don't already have a minimum value, take the first one we see
            if minimum["value"] == "":
                minimum.update({"x": currentPosition["x"] - 1, "y": currentPosition["y"], "value": file_infos["Fx"][currentPosition["y"]][currentPosition["x"] - 1]})

            #If we already have one, check if the value is smaller that our minimum
            elif file_infos["Fx"][currentPosition["y"]][currentPosition["x"] - 1] < minimum["value"]:
                minimum.update({"x": currentPosition["x"] - 1, "y": currentPosition["y"], "value": file_infos["Fx"][currentPosition["y"]][currentPosition["x"] - 1]})

        if currentPosition["x"] < (len(file_infos["map"][0]) - 1) and file_infos["aGx"][currentPosition["y"]][currentPosition["x"] + 1]:

            #If we don't already have a minimum value, take the first one we see
            if minimum["value"] == "":
                minimum.update({"x": currentPosition["x"] + 1, "y": currentPosition["y"], "value": file_infos["Fx"][currentPosition["y"]][currentPosition["x"] + 1]})

            #If we already have one, check if the value is smaller that our minimum
            elif file_infos["Fx"][currentPosition["y"]][currentPosition["x"] + 1] < minimum["value"]:
                minimum.update({"x": currentPosition["x"] + 1, "y": currentPosition["y"], "value": file_infos["Fx"][currentPosition["y"]][currentPosition["x"] + 1]})

        if currentPosition["y"] < (len(file_infos["map"]) - 1) and file_infos["aGx"][currentPosition["y"] + 1][currentPosition["x"]]:

            #If we don't already have a minimum value, take the first one we see
            if minimum["value"] == "":
                minimum.update({"x": currentPosition["x"], "y": currentPosition["y"] + 1, "value": file_infos["Fx"][currentPosition["y"] + 1][currentPosition["x"]]})

            #If we already have one, check if the value is smaller that our minimum
            elif file_infos["Fx"][currentPosition["y"] + 1][currentPosition["x"]] < minimum["value"]:
                minimum.update({"x": currentPosition["x"], "y": currentPosition["y"] + 1, "value": file_infos["Fx"][currentPosition["y"] + 1][currentPosition["x"]]})

        #Add the opposite direction to the "reverseWinningPath" proprety of file_infos
        if currentPosition["x"] < minimum["x"]: file_infos["reverseWinningPath"].append("W")
        elif currentPosition["x"] > minimum["x"]: file_infos["reverseWinningPath"].append("E")
        elif currentPosition["y"] > minimum["y"]: file_infos["reverseWinningPath"].append("S")
        else: file_infos["reverseWinningPath"].append("N")
        currentPosition = minimum

#Function to write the file containing the answer
def writeFile(num):
    textFile = open("./MazeResult" + str(3) + ".txt",'w')

    #If the file is IMPOSSIBLE to solve
    if file_infos["numberSteps"] == "IMPOSSIBLE":

        #Write "IMPOSSIBLE" in the file
        textFile.write(str(file_infos["reverseWinningPath"]))

    #If the file is solvable
    else:

        #Take the reverse of our "reverseWinningPath"
        file_infos["reverseWinningPath"].reverse()

        #Write it to the file
        textFile.write('Path: '+str(''.join(file_infos["reverseWinningPath"])))
        textFile.write(str("\n"))

        #Write the amount of steps to the file
        textFile.write('Steps: '+str(file_infos["numberSteps"]))
    textFile.close()

#Our main from which we call all of our functions
def main():

    #Repeat for all 9 files
    for each_file in range(1,4):
        global file_infos
        file_infos = {"map": [], "startPos": {"x": "", "y": ""}, "endPos": {"x": "", "y": ""}, "Fx": [], "ManX": [], "aGx": [], "amountSteps": "", "reverseWinningPath": []}

        #Assign the correct "alpha" based on the exercise
        if 1 <= each_file <=  6: a = 1.0
        elif 7 <= each_file <= 8: a = 0.5
        else: a = 5.0

        #Call each functions in the correct order
        readFiles(str(each_file))
        locateStartEnd()
        createManX()
        createFx()
        createaGx(a)
        moveAround(a)
        trackBack()
        writeFile(str(each_file))

    agent = Agent()
    agent.sense()

if __name__ == "__main__":
    main()
