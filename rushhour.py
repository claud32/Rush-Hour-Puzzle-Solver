import copy

# 1) The function’s purpose is to initial the rush hour solver
# 2) Expected Arguments are: a interger and a list of strings of starting configuration
# 3) The function returns the print of solving a rushhour puzzle
def rushhour(heuristicChoice, startNode):
    unexploredNodes = [startNode]
    path = []
    totalExplored = 0
    gn = 0
    return aStar(heuristicChoice, unexploredNodes, path, totalExplored, gn)


# 1) The function’s purpose is to start the recursive A* search
# 2) Expected Arguments are: a interger, a list of string, the path visited, a counter for states, a value for g(n)
# 3) The function returns the print of solving a rushhour puzzle
def aStar(heuristicChoice, unexploredNodes, path, totalExplored, gn):
    # print("Total moves:",len(path))
    # print("Total states explored:",totalExplored)
    # for i in path:
    #     print("\n")
    #     for j in i:
    #         print(j,end='\n')
    # print(unexploredNodes)

    if unexploredNodes == []:
        print("Fail to find solution")
        return []
        
    path.append(unexploredNodes[0])
    
    if (unexploredNodes[0][2][4] == "X" and unexploredNodes[0][2][5] == "X"):
        for i in path:
            print("\n")
            for j in i:
                print(j,end='\n')
        print("Total moves:",len(path)-1)
        print("Total states explored:",totalExplored)
        goal = path
        return goal
    
    else: 
        newNodes = generateNewNodes(unexploredNodes[0],path)
        unexploredNodes.extend(newNodes)
        totalExplored += len(newNodes)

        if heuristicChoice == 0:
            ascendingList1 = blockingHeuristic(newNodes,gn)
            ascendingList2 = blockingHeuristic(unexploredNodes,gn)
            res = aStar(0, ascendingList1, path, totalExplored, gn+1)
            if res != []:
                return res
            else:
                res = aStar(0, tail(ascendingList2), path, totalExplored, gn+1)
                if res != []:
                    return res

        elif heuristicChoice == 1:
            ascendingList = distancePlusBlockingHeuristic(newNodes,gn)
            res = aStar(1, ascendingList, path, totalExplored, gn+1)
            if res != []:
                return res
            else:
                res = aStar(1, tail(unexploredNodes), path, totalExplored, gn+1)
                if res != []:
                    return res

# 1) The function’s purpose is to get the first element of a list
# 2) Expected Arguments are: a list 
# 3) The function returns the first element of a list
def head(lst):
    return lst[0]

# 1) The function’s purpose is to get elements of a list except for the first element
# 2) Expected Arguments are: a list 
# 3) The function returns the elements of a list except for the first element
def tail(lst):
    return lst[1:]

# 1) The function’s purpose is to generateNewStates from a currentState
# 2) Expected Arguments are: a list of string
# 3) The function returns a list of lists of strings
def generateNewNodes(currentNode,path):
    empty = '-'
    checkedAlphabet = []
    newNodes = []
    typeList = []
    for row in currentNode:
        for carAlphabet in row:
            if carAlphabet != empty and carAlphabet not in checkedAlphabet:
                typeList.append(vehicleType(currentNode,carAlphabet))
                checkedAlphabet.append(carAlphabet)


    for k in range(len(checkedAlphabet)):
       if typeList[k] == 'HC' or 'HT':
           newNode = moveLeft(currentNode,path,checkedAlphabet[k],typeList[k])
           if newNode != []:
               newNodes.append(newNode)
           newNode = moveRight(currentNode,path,checkedAlphabet[k],typeList[k])        
           if newNode != []:
               newNodes.append(newNode)

       if typeList[k] == 'VC' or 'VT':
           newNode = moveUp(currentNode,path,checkedAlphabet[k],typeList[k])
           if newNode != []:
               newNodes.append(newNode)
           newNode = moveDown(currentNode,path,checkedAlphabet[k],typeList[k])
           if newNode != []:
               newNodes.append(newNode)

    return newNodes


# 1) The function’s purpose is to detemined the vehicle type
# 2) Expected Arguments are: a list of string, a char represent the vehicle
# 3) The function returns strings HC(horizontal car), HT(horizontal truck), etc
def vehicleType(currentNode,carAlphabet):
    hCount = 0
    vCount = 0
    vCountList = []
    if carAlphabet == 'X': 
        return 'HC' # Horizontal Car

    else:
        for row in currentNode:
            hCount = max(hCount,row.count(carAlphabet))
            vCountList.append(row.count(carAlphabet))
        vCount = vCountList.count(1)
        if hCount == 2:
            return 'HC'
        if hCount == 3:
            return 'HT' # Horizontal Truck
        if vCount == 2:
            return 'VC' # Vertical Car
        if vCount == 3:
            return 'VT' # Vertical Truck


