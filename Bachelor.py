import numpy as np
import copy
import random

f = open("words10000.txt", "r")
words = f.read().split("\n")
f.close()

print(len(words))

#Fill a board with with empty lists
def createBoard(x, y):
    board = []
    row = []
    for e in range(0, y):
        row += [0]
    for e in range(0, x):
        board += copy.deepcopy([row])
    return board
    
#Takes a list of letters and returns a simple entropy from that
def SimpleEntropy(letterList):
    if len(letterList) <= 1:
        return 0
    return (len(letterList)-1)/25

#calculates the frequency of how used a letter is present in a list of words
def Weights(words):
    Weights = {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}
    letterCount = 0
    for word in words:
        for letter in word:
            if letter in alphabet:
                letterCount += 1
                Weights[letter.lower()] +=1
    for letter in Weights:
        Weights[letter] /= letterCount
    return Weights

#Takes a list of letters and returns a simple entropy from that
def WeightedEntropy(letterList, weights):
    entropy = 0
    for letter in letterList:
        entropy+=weights[letter]
    return entropy

#Fill a board with an alphabet
#TODO: Give the alphabet as an argument
def Fillboard(board):
    for e in range(0,len(board)):
        for g in range(0,len(board[e])):
            board[e][g]= copy.deepcopy(alphabet)
    return board

#Check if a cell in a board has any value
def IsCellFilled(x, y, board):
    if(x < 0 or y < 0 or board[x][y] == []):
        return True
    else:
        return False

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

boardWidth = 5
boardHeight = 5
board = createBoard(boardHeight,boardWidth)

board = Fillboard(board)

#Creates a word length lookup table
#TODO: Make to function and comment
wordLengthLookupTable = []
for e in range(0,boardHeight):
    row = []
    for g in range(0,boardWidth):
        cell = []
        if(IsCellFilled(e-1,g,board)):
            counter = 0
            while counter < boardHeight and not IsCellFilled(e+counter,g,board):
                counter+=1
            cell+=[counter]
        else:
            cell+=[0]
            
        if(IsCellFilled(e,g-1,board)):
            counter = 0
            while counter < boardWidth and not IsCellFilled(e,g+counter,board):
                counter+=1
            cell+=[counter]
        else:
            cell+=[0]
        row+=[cell]
    wordLengthLookupTable+=[row]

#Check if there are any marked cells
def PropagationFinished(markedBoard):
    for row in markedBoard:
        if 0 in row:
            return False
    return True

def Propagate(markedBoard):
    while not PropagationFinished(markedBoard):
        for e in range(0,len(markedBoard)):
            for g in range(0,len(markedBoard[e])):
                if (markedBoard[e][g] == 0):
                    #Check if the word begins on the cell and if it doesn't then offset until the beginning of the word is found
                    yoffset = 0
                    yLength = wordLengthLookupTable[e][g][0]
                    while yLength == 0:
                        yoffset+=1
                        yLength = wordLengthLookupTable[e-yoffset][g][0]
                    #Redundent check
                    if (yLength != 0):
                        #Creates a list to store the valid letters for the selected word
                        validLetters = []
                        for i in range(0,yLength):
                            validLetters+=[[]]
                        for word in words:
                            if (len(word) == yLength):
                                counter = 0
                                valid = True
                                for letter in word:
                                    if (letter not in board[e+counter-yoffset][g]):
                                        valid = False
                                    counter+=1
                                if (valid):
                                    for letterIndex in range(0,len(word)):
                                        if word[letterIndex] not in validLetters[letterIndex]:
                                            validLetters[letterIndex] += copy.deepcopy([word[letterIndex]])
                        for i in range(0,len(validLetters)):
                            if sorted(validLetters[i]) != board[e+i-yoffset][g]:
                                markedBoard[e+i-yoffset][g] = 0
                            board[e+i-yoffset][g] = copy.deepcopy(sorted(validLetters[i]))
                            
                    #Check if the word begins on the cell and if it doesn't then offset until the beginning of the word is found
                    xoffset = 0
                    xLength = wordLengthLookupTable[e][g][1]
                    while yLength == 0:
                        xoffset+=1
                        xLength = wordLengthLookupTable[e][g-xoffset][1]
                    #Redundent check
                    #TODO: remove
                    if (xLength != 0):
                        #Creates a list to store the valid letters for the selected word
                        validLetters = []
                        for i in range(0,xLength):
                            validLetters+=[[]]
                        #Loop thru the words
                        for word in words:
                            #Check if the word has the right length
                            if (len(word) == xLength):
                                #Counter used to keep tract of the selected letter
                                #TODO: Should maybe use a range instead of looping thru letters in word
                                counter = 0
                                valid = True
                                for letter in word:
                                    if (letter not in board[e][g+counter-xoffset]):
                                        valid = False
                                    counter+=1
                                #If the word doesn't use any illegal letters
                                if (valid):
                                    #Adds the letters of the word to validLetters
                                    for letterIndex in range(0,len(word)):
                                        if word[letterIndex] not in validLetters[letterIndex]:
                                            validLetters[letterIndex] += copy.deepcopy([word[letterIndex]])
                        #Replace letters in board with valid letters and mark the changed let
                        for i in range(0,len(validLetters)):
                            #Mark cell if letters are changed
                            if sorted(validLetters[i]) != board[e][g+i-xoffset]:
                                markedBoard[e][g+i-xoffset] = 0
                            board[e][g+i-xoffset] = copy.deepcopy(sorted(validLetters[i]))
                    #Unmark the cell
                    markedBoard[e][g] = 1

def FindLowestEntropy():
    bestCell = [0,0]
    lowestEntropy = 2
    for row in range(0,len(board)):
        for col in range(0,len(board[row])):
            if SimpleEntropy(board[row][col]) > 0 and SimpleEntropy(board[row][col]) < lowestEntropy:
                lowestEntropy = SimpleEntropy(board[row][col])
                bestCell = [row, col]
    return bestCell

def Run():
    while True:
        markedBoard = createBoard(boardHeight,boardWidth)
        Propagate(markedBoard)
        lowestEntropy = FindLowestEntropy()
        if SimpleEntropy(board[lowestEntropy[0]][lowestEntropy[1]]) == 0:
            break
        c = random.choice(board[lowestEntropy[0]][lowestEntropy[1]])
        board[lowestEntropy[0]][lowestEntropy[1]] = c
        markedBoard[lowestEntropy[0]][lowestEntropy[1]] = 0

Run()
c = 0
while board[0][0] == [] or board[0][0] == 0:
    board = Fillboard(board)
    markedBoard = createBoard(boardHeight,boardWidth)
    Run()
    c += 1
    print(c)
    
    
print(board)



