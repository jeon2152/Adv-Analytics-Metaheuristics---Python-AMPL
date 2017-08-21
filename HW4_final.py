# basic hill climbing search provided as base code for the DSA/ISE 5113 course
# author: Charles Nicholson
# date: 4/5/2017

# NOTE: YOU MAY CHANGE ALMOST ANYTHING YOU LIKE IN THIS CODE.
# However, I would like all students to have the same problem instance, therefore please do not change anything relating to:
#   random number generation
#   number of items (should be 100)
#   random problem instance
#   weight limit of the knapsack

# ------------------------------------------------------------------------------

# Student name: Jiwon Jeon and Andrew Rocha
# Date: 4/22/2017


# need some python libraries
import copy
from random import Random  # need this for the random number generation -- do not change
import numpy as np
import math
# to setup a random number generator, we will specify a "seed" value
# need this for the random number generation -- do not change
seed = 5113
myPRNG = Random(seed)

# to get a random number between 0 and 1, use this:             myPRNG.random()
# to get a random number between lwrBnd and upprBnd, use this:  myPRNG.uniform(lwrBnd,upprBnd)
# to get a random integer between lwrBnd and upprBnd, use this: myPRNG.randint(lwrBnd,upprBnd)

# number of elements in a solution
n = 100

# create an "instance" for the knapsack problem
value = []
for i in range(0, n):
    value.append(myPRNG.uniform(10, 100))

weights = []
for i in range(0, n):
    weights.append(myPRNG.uniform(5, 20))

# define max weight for the knapsack
maxWeight = 5 * n


# setups for local searches -------------------------------------------------------------------

# function to evaluate a solution x
def evaluate(x):
    a = np.array(x)
    b = np.array(value)
    c = np.array(weights)

    totalValue = np.dot(a, b)   # compute the value of the knapsack selection
    totalWeight = np.dot(a, c)  # compute the weight value of the knapsack selection

    if totalWeight > maxWeight:
        # print ("The solution is infeasible. Repeat the process!")
        totalValue = 0

    return [totalValue, totalWeight]  # returns a list of both total value and total weight


# here is a simple function to create a neighborhood
# 1-flip neighborhood of solution x
def neighborhood(x):
    nbrhood = []

    for i in range(0, n):
        nbrhood.append(x[:])
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1

    return nbrhood

# k-flip neighborhood of solution x with given k-times
# (to be used for Basic Variable Neighborhood Search)
def neighborhood_k(x, k):
    nbrhood = []

    for i in range(0, int(n/k)):
        nbrhood.append(x[:])

        for j in range(0,k):
            if nbrhood[i][i+j*int(n/k)] == 1:
                nbrhood[i][i+j*int(n/k)] = 0
            else:
                nbrhood[i][i+j*int(n/k)] = 1

    return nbrhood


# create the initial solution

# assign 0's to all items inside the solution list
"""
def initial_solution():
    x = []  # i recommend creating the solution as a list

    # assign 0's to all items: no items are selected.
    for i in range(0, n):
        x.append(0)

    return x
"""
# randomly pick 30 items and assign 1's. Others are assigned with 0's
def initial_solution():
    x = []
    for i in range(0,n):              # assign 0's to all items
        x.append(0)

    y = myPRNG.sample(range(0,n),30)
    for i in y:                       # select 30 indices randomly and assign 1's
        x[i] = 1

    if evaluate(x)[1] > maxWeight:    # if total weight > max weight, iterate the process
        x = initial_solution()        # till total weight <= max weight

    return x

x_initial = initial_solution()        # x_initial will hold the initial solution to implement local searches
print(x_initial)

# variable to record the number of solutions evaluated
"""
# monitor the number of solutions evaluated
solutionsChecked = 0

x_curr = initial_solution()  # x_curr will hold the current solution
x_best = x_curr[:]           # x_best will hold the best solution
f_curr = evaluate(x_curr)    # f_curr will hold the evaluation of the current solution
f_best = f_curr[:]
"""


# begin local search overall logic ----------------------------------------------------------------------

# -----------------------------------------------
# Question 2: Hill Climbing with Best Improvement
# -----------------------------------------------

