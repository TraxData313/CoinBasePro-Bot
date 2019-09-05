import numpy as np
import random
import time

# - Standardize input data (-1<x<1):
def normalizeStd(array):
	return (array - array.mean()) / array.std()
    
# - Normalize data array[n] = array[n]/lengh_array:
def normalizeLenght(array):
    sum_of_sqrs = 0
    for n in range(len(array)):
        sum_of_sqrs += array[n]**2
    lenght = np.sqrt(sum_of_sqrs)
    array = array / lenght
    return array

# - Bound input (min < input < max):
def boundInputMinMax(input, min_value, max_value):
    if input < min_value:
        input = min_value
    elif input > max_value:
        input = max_value
    return input
    
# - Bound input array (min < input < max):
def boundInputMinMaxArray(array, min_value, max_value):
    for n in range(len(array)):
        if array[n] < min_value:
            array[n] = float(min_value)
        elif array[n] > max_value:
            array[n] = float(max_value)
    return array

# - Bound input (min < input):
def boundInputMin(input, min_value):
    if input < min_value:
        input = min_value
    return input
    
def boundInputMinArray(array, min_value):
    for n in range(len(array)):
        if array[n] < min_value:
            array[n] = float(min_value)
    return array

# - Standardize sigmoid:
def sigmoid(input):
	return 1/(1 + np.exp(-input))
    
def sigmoidArray(array):
    for n in range(len(array)):
        array[n] = sigmoid(array[n])
    return array
    
# - Standard covarriance of X1 and X2:
def COV(X1,EX1,X2,EX2):
    COV = (X1-EX1)*(X2-EX2)
    return COV
    
# - Moving average:
def movingAverage(old_value, new_value, resistance):
    result = (old_value*resistance+new_value)/(resistance+1)
    return result

# - takes predicted and real binary labes and gives prediction correctness:
def classification_rate(Y, P):
	return np.mean(Y == P)

'''
Cross-Entropy Error (cost) function
J = - SUM{ ( t*log(y) + (1-t)*log(1-y) ) } , where t = target, y = output of logistic
ex:
t = 1, y = 1 -> J = 0
t = 0, y = 0 -> J = 0
t = 1, y = 0,9 -> 0,11
t = 1, y = 0,1 -> 2,3
'''
# Cross-entropy error
def cross_entropy(T, Y):
    E = 0
    for i in range(len(T)):
        if T[i] == 1:
            E -= np.log(Y[i])
        else:
            E -= np.log(1 - Y[i])
    return E
    
def println(lines):
    for n in range(lines):
        print(" ")       

# - Create diagnolized matrix:
def diagonalized(rows, cols, min=-1, max=1):
    temp_matrix = np.zeros((rows, cols))
    for row in range(rows):
        for el in range(cols):
            if el == row or el-1 == row or el+1 == row:
                if min == 0 and max == 0:
                    temp_matrix[row][el] = 0
                else:
                    temp_matrix[row][el] = random.randint(min*100,max*100)/100.
    return temp_matrix
    
### ### ###
# Block dots:
def runConnectionsPush(array_matrix, conn_matr_list, norm=0):
    # A[n+1] = np.dot(A[n],M[n])
    for n in range(len(array_matrix)-1):
        array_matrix[n+1] = np.dot(array_matrix[n],conn_matr_list[n])
    return array_matrix
    
def runConnectionsPull(array_matrix, conn_matr_list, norm=0):
    # A[n+1] = np.dot(A[n],M[n])
    n = len(array_matrix)-2
    while n >= 0:
        array_matrix[n+1] = np.dot(array_matrix[n],conn_matr_list[n])
        n = n - 1
    return array_matrix
# END Block dots
### ### ###

# - Fire or don't fire given P(Fire):
def fireNotFire(PF_array, min_value=0, max_value=1):
    F_array = []
    for el in range(len(PF_array)):
        rand_numb = random.randint(0,1000)
        # - min < PF < max:
        if PF_array[el] < min_value:
            PF_array[el] = float(min_value)
        elif PF_array[el] > max_value:
            PF_array[el] = float(max_value)
        # - Fire/NotFire:
        if rand_numb < PF_array[el]*1000:
            F_array.append(1)
        else:
            F_array.append(0)
    return F_array

# - Given array of numbers, provide one output:
def classOutput(array, min_value, max_value):
    result = np.zeros(len(array))
    # - Bound the array:
    for n in range(len(array)):
        if array[n] < min_value:
            array[n] = float(min_value)
        elif array[n] > max_value:
            array[n] = float(max_value)
    # - Total sum:
    sum = 0
    cell_numb = 0
    while cell_numb < len(array):
        sum += array[cell_numb]
        cell_numb+=1
    sum = sum*1000
    sum = int(sum)
    randInt = random.randint(0,sum)
    cell_numb    = 0
    winner       = 0
    # - Running sum:
    runnning_sum = 0
    while winner == 0:
        runnning_sum += array[cell_numb]*1000
        if randInt <= runnning_sum:
            result[cell_numb] = 1
            winner = 1
        cell_numb+=1
    return result

# Reward on A given B and given !B:
# Given the source*reward, update average R(a|b) and R(a|!b),
# where b is True/False event,
# and a is > 0 or True/False event:
def updERpAndERn(source_F_array, target_F_array, ERp_matrix, ERn_matrix, reward, resist):
    for row in range(len(source_F_array)):
        a = source_F_array[row]
        for col in range(len(target_F_array)):
            b = target_F_array[col]
            # if a > 0:
            if a > 0:
                # if b > 0, R(a|b) = a*b*reward
                if b > 0:
                    Rp = a*b*reward
                    ERp_matrix[row][col] = movingAverage(ERp_matrix[row][col], Rp, resist)
                # if b == 0, R(a|!b) = a*reward
                elif b == 0:
                    Rn = a*reward
                    ERn_matrix[row][col] = movingAverage(ERn_matrix[row][col], Rn, resist)
                else:
                    print("ERROR: b not => 0")
                    print("- b =", b)
                    print()
                    b = 1 / 0
    return ERp_matrix, ERn_matrix

# Update the MovingAverage of the COV (EC) of a and b,
# given arrays A, EA, B, EB and the current EC matrix:
def updEC(A_array, EA_array, B_array, EB_array, EC_matrix, resist):
    for row in range(len(A_array)):
        for col in range(len(B_array)):
            new_C = (A_array[row]-EA_array[row])*(B_array[col]-EB_array[col])
            EC_matrix[row][col] = movingAverage(EC_matrix[row][col], new_C, resist)
    return EC_matrix
    
# Updates the weights in a matrix using the formula:
# R = ERp - ERn
# w = R - EC*abs(R)
def updWeightBound(W_matrix, ERp_matrix, ERn_matrix, EC_matrix):
    for row in range(len(W_matrix)):
        for col in range(len(W_matrix[row])):
            R = ERp_matrix[row][col] - ERn_matrix[row][col]
            w = R - EC_matrix[row][col]*abs(R)
            if   w < -1: w = -1
            elif w >  1: w =  1
            W_matrix[row][col] = w
    return W_matrix
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


