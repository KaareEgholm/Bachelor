import numpy as np
import copy
import random
import math
import multiprocessing

f = open("words5000.txt", "r")
words = f.read().split("\n")
f.close()

print(len(words))

#5x5
#startingBlanks = [[1,3],[2,3],[4,1]]
#10x10
#startingBlanks = [[2,3],[4,0],[4,1],[4,2],[6,3]]
#startingBlanks = [[0,4],[0,8],[0,9],[1,4],[1,8],[2,3],[2,7],[3,4],[3,5],[4,0],[4,1],[4,2],[4,8],[5,4],[5,9],[6,3],[6,4],[6,5],[6,6],[7,4],[7,9],[8,4],[8,5],[8,9],[9,4],[9,5]]
#startingBlanks = [[0,6],[1,1],[1,2],[1,9],[2,6],[3,1],[3,7],[3,9],[4,3],[4,4],[4,5],[5,4],[5,5],[5,6],[6,0],[6,2],[6,8],[7,4],[8,0],[8,7],[8,8],[9,4]]
#startingBlanks = [[0,1],[0,6],[1,3],[2,5],[2,7],[3,2],[3,9],[4,6],[5,0],[5,4],[5,8],[6,2],[7,4],[7,7],[7,9],[8,2],[9,6]]
startingBlanks = [[0,0],[0,2],[0,4],[0,9],[1,6],[1,8],[2,0],[2,2],[2,4],[3,6],[3,8],[4,0],[4,2],[5,7],[5,9],[6,1],[6,3],[6,4],[7,5],[7,7],[7,9],[8,1],[8,3],[9,0],[9,5],[9,7],[9,9]]
#15x15
#startingBlanks = [[0,5],[0,9],[0,10],[1,5],[1,9],[2,5],[2,9],[3,7],[4,0],[4,1],[4,2],[4,6],[4,11],[4,12],[4,13],[4,14],[5,3],[5,8],[6,4],[6,9],[7,4],[7,10],[8,5],[8,10],[9,6],[9,11],[10,0],[10,1],[10,2],[10,3],[10,8],[10,12],[10,13],[10,14],[11,7],[12,5],[12,9],[13,5],[13,9],[14,4],[14,5],[14,9]]

startingBlanks = []
for i in range(0,190):
    while True:
        x = random.randrange(0,20)
        y = random.randrange(0,20)
        if [x,y] not in startingBlanks:
            startingBlanks.append([x,y])
            break


minimumWordsToValidate = 2

def letterToWordIndex(letter, letterPosition, wordLength):
    return '_'*letterPosition+letter+('_'*(wordLength-letterPosition-1))

def createWordLookupTable(wordList):
    wordDictionary = {}
    for word in wordList:
        for i in range(0,len(word)):
            index = letterToWordIndex(word[i], i, len(word))
            if index not in wordDictionary:
                wordDictionary[index] = []
            wordDictionary[index].append(word)
    return wordDictionary

wordLookupTable = createWordLookupTable(words)

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def findWordInLookupTable(word):
    validWordList = []
    for letterIndex in range(0, len(word)):
        if word[letterIndex] != " ":
            index = letterToWordIndex(word[letterIndex], letterIndex, len(word))
            if index not in wordLookupTable:
                return []
            validWordList.append(wordLookupTable[index])
    if validWordList == []:
        return []
    validWordIntersection = validWordList[0]
    for wordList in range(1,len(validWordList)):
        validWordIntersection = intersection(validWordIntersection,validWordList[wordList])
    return validWordIntersection

def createBoard(x, y):
    '''
    returns a list of lists with size x*y

            Parameters:
                    x (int): A whole number
                    y (int): Another whole number

            Returns:
                    binary_sum (list(list(0))): List of lists with size x*y
    '''
    board = []
    row = []
    for e in range(0, x):
        row += [0]
    for e in range(0, y):
        board += copy.deepcopy([row])
    return board

def SimpleEntropy(letterList, w):
    '''
    Calculates a linear entropy by dividing the length of the input list
        with the amount of letters in the alphabet

            Parameters:
                    letterList (list(T)): A list of elements

            Returns:
                    entropy (int): Int of the length of the list divided by the length of the alphabet
    '''
    if len(letterList) <= 1:
        return 0
    p = -1/25*math.log(1/25)
    entropy = len(letterList)*p
    return entropy


