from __future__ import print_function
import numpy as np
from collections import deque
import time

import math

import random


Q = deque()
flag_sol = False
solution_state = None


class Struct:
    def __init__(self,N,P,list):
        self.N=N
        self.P=P
        self.list=[x for x in list]




def checkifvalid(state,row,col,N,P,Z):
    global flag_sol
    global Q
    global solution_state
    temp_board = np.copy(Z)
    for k in state.l:
        temp_board[k[0]][k[1]] =1
    i=col
    while i>=0:
        if temp_board[row][i] ==1:
            return False
        if temp_board[row][i] ==2:
            break
        i=i-1


    i = row
    j = col
    while i>=0 and j>=0:
        if temp_board[i][j]==1:
            return False
        if temp_board[i][j]==2:
            break
        i=i-1
        j=j-1

    i =row
    j=col
    while i < N and j >= 0:
        if temp_board[i][j] == 1:
            return False
        if temp_board[i][j] == 2:
            break
        i = i + 1
        j = j - 1
    return True




def BFS(N,P,Z1):
    global flag_sol
    global Q
    global solution_state
    col = 0
    start = time.time()
    PERIOD_OF_TIME = 300

    while (col < N):
        for i in range(N):
            if Z1[i][col] == 2:
                continue
            list = []
            list.append((i, col))
            state = Struct(N, P - 1, list)
            Q.append(state)
        while (len(Q) != 0 and not flag_sol) and time.time() < start + PERIOD_OF_TIME:
            current_state = Q.popleft()
            find_children(current_state,N,P,Z1)

        if not flag_sol:
            failureoutput(N)
        else:
            finalanswer(N,solution_state,Z1)

        col=col+1

def find_children(state,N,P,Z):
    global flag_sol
    global Q
    global solution_state
    k = len(state.l)
    k = k - 1
    current_row = state.l[k][0]
    current_col = state.l[k][1]
    i = current_row + 1
    while (i < N):
        if Z[i][current_col] == 2:
            break
        i = i + 1
    i = i + 1

    if i < N:
        while (i < N):
            if Z[i][current_col] == 0:
                if checkifvalid(state, i, current_col,N,P,Z):
                    child_state = Struct(state.N, state.P - 1, state.l)
                    child_state.l.append((i, current_col))
                    if not P:
                        flag_sol = True
                        solution_state = child_state
                    Q.append(child_state)
            i = i + 1
    if current_col == N - 1:
        return
    while (current_col < N - 1):
        for j in range(0, N):
            if Z[j][current_col + 1] == 0:
                if checkifvalid(state, j, current_col + 1,N,P,Z):
                    child_state = Struct(state.N, state.P - 1, state.l)
                    child_state.l.append((j, current_col + 1))
                    if child_state.P == 0:
                        flag_sol= True
                        solution_state = child_state
                    Q.append(child_state)

        current_col = current_col + 1


def newstategenerator(N, P,checkboard,factor):
    abc = 2
    newlist =[]
    number = 0

    while P>number :
        yaxis = random.randrange(0, N)
        xaxis = random.randrange(0,N)

        if checkboard[xaxis][yaxis] == abc:
            continue

        newlist.append((xaxis,yaxis))
        number += 1

    return newlist


