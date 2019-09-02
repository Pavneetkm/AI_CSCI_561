from __future__ import print_function
import numpy as np


class DFS:
    def __init__(self, N,P,Z):
        self.P =P
        self.N =N
        self.Z =np.copy(Z)


    def depthSearch(self):
        row=0
        col=0

        if self.dfssolver(row,col,self.P) :
            print(np.matrix(self.Z))
            fout = open("output.txt", 'w')
            fout.write('OK')
            fout.write(np.matrix(self.Z))
            fout.close()
            return True
        else :
            fout = open("output.txt", 'w')
            fout.write('FAIL')
            fout.close()
            print('FAIL')
            return False


    def validChild(self,row,col):
        i =row
        j=col
        while j>=0:
            if self.Z[row][j] ==2:
                break
            if self.Z[row][j]==1:
                return False
            j=j-1

        i=row
        j=col


        while i >=0 and j>=0:
            if self.Z[i][j] ==2:
                break
            if self.Z[i][j]==1:
                return False
            i =i-1
            j=j-1

        i=row
        j=col

        flag=True
        while i<self.N and j>=0 :
            if self.Z[i][j]==2:
                break
            if self.Z[i][j]==1:
                return False
            i =i+1
            j=j-1
        return True



    def dfssolver(self,row,col,P):
        if P==0:
            return True
        if P>0 and col >= self.N:
            return False
        for i in range(row,self.N):
            if self.Z[i][col] ==2:
                continue
            if self.validChild(i,col):
                self.Z[i][col]=1
                P = P-1
                #print(np.matrix(self.Z))
                j=i+1
                while j<self.N:
                    if self.Z[j][col] ==2:
                        j=j+1
                        break
                    j =j+1
                if j< self.N:
                    if self.dfssolver(j,col,P):
                        return True
                if self.dfssolver(0,col+1,P):
                    return True

                self.Z[i][col]= 0
                P = P +1

        if self.dfssolver(0,col+1,P):
            return True
        return False



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
















