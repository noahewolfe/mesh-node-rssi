#2D lists & time based animation

def makeMagicSquare(n):

    if n%2 == 0:

        return None

    board = [[None]*n for row in range(n)]

    currRow, currCol, num = 0, 1, 1 

    board[currRow][currCol] = num

    # up and to the right
    # or, down if its already a number

    while num < (n**2):

        num += 1

        newRow, newCol = getCoords(n, currRow, currCol)
        #print("from get coords", newRow, newCol)
        if board[newRow][newCol] == None:

            board[newRow][newCol] = num

        else:
            # need to go down one from the starting position!
            newRow = currRow + 1 
            
            if newRow >= n:
                newRow = n - newRow

            newCol = currCol 

            board[newRow][newCol] = num
            #print("changin to", newRow, newCol)

        currRow = newRow

        currCol = newCol

        #print("currRow, currCol",currRow, currCol)

        

    return board



def getCoords(n, currRow, currCol):

    newRow = currRow - 1 

    newCol = currCol + 1

    if newRow < 0:

        newRow = n + newRow 

    if newCol >= n:

        newCol = n - newCol

    return newRow, newCol

### Random garbage I found on the internet ###

# Python3 program to check whether a given  
# matrix is magic matrix or not 
N = 3
  
# Returns true if mat[][] is magic 
# square, else returns false. 
def isMagicSquare( mat) : 
    print(mat)
    # calculate the sum of  
    # the prime diagonal 
    s = 0
    for i in range(0, N) : 
        s = s + mat[i][i] 
  
    # For sums of Rows  
    for i in range(0, N) : 
        rowSum = 0;      
        for j in range(0, N) : 
            rowSum += mat[i][j] 
          
        # check if every row sum is 
        # equal to prime diagonal sum 
        if (rowSum != s) : 
            return False
  
    # For sums of Columns 
    for i in range(0, N): 
        colSum = 0
        for j in range(0, N) : 
            colSum += mat[j][i] 
  
        # check if every column sum is  
        # equal to prime diagonal sum 
        if (s != colSum) : 
            return False
  
    return True
  
# Driver Code 
mat = makeMagicSquare(3)
      
if (isMagicSquare(mat)) : 
    print( "Magic Square") 
else : 
    print( "Not a magic Square") 