import numpy as np
import copy
import random

f = open("words5000.txt", "r")
words = f.read().split("\n")
f.close()

print(len(words))

#startingBlanks = [[1,3],[2,3],[4,1]]
startingBlanks = [[1,1],[1,3],[3,1],[3,3]]
minimumWordsToValidate = 2

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

def SimpleEntropy(letterList):
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
    entropy = (len(letterList)-1)/25
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
        entropy+=weights[letter]
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
            if wordLengthLookupTable[row][col][0] >= minimumWordsToValidate:
                word = ""
                valid = True
                for i in range(0,wordLengthLookupTable[row][col][0]):
                    if len(board[row+i][col]) == 1:
                        word += board[row+i][col][0]
                    else:
                        valid = False
                if valid and word in words and word not in plainChosenWords:
                    chosenWords.append([word,row,col,0])
                    plainChosenWords.append(word)
            if wordLengthLookupTable[row][col][1] >= minimumWordsToValidate:
                word = ""
                valid = True
                for i in range(0,wordLengthLookupTable[row][col][1]):
                    if len(board[row][col+i]) == 1:
                        word += board[row][col+i][0]
                    else:
                        valid = False
                if valid and word in words and word not in plainChosenWords:
                    chosenWords.append([word,row,col,1])
                    plainChosenWords.append(word)
    return chosenWords

def IsWordAlreadyChosen(x,y,xMultiplier,yMultiplier,chosenWords):
    for chosenWord in chosenWords:
        if x == chosenWord[2] and y == chosenWord[1]:
            if xMultiplier == 1 and chosenWord[3] == 1:
                return True
            if yMultiplier == 1 and chosenWord[3] == 0:
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
    if wordLength < minimumWordsToValidate or IsWordAlreadyChosen(x-xoffset,y-yoffset,xMultiplier,yMultiplier,chosenWords):
        for i in range(0,wordLength):
            validLetters[i] = board[yMultiplier*(i-yoffset)+y][xMultiplier*(i-xoffset)+x]
        return validLetters

    for word in words:
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
                    chosenWords = FindChosenWords(board, wordLengthLookupTable)
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
                        validLetters = FindValidLetters(board, g, e, yLength, yoffset, 0, 0, chosenWords)
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
                        validLetters = FindValidLetters(board, g, e, 0, 0, xLength, xoffset, [])
                        #Replace letters in board with valid letters and mark the changed let
                        for i in range(0,len(validLetters)):
                            #Mark cell if letters are changed
                            if sorted(validLetters[i]) != board[e][g+i-xoffset]:
                                markedBoard[e][g+i-xoffset] = 0
                            board[e][g+i-xoffset] = copy.deepcopy(sorted(validLetters[i]))
    return board

def FindLowestEntropy(board, weights):
    bestCell = [0,0]
    lowestEntropy = 2
    for row in range(0,len(board)):
        for col in range(0,len(board[row])):
            if WeightedEntropy(board[row][col], weights) > 0 and WeightedEntropy(board[row][col], weights) < lowestEntropy:
                lowestEntropy = WeightedEntropy(board[row][col], weights)
                bestCell = [row, col]
    return bestCell

def IsBoardValid(board, startingBlanks):
    for row in range(0,len(board)):
        for col in range(0,len(board[row])):
            if board[row][col] == [] and [row,col] not in startingBlanks:
                return False
    return True 

def Run():
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    boardWidth = 5
    boardHeight = 5
    board = createBoard(boardHeight,boardWidth)
    board = Fillboard(board, alphabet)
    wordLengthLookupTable = CreatewordLengthLookupTable(boardHeight, boardWidth, board)

    weights = Weights(words, alphabet)

    savedBoards = []
    boardChoises = []
    boardSaveIndex = -1

    while True:
        markedBoard = createBoard(boardHeight,boardWidth)
        board = Propagate(board, markedBoard, wordLengthLookupTable)
        print(board)
        #Saves previous boards for backtracking
        boardSaveIndex += 1
        savedBoards.append(copy.deepcopy(board))

        lowestEntropy = FindLowestEntropy(board, weights)
        if WeightedEntropy(board[lowestEntropy[0]][lowestEntropy[1]],weights) == 0:
            #Propagate one last time to check if the crossword is valid
            markedBoard = createBoard(boardHeight,boardWidth)
            board = Propagate(board, markedBoard, wordLengthLookupTable)
            
            if board[0][0] != []:
                break

            while not IsBoardValid(board,startingBlanks) and boardSaveIndex != 0:
                savedBoards.pop(boardSaveIndex)
                boardSaveIndex -= 1
                board = copy.deepcopy(savedBoards[boardSaveIndex])
                lastBoardChoise = boardChoises.pop(boardSaveIndex)
                board[lastBoardChoise[0]][lastBoardChoise[1]].remove(lastBoardChoise[2])
                savedBoards[boardSaveIndex] = copy.deepcopy(board)
            
            if not IsBoardValid(board,startingBlanks):
                break
            lowestEntropy = FindLowestEntropy(board, weights)
        c = random.choice(board[lowestEntropy[0]][lowestEntropy[1]])
        board[lowestEntropy[0]][lowestEntropy[1]] = [c]
        markedBoard[lowestEntropy[0]][lowestEntropy[1]] = 0
        boardChoises.append([lowestEntropy[0],lowestEntropy[1],c])

    return board


crossword = Run()
c = 0
while (not IsBoardValid(crossword, startingBlanks)):
    c += 1
    print(c)
    crossword = Run()
print(crossword)