def conflictcalculator(answer):
    num = 0
    abc=len(answer)

    for oldlocation in range(0, abc):
        xyz=oldlocation+1
        for newlocation in range(xyz, abc):

            if answer[oldlocation][1] == answer[newlocation][1]:
                least1= min(answer[oldlocation][0],answer[newlocation][0])
                most1= max(answer[oldlocation][0],answer[newlocation][0])
                while(least1 !=most1):
                    if(checkboard[least1][answer[oldlocation][1]] ==2):
                        break
                    least1 += 1
                    if(least1==most1):
                        num += 1

            if answer[oldlocation][1]+answer[oldlocation][0] == answer[newlocation][1] +answer[newlocation][0]:
                least2= min(answer[oldlocation][1],answer[newlocation][1])
                most2= max(answer[oldlocation][1],answer[newlocation][1])
                previousrow = min(answer[oldlocation][0], answer[newlocation][0])
                while (least2 != most2):
                    if (checkboard[previousrow][most2]==2):
                        break
                    previousrow += 1
                    most2 = most2 - 1


                    if (least2==most2):
                        num += 1

            if answer[oldlocation][1]-answer[oldlocation][0] == answer[newlocation][1] -answer[newlocation][0]:
                least3=min(answer[oldlocation][0],answer[newlocation][0])
                most3=max(answer[oldlocation][0],answer[newlocation][0])
                previouscolumn = min(answer[oldlocation][1],answer[newlocation][1])

                while(least3!=most3):
                    if(checkboard[least3][previouscolumn]==2):
                        break
                    least3 += 1
                    previouscolumn += 1


                    if(least3==most3):
                        num += 1

            if answer[oldlocation][0] == answer[newlocation][0]:
                least4 =min(answer[oldlocation][1],answer[newlocation][1])
                most4 =max(answer[oldlocation][1],answer[newlocation][1])
                while(least4!=most4):
                    if(checkboard[answer[oldlocation][0]][least4] ==2):
                        break
                    least4 += 1
                    if(least4==most4):
                        num += 1

    return num

def futureposition(present,lizards,size):
    flag = 0
    position = random.randrange(0,lizards)
    present = present[:]
    while flag == 0:
        yaxis = random.randrange(0, N)
        xaxis = random.randrange(0,N)

        newlocation=(xaxis,yaxis)
        if newlocation in present:
            continue
        elif checkboard[xaxis][yaxis] == 2:
            continue
        flag = 1
        present[position]=newlocation

    return present


def simannealing(checkboard, lizards, temp, factor,size):
    start = time.time()
    PERIOD_OF_TIME = 250
    endlimit = 25000

    present = newstategenerator(size,lizards,checkboard,factor)
    pconflict = conflictcalculator(present)

    for startlimit in range(endlimit):

        future = futureposition(present,lizards,size)
        newconflicts = conflictcalculator(future)
        temp = factor * temp

        difference = newconflicts - pconflict

        if difference<0 or math.exp(-difference / temp) > random.uniform(0,1) and time.time() < start + PERIOD_OF_TIME:
            pconflict = newconflicts
            present = future

            if not pconflict:
              finalanswer(size,present,checkboard)
              return present

        failureoutput(size)

    return None

def failureoutput(size):
    writeinfile = open("output.txt", 'w')
    writeinfile.write("FAIL")
    writeinfile.close()

def finalanswer(N,answer,checkboard):
    ans = ""

    for state in answer:
        checkboard[state[0]][state[1]]=1

    for xaxis in range(0, N):
        for yaxis in range(0, N):
            abc = int(checkboard[xaxis][yaxis])
            ans = ans + (str(abc))
        ans = ans + ('\n')
    ans = ans + ('\r\n')
    writeinfile = open("output.txt", 'w')
    writeinfile.write("OK" + "\n")
    writeinfile.write(ans)
    writeinfile.close()


if __name__ == "__main__":
    readfromfile = open("input.txt", 'r')
    writeinfile = open("output.txt", 'w')

    with readfromfile as f:
        line = f.readline()
        method = line.rstrip('\n')
        line = f.readline()
        Nval = line.rstrip()
        N = (int)(Nval)
        line = f.readline()
        Pval = line.rstrip()
        checkboard = np.zeros((N, N))
        P = int(Pval)
        Z=np.zeros((N,N))

        i = 0
        j = 0

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
                    Z[i][j] = no
                    checkboard[i][j]=no
                j = j + 1
            i = i + 1

        if(method=="BFS"):
            BFS(N,P,Z)
        elif (method == "SA"):
            simannealing(checkboard, P, 350, 0.8, N)
        else:
            BFS(N,P,Z)

