from __future__ import print_function
import numpy as np
from collections import deque
import time


mydetailstack = [['alpha','beta',0,0,0,0,0,0] for alpha in range(1000)]
firstmove=[]
dep=0;
sweetheart={}
head = 0

def pop():
    global mydetailstack
    global head
    if head == 0:
        return mylist1[0], mylist1[1],mylist1[2],mylist1[3],mylist1[4],mylist1[5]
    eye = mydetailstack[head]
    head -= 1
    return eye


def push(element):
    global mydetailstack
    global head
    head += 1
    mydetailstack[head] = element



def calculate(size,board):
    list=[]
    newlist=[]
    lateboard=np.copy(board)
    visited = [[False for x in range(size)] for y in range(size)]
    for x in range(size):
        for y in range(size):
            if lateboard[x][y] != -1:

                if not visited[x][y]:

                    a=compute_neighbours(x,y,visited,board,size)

                    lateboard=a[6]

                list.append(a)
                for c in list:
                    if c not in newlist:
                        newlist.append(c)

    return newlist


def compute_neighbours(x, y,visited,board,size):
    covered = np.zeros((size,size),dtype=bool)
    value = board[x][y]
    Q = deque()
    Q.append((x,y))
    count = 0
    visited[x][y]=True
    while len(Q)!=0:
        count =count + 1
        parent = Q.popleft()
        i =parent[0]
        j =parent[1]
        covered[i][j] = True
        if i<size-1:
            if board[i+1][j] == value:
                if visited[i+1][j]==False:
                    Q.append((i+1,j))
                    visited[i+1][j] = True
        if i>0:
            if board[i-1][j] == value:
                if visited[i-1][j]==False:
                    Q.append((i-1, j))
                    visited[i-1][j] = True
        if j<size-1:
            if board[i][j+1] == value:
                if visited[i][j+1]==False:
                    Q.append((i, j+1))
                    visited[i][j+1] = True
        if j>0:
            if board[i][j-1] == value:
                if visited[i][j-1]==False:
                    Q.append((i, j-1))
                    visited[i][j-1] = True

    seconday_board = np.copy(board)


    for j in range(0,size):
        i=size-1

        while i>=0:
            if covered[i][j]==False :
                i=i-1


            if covered[i][j] == True:
                seconday_board[i][j]=-1
                i=i-1

    for col in range(0,size):

        for row in range(0,size):
            if seconday_board[row][col]==-1:
                for n in range(row,0,-1):
                    seconday_board[n][col]=seconday_board[n-1][col]
                seconday_board[0][col]=-1

    new_board= seconday_board
    totalsum = 0
    rightdiagonal=0

    for b in range(0,size):
        for c in range(0,size):
            totalsum+=new_board[b][c]

    totalsum=int(totalsum)
    leftdiagonal=0
    for h in range(0,size):
        leftdiagonal+=new_board[h][h]
    leftdiagonal= int(leftdiagonal)

    for j in range(0,size):
        for k in range(0,size):
            rightdiagonal += new_board[j][k]
    rightdiagonal =int(rightdiagonal)


    score=count*count
    return (score,x,y,totalsum,leftdiagonal,rightdiagonal,new_board)


def game_score(mylist1):
    i = 0
    first_player = 0
    second_player = 0

    for s in mylist1:
        if int((i % 2)) is 0:
            first_player += s[0]
        else:
            second_player += s[0]
        i += 1

    return (first_player - second_player)

def firstoutput():
    global firstmove

    outputlist = []
    for values in firstmove:
        outputlist.append(values[0])

    maxfirst=max(outputlist)
    new=outputlist.index(maxfirst)
    firstanswer=firstmove[new]
    outputFile = open("output.txt", 'w')

    n = firstanswer[2] + 1
    m = firstanswer[1] + 1

    char = chr(ord('@') + n)

    ans = ""

    for xaxis in range(0, size):
        for yaxis in range(0, size):
            abc = int(firstanswer[6][xaxis][yaxis])
            if (abc == -1):
                abc = "*"
            ans = ans + (str(abc))
        ans = ans + ('\n')
    ans = ans + ('\r\n')

    outputFile.write(char)
    outputFile.write(str(m) + "\n")
    outputFile.write(ans)
    outputFile.close()

    return

def alphabetaalgo (depth,mylist1,board,size):
    global dep
    global sweetheart
    global mydetailstack
    global head
    global firstmove


    alpha = float(-10000)
    beta = float(10000)

    firstmove=calculate(size,board)

    firstoutput()

    v = algo_max(alpha,beta,depth,mylist1,board,size)

    for move in firstmove:
        if ((move[0],move[1],move[2],move[3],move[4],move[5]), 1) in sweetheart:
            if sweetheart[((move[0],move[1],move[2],move[3],move[4],move[5]), 1)] == v[0]:

                return move

    return firstmove[1]