def Weights(words, alphabet):
    '''
    Calculates a weighted entropy lookup dictionary where the sum of all the letters are approximetly 1

            Parameters:
                    words (list(str)): A list of words
                    words (list(char)): A list of the charaters in the alphabet

            Returns:
                    Weights (dict(char,float)): A dictionary with charaters as lookup and the corresponding entropy as the value
    '''
    Weights = {}
    for letter in alphabet:
        Weights[letter] = 0
    letterCount = 0
    for word in words:
        for letter in word:
            if letter in alphabet:
                letterCount += 1
                Weights[letter.lower()] +=1
    for letter in Weights:
        Weights[letter] /= letterCount
    return Weights


def WeightedEntropy(letterList, weights):
    '''
    Calculates the entropy of a given list of charaters with a gien weighted entropy dictionary

            Parameters:
                    letterList (list(char)): A list of charaters
                    weights (dict(char,float)): A dictionary with charaters as lookup and the corresponding entropy as the value

            Returns:
                    entropy (int): The sum of entropys from the lookup dictionary corresponding with the letterList
    '''
    if len(letterList) <= 1:
        return 0
    entropy = 0
    for letter in letterList:
        entropy+=-weights[letter]*math.log(weights[letter])
    return entropy

def Fillboard(board, alphabet):
    '''
    Filles all cells of the given board with the given alphabet

            Parameters:
                    board (list(list(x)): A list inside a list where the content of that list is irrelevant
                    words (list(char)): A list of the charaters in the alphabet

            Returns:
                    board (list(list(list(char)))): The initial board filled with the alphabet in all cells
    '''
    for e in range(0,len(board)):
        for g in range(0,len(board[e])):
            board[e][g]= copy.deepcopy(alphabet)
    for blank in startingBlanks:
        board[blank[0]][blank[1]] = []
    return board

def IsCellFilled(x, y, board):
    '''
    Checks if a cell is filled

            Parameters:
                    x (int): A whole number
                    y (int): Another whole number
                    board (list(list(x))): A list inside a list where the content of that list is irrelevant

            Returns:
                    (bool): True if the cell is outside the board or is a blank cell
    '''
    if(x < 0 or y < 0 or board[x][y] == []):
        return True
    if (x > len(board) or y > len(board[x])):
        return True
    else:
        return False


def CreatewordLengthLookupTable(boardWidth, boardHeight, board):
    '''
    Creates a word length lookup table

            Parameters:
                    x (int): A whole number
                    y (int): Another whole number
                    board (list(list(x))): A list inside a list where the content of that list is irrelevant

            Returns:
                    wordLengthLookupTable (list(list(list(int,int)))): Creates a list of lists where the content is a list with two ints corresponding to the
                        y and x length of the words. The values in the lookup table is 0 if it is not the beginning of a word.
    '''
    wordLengthLookupTable = []
    for e in range(0,boardHeight):
        row = []
        for g in range(0,boardWidth):
            cell = []
            if(IsCellFilled(e-1,g,board)):
                counter = 0
                while e+counter < boardHeight and not IsCellFilled(e+counter,g,board):
                    counter+=1
                cell+=[counter]
            else:
                cell+=[0]
                
            if(IsCellFilled(e,g-1,board)):
                counter = 0
                while g+counter < boardWidth and not IsCellFilled(e,g+counter,board):
                    counter+=1
                cell+=[counter]
            else:
                cell+=[0]
            row+=[cell]
        wordLengthLookupTable+=[row]
    return wordLengthLookupTable



#Check if there are any marked cells
def PropagationFinished(markedBoard):
    '''
    Checks if propagation is done

            Parameters:
                    markedBoard (list(list(int))): A list of lists containing 0 if a cell should be propagated

            Returns:
                    (bool): Returns True in case no 0 is present in markedBoard
    '''
    for row in markedBoard:
        if 0 in row:
            return False
    return True

def FindChosenWords(board, wordLengthLookupTable):
    chosenWords = []
    plainChosenWords = []
    for row in range(0,len(board)):
        for col in range(0,len(board[row])):
            for direction in range(0,2):
                if wordLengthLookupTable[row][col][direction] >= minimumWordsToValidate:
                    word = ""
                    valid = True
                    for i in range(0,wordLengthLookupTable[row][col][direction]):
                        if len(board[row+(i*((direction+1)%2))][col+(i*((direction)%2))]) == 1:
                            word += board[row+(i*((direction+1)%2))][col+(i*((direction)%2))][0]
                        else:
                            valid = False
                    if valid and word in words and word not in plainChosenWords:
                        chosenWords.append([word,row,col,direction])
                        plainChosenWords.append(word)
    return chosenWords

def IsWordAlreadyChosen(x,y,horizontal,vertical,chosenWords):
    for chosenWord in chosenWords:
        if x == chosenWord[2] and y == chosenWord[1]:
            if horizontal == 1 and chosenWord[3] == 1:
                return True
            if vertical == 1 and chosenWord[3] == 0:
                return True
    return False

