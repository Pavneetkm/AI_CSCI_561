import math
import numpy as np
import random
import time

def generateRandomState(n, p,board):
    no =0
    randPoints =[]
    while no <P :
        x = random.randrange(0,N)
        y = random.randrange(0,N)
        if board[x][y] == 2:
            continue
        randPoints.append((x,y))
        no=no+1
    # print randPoints
    return randPoints


#Cost function for Simulated Annealing
def costFunction(solution):
    cost = 0
    for position in range(0, len(solution)):
        for next_position in range(position+1, len(solution)):
            if solution[position][0] == solution[next_position][0]:
                min1 =min(solution[position][1],solution[next_position][1])
                max1 =max(solution[position][1],solution[next_position][1])
                while(min1!=max1):
                    if(board[solution[position][0]][min1] ==2):
                        break
                    min1 =min1 +1
                    if(min1==max1):
                        cost = cost + 1

            if solution[position][1] == solution[next_position][1]:
                min2= min(solution[position][0],solution[next_position][0])
                max2= max(solution[position][0],solution[next_position][0])
                while(min2 !=max2):
                    if(board[min2][solution[position][1]] ==2):
                        break
                    min2=min2+1
                    if(min2==max2):
                        cost =cost + 1

            if solution[position][1]-solution[position][0] == solution[next_position][1] -solution[next_position][0]:
                min3=min(solution[position][0],solution[next_position][0])
                max3=max(solution[position][0],solution[next_position][0])
                min_col = min(solution[position][1],solution[next_position][1])

                while(min3!=max3):
                    if(board[min3][min_col]==2):
                        break
                    min3=min3+1
                    min_col =min_col+1


                    if(min3==max3):
                        cost =cost +1

            if solution[position][1]+solution[position][0] == solution[next_position][1] +solution[next_position][0]:
                min4= min(solution[position][1],solution[next_position][1])
                max4= max(solution[position][1],solution[next_position][1])
                min_row = min(solution[position][0], solution[next_position][0])
                while (min4 != max4):
                    if (board[min_row][max4]==2):
                        break
                    min_row = min_row + 1
                    max4 = max4 - 1


                    if (min4==max4):
                        cost = cost + 1

    return cost

def generateNextState(state): # randomly swap two values
    state = state[:]
    position = random.randrange(0,P)
    repete = False
    while repete == False:
        x = random.randrange(0,N)
        y = random.randrange(0,N)
        position_new=(x,y)
        if board[x][y]==2:
            continue
        elif position_new in state:
            continue
        state[position]=position_new
        repete =True
    return state


def simulatedAnnealing(size, temperature, alpha, lizards,board):
    start = time.time()
    PERIOD_OF_TIME = 250
    max_iter = 25000
    current_state = generateRandomState(size,lizards,board)
    current_cost = costFunction(current_state)

    for iteration in range(max_iter):
        #print_solution(current_state,size)
        # print(current_cost,temperature)
        temperature = temperature * alpha

        next_state = generateNextState(current_state)
        next_cost = costFunction(next_state)
        delta_E = next_cost - current_cost
        if delta_E<0 or math.exp(-delta_E / temperature) > random.uniform(0,1) and time.time() < start + PERIOD_OF_TIME:
           current_state = next_state
           current_cost = next_cost


           if current_cost == 0:
              print_solution(current_state,size,board)

              # print(iteration)
              return current_state

        fout=open("output.txt",'w')
        fout.write("FAIL")
        fout.close()

    return None


def print_solution(solution,N,board):
    fout = open("output.txt", 'w')
    str1=""

    for state in solution:
        board[state[0]][state[1]]=1

    # print(board)
    for p in range(0, N):
        for q in range(0, N):
            abc = int(board[p][q])
            str1 = str1 + (str(abc))
        str1 = str1 + ('\n')
    str1 = str1 + ('\r\n')
    fout.write("OK" + "\n")
    fout.write(str1)
    fout.close()



if __name__ =='__main__':

    fin = open("input.txt", 'r')
    fout = open("output.txt", 'w')

    with open("input.txt", 'r') as f:
        line = f.readline()
        method = line.rstrip('\n ')
        line = f.readline()
        # print(line)
        Nval = line.rstrip()
        N = (int)(Nval)
        line = f.readline()
        Pval = line.rstrip()
        P = int(Pval)
        board =np.zeros((N,N))
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
                    board[i][j] = no
                j = j + 1
            i = i + 1
    simulatedAnnealing(N,350,0.8,P,board)