def algo_max(alpha, beta,depth,mylist1,board,size):
    global dep
    global sweetheart
    global firstmove
    global mydetailstack
    global head
    v = float('-inf')
    result = False

    if depth is dep:
        r = game_score(mylist1)
        return [r, result]

    if dep==0:
        possible_moves=firstmove
    else:
        possible_moves = calculate(size,board)

    if not possible_moves:
        r = game_score(mylist1)
        return [r,result]



    for move in possible_moves:
        last_move=move
        push([alpha, beta,move[0], move[1],move[2],move[3],move[4],move[5]])


        dep += 1
        sweetheart[((move[0],move[1],move[2],move[3],move[4],move[5]), dep)] = v
        mylist1.append(move)

        [temp1,l]= algo_min(alpha,beta,depth,mylist1,move[6],size)
        mylist1.remove(move)

        v = max(v, temp1)
        a_pop = pop()
        sweetheart[((a_pop[2],a_pop[3],a_pop[4],a_pop[5],a_pop[6],a_pop[7]),dep)] = temp1


        dep -= 1
        if beta <= v:
            result = True
            return [v, result]
        alpha=max(alpha,v)
        mydetailstack[head][0] = alpha

    return [v,result]


def algo_min(alpha,beta,depth,mylist1,board,size):
    global dep
    global sweetheart
    global mydetailstack
    global head

    v = float('inf')
    result = False


    if depth is dep:
        r = game_score(mylist1)
        return [r, result]

    possible_moves = calculate(size, board)


    if not possible_moves:
        r = game_score(mylist1)
        return [r, result]

    for move in possible_moves:
        last_move = move
        push([alpha, beta,move[0], move[1],move[2],move[3],move[4],move[5]])


        dep += 1
        sweetheart[((move[0],move[1],move[2],move[3],move[4],move[5]), dep)] = v
        mylist1.append(move)
        [temp1, l] = algo_max(alpha,beta,depth,mylist1,move[6],size)
        mylist1.remove(move)

        v = min(v, temp1)
        a_pop=pop()
        sweetheart[((a_pop[2],a_pop[3],a_pop[4],a_pop[5],a_pop[6],a_pop[7]),dep)] = temp1


        dep -= 1
        if alpha >= v:

            result = True
            return [v, result]

        beta = min(beta, v)
        mydetailstack[head][1] = beta

    return [v,result]





if __name__ == "__main__":

    readfromfile = open("input.txt", 'r')

    with readfromfile as f:
        line = f.readline()
        Sizeofboard = line.rstrip()
        size = (int)(Sizeofboard)
        line = f.readline()
        Fruitsnumber = line.rstrip()
        board = np.zeros((size, size))
        fruits = int(Fruitsnumber)
        line=f.readline()
        Timeleft=line.rstrip()
        timerforgame=(float)(Timeleft)
        Z=np.zeros((size,size))

        i = 0
        j = 0

        delimiter = [' ', '/n']
        while (i < size):
            j = 0
            while (j < size):
                val = f.read(1)
                if val in delimiter:
                    continue
                if val == '\n':
                    continue

                if val=="*":
                    val = -1

                no = int(val) - int(0)
                if no >= -1 and no < 9 :
                     Z[i][j] = no
                     board[i][j]=no
                j = j + 1
            i = i + 1;


        stoptime1 = 295
        stoptime2 = 200
        stoptime3 = 100
        stoptime4 = 40
        stoptime5 = 10
        stoptime6 = 180
        stoptime7 = 250

        mylist1=[]

        if size<7:
            if timerforgame> stoptime2:
                depth=4
            elif timerforgame>stoptime3:
                depth=3
            elif timerforgame>stoptime5:
                depth=2
            else:
                depth=1

        if size<11:
            if timerforgame> stoptime2:
                depth=3
            elif timerforgame>stoptime3:
                depth=2
            elif timerforgame<=stoptime5:
                depth=1

        if size<=15:
            if timerforgame> stoptime6:
                depth=2
            else:
                depth=1


        if size>15 and size <19:
            if timerforgame > stoptime7:
                depth = 2
            else:
                depth = 1


        if size >18:
            if timerforgame > stoptime1:
                depth = 2
            else:
                depth = 1




        b=alphabetaalgo(depth,mylist1,board,size)

        outputFile = open("output.txt", 'w')

        move=b

        n = move[2] + 1
        m = move[1] + 1

        char = chr(ord('@') + n)
        a = move[6]

        ans = ""

        for xaxis in range(0, size):
            for yaxis in range(0, size):
                abc = int(move[6][xaxis][yaxis])
                if (abc == -1):
                    abc = "*"
                ans = ans + (str(abc))
            ans = ans + ('\n')
        ans = ans + ('\r\n')

        outputFile.write(char)
        outputFile.write(str(m) + "\n")
        outputFile.write(ans)
        outputFile.close()