def column(matrix, i):
    return [row[i] for row in matrix]

def FindValidLetters(board, x, y, yLength, yoffset, xLength, xoffset, chosenWords):
    '''
    Creates a list of lists with the valid letters of a word

            Parameters:
                    board (list(list(list(char)))): A list of lists corresponding to corodinates with a list of available charaters inside
                    x (int): The horizontal position of the word that is being checked
                    y (int): The vertical position of the word that is being checked
                    yLength (int): The length of the vertical word. Is 0 if a horizontal word is being checked
                    yoffset (int): How far the beginning of the word is from the given y corrodinate
                    xLength (int): The length of the horizontal word. Is 0 if a vertical word is being checked
                    xoffset (int): How far the beginning of the word is from the given x corrodinate

            Returns:
                    validLetters (list(list(char))): A list corresponding to the cells of the checked word, with a list of valid charaters to place in that cell
    '''
    xMultiplier = 0
    yMultiplier = 0
    wordLength = 0

    if (yLength != 0):
        yMultiplier = 1
        wordLength = yLength
    
    if (xLength != 0):
        xMultiplier = 1
        wordLength = xLength

    validLetters = []
    for _ in range(0,wordLength):
        validLetters+=[[]]
    
    wordLetters = []
    for i in range(0,wordLength):
        wordLetters.append(board[yMultiplier*(i-yoffset)+y][xMultiplier*(i-xoffset)+x])
        
    if wordLength < minimumWordsToValidate or IsWordAlreadyChosen(x-xoffset,y-yoffset,xMultiplier,yMultiplier,chosenWords):
        return wordLetters

    lookupWord = ""
    for letterList in wordLetters:
        if len(letterList) == 1:
            lookupWord += letterList[0]
        else:
            lookupWord += " "
    
    lookupList = findWordInLookupTable(lookupWord)
    if lookupList == []:
        lookupList = words

    for word in lookupList:
        if len(word) == wordLength and (not word in column(chosenWords,0)):
            counter = 0
            valid = True
            for letter in word:
                if (letter not in board[yMultiplier*(counter-yoffset)+y][xMultiplier*(counter-xoffset)+x]):
                    valid = False
                counter+=1
            if valid:
                for letterIndex in range(0,len(word)):
                    if word[letterIndex] not in validLetters[letterIndex]:
                        validLetters[letterIndex] += copy.deepcopy([word[letterIndex]])
    return validLetters

def Propagate(board, markedBoard, wordLengthLookupTable):
    while not PropagationFinished(markedBoard):
        for e in range(0,len(markedBoard)):
            for g in range(0,len(markedBoard[e])):
                if (markedBoard[e][g] == 0):
                    #Unmark the cell
                    markedBoard[e][g] = 1
                    #Vertical propagation
                    #Check if the word begins on the cell and if it doesn't then offset until the beginning of the word is found
                    yoffset = 0
                    yLength = wordLengthLookupTable[e][g][0]
                    while yLength == 0:
                        yoffset+=1
                        yLength = wordLengthLookupTable[e-yoffset][g][0]
                    #Redundent check
                    if (yLength != 0):
                        #Creates a list to store the valid letters for the selected word
                        validLetters = FindValidLetters(board, g, e, yLength, yoffset, 0, 0, FindChosenWords(board, wordLengthLookupTable))
                        for i in range(0,len(validLetters)):
                            if sorted(validLetters[i]) != board[e+i-yoffset][g]:
                                markedBoard[e+i-yoffset][g] = 0
                            board[e+i-yoffset][g] = copy.deepcopy(sorted(validLetters[i]))
                    
                    #Horizontal propagation
                    #Check if the word begins on the cell and if it doesn't then offset until the beginning of the word is found
                    xoffset = 0
                    xLength = wordLengthLookupTable[e][g][1]
                    while yLength == 0:
                        xoffset+=1
                        xLength = wordLengthLookupTable[e][g-xoffset][1]
                    #Redundent check
                    if (xLength != 0):
                        #Creates a list to store the valid letters for the selected word
                        validLetters = FindValidLetters(board, g, e, 0, 0, xLength, xoffset, FindChosenWords(board, wordLengthLookupTable))
                        #Replace letters in board with valid letters and mark the changed let
                        for i in range(0,len(validLetters)):
                            #Mark cell if letters are changed
                            if sorted(validLetters[i]) != board[e][g+i-xoffset]:
                                markedBoard[e][g+i-xoffset] = 0
                            board[e][g+i-xoffset] = copy.deepcopy(sorted(validLetters[i]))
    return board