# 1) The function’s purpose is to move a vehicle to the left to get a new state
# 2) Expected Arguments are: a list of string, a char represent the vehicle, the type of the vehicle
# 3) The function returns a node of strings
def moveLeft(currentNode,path,carAlphabet,typeOfVehicle):
    if typeOfVehicle == 'HC':
        result = findStartIndex(currentNode,carAlphabet)
        y = result[0]
        x = result[1]
        newNode = []
        if x != 0 and currentNode[y][x-1] == '-':
            for string in currentNode:
                new_string = string.replace("".join(['-',carAlphabet, carAlphabet]),
                "".join([carAlphabet, carAlphabet,'-']))
                newNode.append(new_string)
            if newNode not in path:
                return newNode
            else:
                return []
        else:
            return []
    
    elif typeOfVehicle == 'HT':
        result = findStartIndex(currentNode,carAlphabet)
        y = result[0]
        x = result[1]
        newNode = []
        if x != 0 and currentNode[y][x-1] == '-':
            for string in currentNode:
                new_string = string.replace("".join(['-',carAlphabet, carAlphabet,carAlphabet]),
                "".join([carAlphabet,carAlphabet, carAlphabet,'-']))
                newNode.append(new_string)
            if newNode not in path:
                return newNode
            else:
                return []
        else:
            return []
    
    else:
        return []

# 1) The function’s purpose is to move a vehicle to the right to get a new state
# 2) Expected Arguments are: a list of string, a char represent the vehicle, the type of the vehicle
# 3) The function returns a node of strings
def moveRight(currentNode,path,carAlphabet,typeOfVehicle):
    if typeOfVehicle == 'HC':
        result = findStartIndex(currentNode,carAlphabet)
        y = result[0]
        x = result[1]
        newNode = []
        if x < 4 and currentNode[y][x+2] == '-':
            for string in currentNode:
                new_string = string.replace("".join([carAlphabet, carAlphabet,'-']),
                "".join(['-',carAlphabet, carAlphabet]))
                newNode.append(new_string)
            if newNode not in path:
                return newNode
            else:
                return []
        else:
            return []
    
    elif typeOfVehicle == 'HT':
        result = findStartIndex(currentNode,carAlphabet)
        y = result[0]
        x = result[1]
        newNode = []
        if x < 3 and currentNode[y][x+3] == '-':
            for string in currentNode:
                new_string = string.replace("".join([carAlphabet, carAlphabet,carAlphabet,'-']),
                "".join(['-',carAlphabet, carAlphabet,carAlphabet]))
                newNode.append(new_string)
            if newNode not in path:
                return newNode
            else:
                return []
        else:
            return []
    
    else:
        return []

# 1) The function’s purpose is to convert a string to a list
# 2) Expected Arguments are: a string
# 3) The function returns a list of char
def convertToList(string):
    list1=[]
    list1[:0]=string
    return list1

# 1) The function’s purpose is to convert a list to a string
# 2) Expected Arguments are: a list of char
# 3) The function returns a string
def convertToString(l):
    str1 = ""
    for x in l:
        str1 += x 
    return str1


# 1) The function’s purpose is to move a vehicle to the up to get a new state
# 2) Expected Arguments are: a list of string, a char represent the vehicle, the type of the vehicle
# 3) The function returns a node of strings
def moveUp(currentNode,path,carAlphabet,typeOfVehicle):
    if typeOfVehicle == 'VC':
        result = findStartIndex(currentNode,carAlphabet)
        y = result[0]
        x = result[1]
        if y > 0 and currentNode[y-1][x] == '-':
            # print("up1")
            list2 = []
            newNode = []
            for i in range(6):
                list2.append(convertToList(currentNode[i]))
            list2[y-1][x] = carAlphabet
            list2[y+1][x] = '-'
            for j in range(6):
                newNode.append(convertToString(list2[j]))
            if newNode not in path:
                return newNode
            else:
                return []
        else:
            return []
            
    elif typeOfVehicle == 'VT':
        result = findStartIndex(currentNode,carAlphabet)
        y = result[0]
        x = result[1]
        if y > 0 and currentNode[y-1][x] == '-':
            # print("up2")
            list2 = []
            newNode = []
            for i in range(6):
                list2.append(convertToList(currentNode[i]))
            list2[y-1][x] = carAlphabet
            list2[y+2][x] = '-'
            for j in range(6):
                newNode.append(convertToString(list2[j]))
            if newNode not in path:
                return newNode
            else:
                return []
        else:
            return []
    
    else:
        return []