# as Best Improvement will be used for hill climbing logic,
# define BestImprovement function

def BestImprovement(x_initial):
    solutionsChecked = 0

    x_curr = x_initial[:]

    x_best = x_curr[:]         # x_best will hold the best solution
    f_curr = evaluate(x_curr)  # f_curr will hold the evaluation of the current solution
    f_best = f_curr[:]

    done = 0

    while done == 0:

        Neighborhood = neighborhood(x_curr)  # create a list of all neighbors in the neighborhood of x_curr

        for s in Neighborhood:               # evaluate every member in the neighborhood of x_curr
            solutionsChecked = solutionsChecked + 1
            if evaluate(s)[0] > f_best[0]:
                x_best = s[:]                # find the best member and keep track of that solution
                f_best = evaluate(s)[:]      # and store its evaluation

        if f_best == f_curr:                 # if there were no improving solutions in the neighborhood
            done = 1

        else:
            x_curr = x_best[:]  # else: move to the neighbor solution and continue
            f_curr = f_best[:]  # evaluate the current solution

    #print("\nFinal number of solutions checked: ", solutionsChecked)
    #print("Best value found: ", f_best[0])
    #print("Weight is: ", f_best[1])
    #print("Total number of items selected: ", np.sum(x_best))
    #print("Best solution: ", x_best)

    result = [solutionsChecked, f_best[0], f_best[1], np.sum(x_best), x_best]
    return result

print(BestImprovement(x_initial))


# ------------------------------------------------
# Question 3: Hill Climbing with First Improvement
# ------------------------------------------------

# in case that First Improvement is used for hill climbing logic,
# define FirstImprovement function

def FirstImprovement(x_initial):
    solutionsChecked = 0

    x_curr = x_initial[:]

    x_best = x_curr[:]         # x_best will hold the best solution
    f_curr = evaluate(x_curr)  # f_curr will hold the evaluation of the current solution
    f_best = f_curr[:]

    done = 0

    while done == 0:

        Neighborhood = neighborhood(x_curr)  # create a list of all neighbors in the neighborhood of x_curr

        for s in Neighborhood:               # evaluate every member in the neighborhood of x_curr
            solutionsChecked = solutionsChecked + 1
            if evaluate(s)[0] > f_best[0]:
                x_best = s[:]                # find the best member and keep track of that solution
                f_best = evaluate(s)[:]      # and store its evaluation
                break                        # exit the for loop when the first best solution is found

        if f_best == f_curr:                 # if there were no improving solutions in the neighborhood
            done = 1

        else:
            x_curr = x_best[:]  # else: move to the neighbor solution and continue
            f_curr = f_best[:]  # evaluate the current solution

    #print("\nFinal number of solutions checked: ", solutionsChecked)
    #print("Best value found: ", f_best[0])
    #print("Weight is: ", f_best[1])
    #print("Total number of items selected: ", np.sum(x_best))
    #print("Best solution: ", x_best)

    result = [solutionsChecked, f_best[0], f_best[1], np.sum(x_best), x_best]
    return result

print(FirstImprovement(x_initial))


# ----------------------------------------------
# Question 4: Hill Climbing with Random Restarts
# ----------------------------------------------

# use Best Improvement for hill climbing logic

# set the number of random restart
nr = 200

# monitor the number of solutions evaluated
solutionsChecked = 0

for i in range(0,nr):
    x_curr = initial_solution()
    result_curr = BestImprovement(x_curr)
    solutionsChecked = solutionsChecked + result_curr[0]

    if i == 0:
        result_best = result_curr[:]

    else:
        if result_curr[1] > result_best[1]:
            result_best = result_curr[:]

print("\nFinal number of solutions checked: ", solutionsChecked)
print("Best value found: ", result_best[1])
print("Weight is: ", result_best[2])
print("Total number of items selected: ", np.sum(result_best[4]))
print("Best solution: ", result_best[4])


# ------------------------------------------
# Question 5: Hill Climbing with Random Walk
# ------------------------------------------

# use Best Improvement for hill climbing logic

P = 0.2     # governing probability for random walk
N = 50      # number of random walk

