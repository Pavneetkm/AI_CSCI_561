from __future__ import print_function
import numpy as np
from collections import deque
import time


class Struct:
    def __init__(self,N,P,l):
        self.N=N
        self.P=P
        self.l=[x for x in l]




class Solver:
    def __init__(self,N, P):
        self.N=N
        self.P=P
        self.Z =np.zeros((N,N))
        self.Q = deque()
        self.flag_sol= False
        self.solution_state =None

    def checkifvalid(self,state,row,col):
        temp_board = np.copy(self.Z)
        for k in state.l:
            temp_board[k[0]][k[1]] =1
        # print(np.matrix(temp_board))
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

    def find_children(self, state):
        k = len(state.l)
        k = k - 1
        current_row = state.l[k][0]
        current_col = state.l[k][1]
        # print(' finding children of (%d,%d)'%(current_row,current_col))
        i = current_row + 1
        while (i < N):
            if self.Z[i][current_col] == 2:
                break
            i = i + 1
        i = i + 1

        if i < N:
            while (i < N):
                if self.Z[i][current_col] == 0:
                    if self.checkifvalid(state, i, current_col):
                        child_state = Struct(state.N, state.P - 1, state.l)
                        child_state.l.append((i, current_col))
                        if not P:
                            self.flag_sol = True
                            self.solution_state = child_state
                        self.Q.append(child_state)
                i = i + 1
        if current_col == N - 1:
            return
        while (current_col < N - 1):
            for j in range(0, N):
                if self.Z[j][current_col + 1] == 0:
                    if self.checkifvalid(state, j, current_col + 1):
                        child_state = Struct(state.N, state.P - 1, state.l)
                        child_state.l.append((j, current_col + 1))
                        if child_state.P == 0:
                            self.flag_sol = True
                            self.solution_state = child_state
                        self.Q.append(child_state)

            current_col = current_col + 1

    def print_solution(self, state):
        fout = open("output.txt", 'w')
        str1 = ""
        for k in state.l:
            self.Z[k[0]][k[1]] = 1

        for p in range(0, self.N):
            for q in range(0, self.N):
                abc = int(self.Z[p][q])
                str1 = str1 + (str(abc))
            str1 = str1 + ('\n')
        str1 = str1 + ('\r\n')

        fout.write("OK" + "\n")
        fout.write(str1)
        fout.close()

    def BFS(self):
        col = 0
        start = time.time()
        PERIOD_OF_TIME = 300  # 5min


        while (col < N):
            for i in range(N):
                if self.Z[i][col] == 2:
                    continue
                l = []
                l.append((i, col))
                state = Struct(N, P - 1, l)
                self.Q.append(state)
            while (len(self.Q) != 0 and self.flag_sol == False) and time.time() < start + PERIOD_OF_TIME:
                current_state = self.Q.popleft()
                self.find_children(current_state)

            if self.flag_sol == False:
                fout = open("output.txt", 'w')
                fout.write("FAIL")
                fout.close()

            else:
                self.print_solution(self.solution_state)

            col=col+1


if __name__ == "__main__":
    fin = open("input.txt", 'r')
    fout = open("output.txt", 'w')

    with open("input.txt", 'r') as f:
        line = f.readline()
        method = line.rstrip('\n ')
	print (method)
        line = f.readline()
        Nval = line.rstrip()
        N = (int)(Nval)
        line = f.readline()
        Pval = line.rstrip()
        P = int(Pval)

        s =Solver(N,P)
        i = 0
        j = 0

        Q = deque()
        flag_sol = False
        solution_state = None

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
                    s.Z[i][j] = no
                j = j + 1
            i = i + 1
        s.BFS()
