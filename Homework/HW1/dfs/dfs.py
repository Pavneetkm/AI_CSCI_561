import numpy as np
import time

def solve(N, P,board) :
    if solveNQUtil(board,P,0,0, N):

        fout = open("output.txt", 'w')
        str1 = ""

        for p in range(0, N):
            for q in range(0,N):
                abc = int(board[p][q])
                str1 = str1 + (str(abc))
            str1 = str1 + ('\n')
        str1 = str1 + ('\r\n')

        fout.write("OK" + "\n")
        fout.write(str1)

    else :

        fout = open("output.txt", 'w')
        fout.write("FAIL")
        fout.close()


def solveNQUtil(board, P, col, row, N):
    start = time.time()
    PERIOD_OF_TIME = 280

    if (P == 0):
        return True
    if col >= N and P>0:
        return False

        # print (row,col)
    i=row

    while i<N:
    # for i in range(row,N):
        if (board[i][col] == 2):
            continue
        if isSafe(board, i, col, N):
            board[i][col] = 1
            P= P-1
            j = i+1
            while(j<N):
                if (board[j][col] == 2):
                    j=j+1
                    break
                j=j+1

            if (j < N):
                if solveNQUtil(board, P, col, j, N):
                    return True

            if solveNQUtil(board, P, col + 1, 0, N):
                return True
            board[i][col] = 0
            P =P+1
        i=i+1

    if solveNQUtil(board, P, col + 1, 0, N):
        return True
    return False





def isSafe(board,row,col,N):
    flag =True
    for i in range(0,N):
        if board[row][i] ==1:
            flag =False
        if board[row][i] == 2:
            flag = True
    if flag == False:
        return False

    i =row
    j= col
    flag =True
    while i>=0 and j>=0 :
        if board[i][j]==1:
            flag =False
        if board[i][j]==2:
            flag =True
        i = i-1
        j=j-1
    if flag == False:
        return False
    i =row
    j=col
    while i<N and j>=0:
        if board[i][j]==1:
            flag =False
        if board[i][j]==2:
            flag =True
        i = i+1
        j=j-1


    if flag == False:
        return False
    return True


if __name__== '__main__':
    fin = open("input.txt", 'r')
    fout = open("output.txt", 'w')

    with open("input.txt", 'r') as f:
        line = f.readline()
        method = line.rstrip('\n ')
        line = f.readline()
        Nval = line.rstrip()
        N = (int)(Nval)
        line = f.readline()
        Pval = line.rstrip()
        P = int(Pval)
        i = 0
        j = 0
        board=np.zeros((N,N))
        delimiter = [' ', '/n']
        while (i < N):
            j = 0
            while (j < N):
                val = f.read(1)
                if val in delimiter:
                    continue
                if val == '\n':
                    continue
                no = int(val) - int(0)
                if no >= 0 and no < 3:
                    board[i][j] = no
                j = j + 1
            i = i + 1
    solve(N,P,board)


