import copy
import random
import math

f = open("words5000.txt", "r")
words = f.read().split("\n")
f.close()

#5x5
startingBlanks = [[1,3],[2,3],[4,1]]
#10x10
#startingBlanks = [[0,0],[0,2],[0,4],[0,9],[1,6],[1,8],[2,0],[2,2],[2,4],[3,6],[3,8],[4,0],[4,2],[5,7],[5,9],[6,1],[6,3],[6,4],[7,5],[7,7],[7,9],[8,1],[8,3],[9,0],[9,5],[9,7],[9,9]]
#15x15
#startingBlanks = [[0,5],[0,9],[0,10],[1,5],[1,9],[2,5],[2,9],[3,7],[4,0],[4,1],[4,2],[4,6],[4,11],[4,12],[4,13],[4,14],[5,3],[5,8],[6,4],[6,9],[7,4],[7,10],[8,5],[8,10],[9,6],[9,11],[10,0],[10,1],[10,2],[10,3],[10,8],[10,12],[10,13],[10,14],[11,7],[12,5],[12,9],[13,5],[13,9],[14,4],[14,5],[14,9]]

minimumWordsToValidate = 2

def letterToWordIndex(letter, letterPosition, wordLength):
    '''
    Return the index to the lookup table

            Parameters:
                    letter (char): A single letter
                    letterPosition (int): The position of the letter in the word where 0 is the first position
                    wordLength (int): The length of the word that the letter is from

            Returns:
                    (string): A string with the length of the original word where all letters are '_' except the input letter
    '''
    return '_'*letterPosition+letter+('_'*(wordLength-letterPosition-1))

def createWordLookupTable(wordList):
    '''
    Return a dictionary to find all words with a specific length and a letter at a specific position

            Parameters:
                    wordList (list(string)): A list of words

            Returns:
                    wordDictionary (dict of str: list(string)): A dictionary with letter indexes as keys and list of corresponds words as values
    '''
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
    '''
    Return the intersection of two lists

            Parameters:
                    lst1 (list(string)): A list of words
                    lst2 (list(string)): A list of words

            Returns:
                    lst3 (list(string)): The intersection of lst1 and lst 2
    '''
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def findWordInLookupTable(word):
    '''
    Return all possible words that can be formed from an incomplete word

            Parameters:
                    word (string): A incomplete word where unknown letters are filled with a space

            Returns:
                    validWordIntersection (list(string)): A list of words that can be formed from the incomplete word
    '''
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
    '''
    Returns complete word in the board

            Parameters:
                    board (list(list(list(char)))): A list of lists corresponding to corodinates with a list of available charaters inside
                    wordLengthLookupTable (list(list(list(int,int)))): A list of lists corresponding to matrix where each element is a list with two ints 
                                                                            corresponding to a corrdinate pair

            Returns:
                    chosenWords (list(list(string,int,int,int))): Returns all complete words on the board with their corrdinates and read direction
    '''
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
    '''
    Returns a bool corresponding

            Parameters:
                    x (int): The horizontal position of the word that is being checked
                    y (int): The vertical position of the word that is being checked
                    horizontal (bool)): True if the word is horizontal
                    vertical (bool): True if the word is vertical
                    chosenWords (list(list(string,int,int,int))): A list of the words that have already been chosen with the word, x position, y position 
                                                                    and direction. Where the third int indicate a vertical word if 0 and a horizontal word in case of a 1.

            Returns:
                    (bool): Return a bool representing if the word is found at the coordinate
    '''
    for chosenWord in chosenWords:
        if x == chosenWord[2] and y == chosenWord[1]:
            if horizontal == True and chosenWord[3] == 1:
                return True
            if vertical == True and chosenWord[3] == 0:
                return True
    return False