def FindLowestEntropy(board, weights):
    bestCell = []
    lowestEntropy = 2
    for row in range(0,len(board)):
        for col in range(0,len(board[row])):
            if WeightedEntropy(board[row][col], weights) > 0 and WeightedEntropy(board[row][col], weights) < lowestEntropy:
                lowestEntropy = WeightedEntropy(board[row][col], weights)
                bestCell.append([row, col])
    if bestCell == []:
        return [0,0]
    return bestCell


def FindLowestEntropyNeighbour(board, weights):
    bestCell = []
    lowestEntropy = 2
    boardHeight = len(board)
    boardWidth = len(board[0])
    for row in range(0,len(board)):
        for col in range(0,len(board[row])):
            multiplier = 1
            if row-1 > 0 and WeightedEntropy(board[row-1][col], weights) == 0 and [row-1,col] not in startingBlanks:
                multiplier *= 10
            if row+1 < boardHeight and WeightedEntropy(board[row+1][col], weights) == 0 and [row+2,col] not in startingBlanks:
                multiplier *= 10
            if col-1 > 0 and WeightedEntropy(board[row][col-1], weights) == 0 and [row,col-1] not in startingBlanks:
                multiplier *= 10
            if col+1 < boardWidth and WeightedEntropy(board[row][col+1], weights) == 0 and [row,col+2] not in startingBlanks:
                multiplier *= 10
            if WeightedEntropy(board[row][col], weights) > 0 and WeightedEntropy(board[row][col], weights)/(multiplier) <= lowestEntropy:
                lowestEntropy = WeightedEntropy(board[row][col], weights)/(multiplier)
                bestCell.append([row, col])
    if bestCell == []:
        return [0,0]
    return random.choice(bestCell)

def IsBoardValid(board, startingBlanks):
    for row in range(0,len(board)):
        for col in range(0,len(board[row])):
            if board[row][col] == [] and [row,col] not in startingBlanks:
                return False
    return True 

def Run(alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],
    boardWidth = 20, boardHeight = 20):
    
    board = createBoard(boardWidth,boardHeight)
    board = Fillboard(board, alphabet)
    wordLengthLookupTable = CreatewordLengthLookupTable(boardWidth, boardHeight, board)

    weights = Weights(words, alphabet)

    savedBoards = []
    boardChoises = []

    while True:
        markedBoard = createBoard(boardWidth, boardHeight)
        board = Propagate(board, markedBoard, wordLengthLookupTable)
        #Saves previous boards for backtracking
        savedBoards.append(copy.deepcopy(board))

        lowestEntropy = FindLowestEntropyNeighbour(board, weights)
        if WeightedEntropy(board[lowestEntropy[0]][lowestEntropy[1]],weights) == 0:
            if IsBoardValid(board,startingBlanks):
                break
            
            while not IsBoardValid(board,startingBlanks) and len(boardChoises) != 0:
                savedBoards.pop()
                lastBoardChoise = boardChoises.pop()
                savedBoards[-1][lastBoardChoise[0]][lastBoardChoise[1]].remove(lastBoardChoise[2])
                board = copy.deepcopy(savedBoards[-1])
                markedBoard = createBoard(boardWidth, boardHeight)
                board = Propagate(board, markedBoard, wordLengthLookupTable)
            
            lowestEntropy = FindLowestEntropyNeighbour(board, weights)
            if not IsBoardValid(board,startingBlanks):
                break
            elif (WeightedEntropy(board[lowestEntropy[0]][lowestEntropy[1]],weights) == 0):
                break
        c = random.choice(board[lowestEntropy[0]][lowestEntropy[1]])
        board[lowestEntropy[0]][lowestEntropy[1]] = [c]
        markedBoard[lowestEntropy[0]][lowestEntropy[1]] = 0
        boardChoises.append([lowestEntropy[0],lowestEntropy[1],c])

    print(board)
    return board

if __name__ == '__main__':
    while True:
        # Start bar as a process
        p = multiprocessing.Process(target=Run)
        p.start()

        # Wait for 10 seconds or until process finishes
        p.join(60)

        # If thread is still active
        if p.is_alive():
            print("running... let's kill it...")

            # Terminate - may not work if process is stuck for good
            p.kill()
            # OR Kill - will work for sure, no chance for process to finish nicely however
            # p.kill()

            p.join()


'''
crossword = Run()
c = 0
while (not IsBoardValid(crossword, startingBlanks)):
    c += 1
    print(c)
    crossword = Run()
print(crossword)
'''