# start from the initial solution
x_curr = x_initial

# monitor the number of solutions evaluated
solutionsChecked = 0

for i in range(0,N):
    p = myPRNG.random()

    if p < P:
        result_curr = FirstImprovement(x_curr)
        Xcurr = result_curr[4]
        Fcurr = evaluate(Xcurr)
        solutionsChecked = solutionsChecked + result_curr[0]

    else:
        r_curr = neighborhood(x_curr)[myPRNG.randint(0,n-1)]
        result_curr = FirstImprovement(r_curr)
        Xcurr = result_curr[4]
        #Xcurr = r_curr
        Fcurr = evaluate(Xcurr)

        solutionsChecked = solutionsChecked + result_curr[0]
        #solutionsChecked = solutionsChecked + 1

    x_curr = Xcurr

    if i == 0:
        result_best = result_curr[:]

    else:
        if result_curr[1] > result_best[1]:
            result_best = result_curr[:]

print("\nFinal number of solutions checked: ", solutionsChecked)
print("Best value found: ", result_best[1])
print("Weight is: ", result_best[2])
print("Total number of items selected: ", result_best[3])
print("Best solution: ", result_best[4])


# -------------------------------
# Question 6: Simulated Annealing
# -------------------------------

#Cooling schedules
def cooling_1():
    new_temp = 0.99*current_temp
    return new_temp

def cooling_2():
    new_temp = 0.95*current_temp
    return new_temp

def cooling_3():
    new_temp = 0.90*current_temp
    return new_temp

def cooling_4():
    new_temp = 0.80*current_temp
    return new_temp

def cooling_5():
    new_temp = 0.50*current_temp
    return new_temp


# start from the initial solution
x_curr = x_initial
x_best = x_curr[:]
f_curr = evaluate(x_curr)[0]
totalWeight = evaluate(x_curr)[1]
f_best = f_curr

# monitor the number of solutions evaluated
solutionsChecked = 0
# Iterations for each specific temp
Mk = 500
#temperatures: (Ti and Ts)
current_temp = 10000
stop_temp = 1

# main
done = 0

while done == 0:
    # iterations per cooling
    m = 0

    while m < Mk:
        # create a list of all neighbors in the neighborhood of x_curr
        Neighborhood = neighborhood(x_curr)

        # randomly select a solution in the neighborhood of x_curr
        s = Neighborhood[np.random.randint(0, len(Neighborhood))]

        solutionsChecked = solutionsChecked + 1

        if evaluate(s)[0] > f_best:
            # find the best member and keep track of that solution
            x_best = s[:]
            # evaluation value
            f_best = evaluate(s)[0]
            # evaluate weight
            totalWeight = evaluate(s)[1]
        else:
            Difference = f_best - evaluate(s)[0]
            Xi = np.random.uniform()

            if Xi <= math.exp(-Difference / current_temp):
                x_best = s[:]
                f_best = evaluate(s)[0]
                totalWeight = evaluate(s)[1]

        # increase the iteration
        m += 1

    # change the temperature
    current_temp = cooling_5()

    # if it should be stopped
    if current_temp < stop_temp:
        done = 1
    else:
        x_curr = x_best[:]
        # evaluate the current solution
        f_curr = f_best

        # printing outputs
        print("\nFinal: Total number of solutions checked: ", solutionsChecked)
        print("Best value found: ", f_best)
        print("Weight of knapsack: ", totalWeight)
        print("Best solution: ", x_best)


# ------------------------------------------------
# Question 7-1: Basic Variable Neighborhood Search
# ------------------------------------------------

# use Best Improvement for local search (LS)

k_max = 10     # number of neighborhood structures
l_max = 3      # number of cycles to perform Basic VNS, i.e. number of starting solution

x_curr = x_initial
f_curr = evaluate(x_curr)
f_bestLocal = f_curr

solutionsChecked = 0

