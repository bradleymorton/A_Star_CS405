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

startChar    = 'S'
endChar      = 'E'
wallChar     = '#'
pathChar     = ' '
exploredChar = '+'

class Node:
    def __init__(self, row, col, value):
        self.value = value     # Character in corresponding map of maze
        self.row = row         # X-position of node 
        self.col = col         # Y-position of node 
        self.gscore = math.inf # Cost from start to current node
        self.fscore = math.inf # Estimated cost from start to end through current node
        self.cameFrom = Node   # Previous node used in path reconstruction

    def isNotWall(self):
        return (self.value != wallChar) # Double negative! Ah! Scary!

    def getNeighbors(self, nodeArray):
        neighbors = []

        # Check node above current node
        if self.row != 0:
            nodeAbove = nodeArray[self.row - 1][self.col]
            if nodeAbove.isNotWall():
                neighbors.append(nodeAbove)

        # Check node below current node
        if self.row != len(nodeArray) - 1:
            nodeBelow = nodeArray[self.row + 1][self.col]
            if nodeBelow.isNotWall():
                neighbors.append(nodeBelow)

        # Check node to the left of current node
        if self.col != 0:
            nodeToTheLeft = nodeArray[self.row][self.col - 1]
            if nodeToTheLeft.isNotWall():
                neighbors.append(nodeToTheLeft)

        # Check node to the right of current node
        if self.col != len(nodeArray[0]) - 1:
            nodeToTheRight = nodeArray[self.row][self.col + 1]
            if nodeToTheRight.isNotWall():
                neighbors.append(nodeToTheRight)

        return neighbors

    # Back-track through maze after shortest path has been found
    def reconstructPath(self, mazeString):
        if self.value != startChar:

            # Replace the character with "pathChar"
            mazeString[self.row][self.col] = pathChar

            # Recursively follow path backwards
            self.cameFrom.reconstructPath(mazeString)


class Agent:
    def __init__(self, mazeIndex):
        self.mazeIndex = mazeIndex  # maze1, maze2, etc.

        # String of the char's of the maze
        self.mazeString = getMazeString(self.mazeIndex)
        self.openList = []          # Unexplored nodes
        self.closedList = []        # Explored nodes
        self.solveableMaze = False  # If the current maze is solveable

    def sense(self):
        # Build array to store nodes in
        self.nodeArray = makeNodeArray(self.mazeIndex)

        # Find start node
        self.startNode = locateStart(self.nodeArray)
        self.startNode.gscore = 0
        self.openList.append(self.startNode)

        # Find end node
        self.endNode = locateEnd(self.nodeArray)

        # After reading the maze, find the path
        self.think()
    
    def think(self):
        exploredNodes = 0

        while self.openList:

            # Grab the next node from the unexplored nodes
            currentNode = self.openList[0]

            # Set current ndoe to the node with the lowest fscore
            for eachNode in self.openList:
                if eachNode.fscore < currentNode.fscore:
                    currentNode = eachNode

            # Replace character in maze string with exploredChar
            if currentNode.value != startChar and currentNode.value != endChar:
                self.mazeString[currentNode.row][currentNode.col] = exploredChar

            exploredNodes += 1

            # Check if the end of the maze has been reached
            if currentNode.value == endChar:
                self.solveableMaze = True
                break

            # Move current node to explored nodes list
            self.openList.remove(currentNode)
            self.closedList.append(currentNode)

            # Get neighbors of current node
            neighbors = currentNode.getNeighbors(self.nodeArray)

            # Iterate through each of the neighbors
            for child in neighbors:
                # If the neighbor has already been explored
                if child in self.closedList:
                    continue
                
                # Find distance if the neighbor were to be moved to
                tentative_gscore = currentNode.gscore + 1 #This could be something other than 1 if moves are weighted

                # Make neighbors available for exploration
                if child not in self.openList:
                    self.openList.append(child)

                # If there's a shorter path to get to the neighbor
                elif tentative_gscore >= child.gscore:
                    continue
                
                # Update gscore and fscore for the neighbor
                child.cameFrom = currentNode
                child.gscore = tentative_gscore
                child.fscore = child.gscore + self.heuristicEstimate(child)
        
        # Once maze has been explored, take action (output to file)
        #   Either a path has been found or maze has been declared unsolveable
        self.action()

    def action(self):
        textFile = open("./MazeResult" + str(self.mazeIndex) + ".txt",'w')
        tempStr = ""

        if self.solveableMaze:
            # Back-track to get the shortest path
            self.endNode.cameFrom.reconstructPath(self.mazeString)

            # Concatenate mazeString into one string rather than a list of chars
            for charList in self.mazeString:
                tempStr += "".join(charList)
                tempStr += "\n"

        else:
            tempStr = "NO SOLUTION! IMPOSSIBLE!"

        textFile.write(tempStr)
        textFile.close()        

    # virtual Heuristic
    def heuristicEstimate(self, fromNode):
        return 0

   
class ManhatAgent(Agent):
    # Manhattan Heuristic
    def heuristicEstimate(self, fromNode):
        return abs(fromNode.row - self.endNode.row) + abs(fromNode.col - self.endNode.col)

class EuclidAgent(Agent):
    # Euclidean Heuristic
    def heuristicEstimate(self, fromNode):
        return math.sqrt((fromNode.row - self.endNode.row)**2 + (fromNode.col - self.endNode.col)**2)

def getMazeString(num):
    tempStr = []
    #Read the file's content
    tempMap = open("./maze" + str(num) + ".txt", "r").readlines()
    
    #Loop through all the lines of the file's content
    for line in range(0, len(tempMap)):
        tempMap[line] = tempMap[line].replace("\n", "")
        tempStr.append(list(tempMap[line]))

    #Loop through all the numbers in each line of the file's content
    for line in range(0, len(tempStr)):
        for case in range(0, len(tempStr[line])):
            tempStr[line][case] = tempStr[line][case]

    #Store the information inside the "map" proprety of file_infos
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
            nodeArray[line].append(Node(line,case,tempStr[line][case]))
    
    #Return the node array
    return nodeArray

def locateStart(nodeArray):
    #Loop through all the lines of the "map"
    for line in range(0, len(nodeArray)):

        #Loop through all the numbers of each line of the "map"
        for case in range(0, len(nodeArray[line])):

            #If the current case is the START position
            if nodeArray[line][case].value == startChar:
                
                #Save the X and Y coordinates of the START position
                return nodeArray[line][case]

def locateEnd(nodeArray):

    #Loop through all the lines of the "map"
    for line in range(0, len(nodeArray)):

        #Loop through all the numbers of each line of the "map"
        for case in range(0, len(nodeArray[line])):

            #If the current case is the START position
            if nodeArray[line][case].value == endChar:

                #Save the X and Y coordinates of the START position
                return nodeArray[line][case]

# Our main from which we call all of our functions
# uncomment and run each agent then move output txt file to appropriate folder
def main():

    #Repeat for all 7 files
    for each_file in range(1,8):
        
#        agent = Agent(each_file)
#        agent.sense()
#       
#        manhatAgent = ManhatAgent(each_file)
#        manhatAgent.sense()
#        
        euclidAgent = EuclidAgent(each_file)
        euclidAgent.sense()
       

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