# 1) The function’s purpose is to move a vehicle down to get a new state
# 2) Expected Arguments are: a list of string, a char represent the vehicle, the type of the vehicle
# 3) The function returns a node of strings
def moveDown(currentNode,path,carAlphabet,typeOfVehicle):
    if typeOfVehicle == 'VC':
        result = findStartIndex(currentNode,carAlphabet)
        y = result[0]
        x = result[1]
        if y < 4 and currentNode[y+2][x] == '-':
            # print("d1")
            list2 = []
            newNode = []
            for i in range(6):
                list2.append(convertToList(currentNode[i]))
            list2[y][x] = '-'
            list2[y+2][x] = carAlphabet
            for j in range(6):
                newNode.append(convertToString(list2[j]))
            if newNode not in path:
                return newNode
            else:
                return []
        else:
            return []
            
    elif typeOfVehicle == 'VT':
        result = findStartIndex(currentNode,carAlphabet)
        y = result[0]
        x = result[1]
        if y < 3 and currentNode[y+3][x] == '-':
            list2 = []
            newNode = []
            for i in range(6):
                list2.append(convertToList(currentNode[i]))
            list2[y][x] = '-'
            list2[y+3][x] = carAlphabet
            for j in range(6):
                newNode.append(convertToString(list2[j]))
            if newNode not in path:
                return newNode
            else:
                return []
        else:
            return []
    else:
        return []

# 1) The function’s purpose is to get the first index of a vehicle 
# 2) Expected Arguments are: a list of string, a char represent the vehicle
# 3) The function returns a list first element is y second is x
def findStartIndex(currentNode,carAlphabet):
    if currentNode != []:
        # print("why is this?",currentNode)
        xList = []
        returnList = []
        x = 0
        for row in currentNode:
            xList.append(row.find(carAlphabet))
        for ele in xList:
            if ele != -1:
                x = ele                
        y = xList.index(x)
        returnList.append(y)
        returnList.append(x)
        # print("the cordinates",carAlphabet,returnList)
        return returnList
    else:
        return []

class Node:
 
   def __init__(self, state, heuristicValue):
      self.state = state
      self.heuristicValue = heuristicValue
    
   def __lt__(self, other):
       return self.heuristicValue < other.heuristicValue


# 1) The function’s purpose is to apply the blocking heuristic
# 2) Expected Arguments are: a list of lists of string, an int for g(n)
# 3) The function returns a list of states sorted by heuristic value in ascending order
def blockingHeuristic(unexploredNodes,gn):
    hn = 1
    nodeList = []
    acendStateList = [] 
    for node in unexploredNodes:
        result = findStartIndex(node,'X')
        x = result[1]
        if x < 4:
            for i in range(5-(x+1)):
                if node[2][5-i] != '-':
                    hn = hn + 1
        else:
            hn = 0
        fn = hn + gn
        myNode = Node(node,fn)
        nodeList.append(myNode)
    nodeList.sort()
    for ele in nodeList:
        acendStateList.append(ele.state)
    return acendStateList
    


# 1) The function’s purpose is to apply a heuristic that is distance from car X to the exit plus blocking heuritic.
# The reason for this is that it requires an extra state for Car X just to go on the next state, which less distance
# between car X and exit would possibly lead to less search
# 2) Expected Arguments are: a list of lists of string, an int for g(n)
# 3) The function returns a list of states sorted by heuristic value in ascending order
def distancePlusBlockingHeuristic(unexploredNodes,gn):
    # print("unexpo",unexploredNodes)
    hn = 1
    nodeList = []
    acendStateList = [] 
    for node in unexploredNodes:
        result = findStartIndex(node,'X')
        if result != []:
            x = result[1]
        if x < 4:
            for i in range(5-(x+1)):
                if node[2][5-i] != '-':
                    hn = hn + 1
            distance = 5 - (x + 1)
            hn = hn + distance
        else:
            hn = 0
        fn = hn + gn
        myNode = Node(node,fn)
        nodeList.append(myNode)
    nodeList.sort()
    for ele in nodeList:
        acendStateList.append(ele.state)
    return acendStateList


rushhour(1, ["--B---",
             "--B--E",
             "XXB--E",
             "CAA--D",
             "C----D",
             "FF---D"])

