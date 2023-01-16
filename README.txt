How to run the program:
1) Change the database used at the top of the program
2) Change the blank cells in the 'startingBlanks' list at the top of the program
3) Change the board size or alphabet by changing the input parameters to the 'Run' function
4) Run the program in python


Changing expansions:

Backtracking:
1) Place a 'break' af the line 
        if WeightedEntropy(board[lowestEntropy[0]][lowestEntropy[1]],weights) == 0:
    and before
        if IsBoardValid(board,startingBlanks):

Use 'WeightedEntropy' or 'SimpleEntropy':
1) Change all usages of 'WeightedEntropy' with 'SimpleEntropy' or all usages of 'SimpleEntropy' with 'WeightedEntropy'

Consider neighbouring cell when calculating entropy:
1) Change all usages of 'FindLowestEntropy' with 'FindLowestEntropyNeighbour' or all usages of 'FindLowestEntropyNeighbour' with 'FindLowestEntropy'