l = 1
while l <= l_max:
    k = 1
    while k <= k_max:
        Neighborhood = neighborhood_k(x_curr, k)   # change the neighborhood structure by changing the number of flips
        s_index = myPRNG.randint(0,int(n/k)-1)
        s_random = Neighborhood[s_index]           # s, a random solution in Nk(current)
        LS = BestImprovement(s_random)             # LS, Local Search
        s_best = LS[4]                             # s*, local best solution from Local Search
        sf_best = evaluate(s_best)                 # value of s*
        solutionsChecked = solutionsChecked + LS[0]

        if sf_best[0] > evaluate(x_curr)[0]:
            x_curr = s_best[:]
            f_curr = sf_best[:]
            k = 1
        else:
            k = k+1

    if f_bestLocal[0] == f_curr[0]:                # if the local best solution is same as the current solution,
        l = l+1                                    # start the basic VNS cycle again
    else:
        l = 1
        s_bestLocal = x_curr
        f_bestLocal = f_curr

print("\nFinal number of solutions checked: ", solutionsChecked)
print("Best value found: ", f_bestLocal[0])
print("Weight is: ", f_bestLocal[1])
print("Total number of items selected: ", np.sum(s_bestLocal))
print("Best solution: ", s_bestLocal)


# use First Improvement for local search (LS)

k_max = 10     # number of neighborhood structures
l_max = 3      # number of cycles to perform Basic VNS, i.e. number of starting solution

x_curr = x_initial
f_curr = evaluate(x_curr)
f_bestLocal = f_curr

solutionsChecked = 0

l = 1
while l <= l_max:
    k = 1
    while k <= k_max:
        Neighborhood = neighborhood_k(x_curr, k)   # change the neighborhood structure by changing the number of flips
        s_index = myPRNG.randint(0,int(n/k)-1)
        s_random = Neighborhood[s_index]           # s, a random solution in Nk(current)
        LS = FirstImprovement(s_random)            # LS, Local Search
        s_best = LS[4]                             # s*, local best solution from Local Search
        sf_best = evaluate(s_best)                 # value of s*
        solutionsChecked = solutionsChecked + LS[0]

        if sf_best[0] > evaluate(x_curr)[0]:
            x_curr = s_best[:]
            f_curr = sf_best[:]
            k = 1
        else:
            k = k+1

    if f_bestLocal[0] == f_curr[0]:                # if the local best solution is same as the current solution,
        l = l+1                                    # start the basic VNS cycle again
    else:
        l = 1
        s_bestLocal = x_curr
        f_bestLocal = f_curr

print("\nFinal number of solutions checked: ", solutionsChecked)
print("Best value found: ", f_bestLocal[0])
print("Weight is: ", f_bestLocal[1])
print("Total number of items selected: ", np.sum(s_bestLocal))
print("Best solution: ", s_bestLocal)


# ------------------------------------------------
# Question 7-2: Tabu Search
# ------------------------------------------------

# Tabu Search with recency memory (short-term memory)

tabuTanure = 3   # length of the tabu list
itr_max = 100    # maximum number of iteration

x_curr = x_initial
x_best = x_curr[:]
f_curr = evaluate(x_curr)
f_best = f_curr[:]

# create tabu list
tabuList = []

# monitor the number of evaluations made
solutionsChecked = 0

itr = 0
while itr < itr_max:

    Neighborhood = neighborhood(x_curr)
    Xcurr = x_curr[:]

    for s in Neighborhood:
        solutionsChecked = solutionsChecked + 1
        Fcurr = evaluate(Xcurr)
        # apply tabu criterion: accept only if it is not inside tabu list & better solution
        if (s not in tabuList) and (evaluate(s)[0] > Fcurr[0]):
            Xcurr = s[:]

    x_curr = Xcurr[:]

    if evaluate(Xcurr)[0] > f_best[0]:
        x_best = Xcurr[:]
        f_best = evaluate(x_best)

    # if the total number of items in tabu list > maximum allowed number of items,
    # release the solution to feasible region one by one
    tabuList.append(Xcurr)
    if len(tabuList) > tabuTanure:
        tabuList.pop(0)

    itr = itr + 1

print("\nFinal number of solutions checked: ", solutionsChecked)
print("Best value found: ", f_best[0])
print("Weight is: ", f_best[1])
print("Total number of items selected: ", np.sum(x_best))
print("Best solution: ", x_best)