def Column(matrix, i):
    '''
    Returns a coloum of a matrix

            Parameters:
                    matrix (list(list(type))): A list of lists containing any type
                    i (int): The index of the coloum

            Returns:
                    (list(type)): Returns a list with the values from the coloum of the matrix
    '''
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
        if len(word) == wordLength and (not word in Column(chosenWords,0)):
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
    '''
    Removes options from a board which are not part of a valid solution

            Parameters:
                    board (list(list(list(char)))): A list of lists corresponding to corodinates with a list of available charaters inside
                    markedBoard (list(list(int))): A list of lists containing 0 if a cell should be propagated
                    wordLengthLookupTable (list(list(list(int,int)))): A list of lists corresponding to matrix where each element is a list with two ints 
                                                                            corresponding to a corrdinate pair

            Returns:
                    board (list(list(list(char)))): A list of lists corresponding to corodinates with a list of available charaters inside
    '''
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
    '''
    Finds the celll with the lowest entropy

            Parameters:
                    board (list(list(list(char)))): A list of lists corresponding to corodinates with a list of available charaters inside
                    weights (dict(char,float)): A dictionary with charaters as lookup and the corresponding entropy as the value

            Returns:
                    (list(int,int)): Returns a list with the corrdinate to the cell with the lowest entropy
    '''
    bestCell = [0,0]
    lowestEntropy = 2
    for row in range(0,len(board)):
        for col in range(0,len(board[row])):
            if WeightedEntropy(board[row][col], weights) > 0 and WeightedEntropy(board[row][col], weights) < lowestEntropy:
                lowestEntropy = WeightedEntropy(board[row][col], weights)
                bestCell = [row, col]
    return bestCell


def FindLowestEntropyNeighbour(board, weights):
    '''
    Finds the celll with the lowest entropy by considering neighbouring cells

            Parameters:
                    board (list(list(list(char)))): A list of lists corresponding to corodinates with a list of available charaters inside
                    weights (dict(char,float)): A dictionary with charaters as lookup and the corresponding entropy as the value

            Returns:
                    (list(int,int)): Returns a list with the corrdinate to the cell with the lowest entropy
    '''
    bestCell = [0,0]
    lowestEntropy = 2
    boardHeight = len(board)
    boardWidth = len(board[0])
    for row in range(0,len(board)):
        for col in range(0,len(board[row])):
            multiplier = 1
            if row-1 > 0 and SimpleEntropy(board[row-1][col], weights) == 0 and [row-1,col] not in startingBlanks:
                multiplier *= 1000
            if row+1 < boardHeight and SimpleEntropy(board[row+1][col], weights) == 0 and [row+2,col] not in startingBlanks:
                multiplier *= 1000
            if col-1 > 0 and SimpleEntropy(board[row][col-1], weights) == 0 and [row,col-1] not in startingBlanks:
                multiplier *= 1000
            if col+1 < boardWidth and SimpleEntropy(board[row][col+1], weights) == 0 and [row,col+2] not in startingBlanks:
                multiplier *= 1000
            if SimpleEntropy(board[row][col], weights) > 0 and SimpleEntropy(board[row][col], weights)/(multiplier) <= lowestEntropy:
                lowestEntropy = SimpleEntropy(board[row][col], weights)/(multiplier)
                bestCell = [row, col]
    return bestCell

def IsBoardValid(board, startingBlanks):
    '''
    Checks if the board is valid

            Parameters:
                    board (list(list(list(char)))): A list of lists corresponding to corodinates with a list of available charaters inside
                    startingBlanks (list(list(int,int))): A list of corrdinates

            Returns:
                    (bool): Returns a bool which is True if the board is valid and False if it is not valid
    '''
    for row in range(0,len(board)):
        for col in range(0,len(board[row])):
            if board[row][col] == [] and [row,col] not in startingBlanks:
                return False
    return True 

def Run(alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],
    boardWidth = 5, boardHeight = 5):
    '''
    Runs the algorithm

            Parameters:
                    alphabet (list(char)): List of the charaters in the used alphabet
                    boardWidth (int): The width of the board
                    boardHeight (int): The height of the board

            Returns:
                    board (list(list(list(char)))): A list of lists corresponding to corodinates with a list with one or no charater inside
    '''
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

        lowestEntropy = FindLowestEntropy(board, weights)
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
            
            lowestEntropy = FindLowestEntropy(board, weights)
            if not IsBoardValid(board,startingBlanks):
                break
            elif (WeightedEntropy(board[lowestEntropy[0]][lowestEntropy[1]],weights) == 0):
                break
        c = random.choice(board[lowestEntropy[0]][lowestEntropy[1]])
        board[lowestEntropy[0]][lowestEntropy[1]] = [c]
        markedBoard[lowestEntropy[0]][lowestEntropy[1]] = 0
        boardChoises.append([lowestEntropy[0],lowestEntropy[1],c])

    return board

#Runs the algorithm until a valid crossword is found
crossword = Run()
c = 0
while (not IsBoardValid(crossword, startingBlanks)):
    c += 1
    print(c)
    crossword = Run()
print(crossword)