# QUESTION 2: (C)

"""---------------------------- library -------------------------"""

import copy
import math
from random import Random
import numpy as np

"""-------------------------- parameters -------------------------"""

seed = 12345
myPRNG = Random(seed)

# number of dimensions of problem
n = 2

# number of particles in swarm
size = 100

# stopping criteria
iteration = 80

# velocity update formula parameters
phi1 = 2
phi2 = 2
vel_limit = 20
pos_limit = 500

inertia_weight = 0.7
constriction = 0.85

# neighbor
neighbor_size = 3

"""-------------------------- functions -------------------------"""


# Schwefel function to evaluate a real-valued solution x
# note: the feasible space is an n-dimensional hypercube centered at the origin with side length = 2 * 500

def evaluate(x):
    val = 0
    d = len(x)
    for i in xrange(d):
        val = val + x[i] * math.sin(math.sqrt(abs(x[i])))
    val = 418.9829 * d - val
    return val


def update_velocity(pos, vel, pBest, gBest):
    gamma1 = myPRNG.uniform(0, 1)
    gamma2 = myPRNG.uniform(0, 1)
    vel_arr = np.array(vel)
    pos_arr = np.array(pos)
    pBest_array = np.array(pBest)
    gBest_array = np.array(gBest)

    new_velocity = inertia_weight * vel_arr + phi1 * gamma1 * (pBest_array - pos_arr) + phi2 * gamma2 * (gBest_array - pos_arr)
    new_velocity = constriction * new_velocity
    return new_velocity.tolist()


def update_position(pos, vel):
    vel_arr = np.array(vel)
    pos_arr = np.array(pos)

    new_position = pos_arr + vel_arr
    new_position = new_position.tolist()
    for j in xrange(n):
        if (new_position[j]) > pos_limit:
            new_position[j] = pos_limit
        elif (new_position[j]) < -pos_limit:
            new_position[j] = -pos_limit
    return new_position


def get_neighbor_index(index):
    neighbor_index = np.zeros(neighbor_size, dtype=np.int)
    if index == 0:
        neighbor_index[0] = size - 1  # the last element in the particles
        neighbor_index[1] = index
        neighbor_index[2] = index + 1
    elif index == (size - 1):
        neighbor_index[0] = index - 1
        neighbor_index[1] = index
        neighbor_index[2] = 0
    else:
        neighbor_index[0] = index - 1
        neighbor_index[1] = index
        neighbor_index[2] = index + 1
    return neighbor_index

"""--------------------------------- variables  -----------------------------------"""

# the swarm will be represented as a list of positions, velocities, values, pbest, and pbest values

pos = [[] for _ in xrange(size)]  # position of particles -- will be a list of lists
vel = [[] for _ in xrange(size)]  # velocity of particles -- will be a list of lists

curValue = []  # value of current position  -- will be a list of real values
pbest = []  # particles' best historical position -- will be a list of lists
pbestVal = []  # value of pbest position  -- will be a list of real values

"""-------------------------- initialize swarm positions  -------------------------"""

# initialize the swarm randomly

for i in xrange(size):
    for j in xrange(n):
        pos[i].append(myPRNG.uniform(-pos_limit, pos_limit))  # assign random value between -500 and 500
        vel[i].append(myPRNG.uniform(-1, 1))  # assign random value between -1 and 1
    curValue.append(evaluate(pos[i]))  # evaluate the current position

pBest = pos[:]  # initialize pbest to the starting position
pBestVal = curValue[:]  # initialize pbest to the starting position


local_best = pBest[:]
local_bestVal = pBestVal[:]


gBest = pos[0]
gBestVal = curValue[0]

"""-------------------------------------- main simulation -------------------------------------"""


done = 0
counter = 0
count = 0

while done == 0:
    # ax = fig.add_subplot(111, projection='3d')
    for i in xrange(size):

        neighbor_index = get_neighbor_index(i)

        for j in neighbor_index:

            curValue[j] = evaluate(pos[j])

            if curValue[j] < pBestVal[j]:  # update pBest

                pBestVal[j] = curValue[j]
                pBest[j] = pos[j][:]

            if pBestVal[j] < local_best[i]:  # update local best
                local_best[i] = pBest[j][:]
                local_bestVal[i] = pBestVal[j]

        if local_bestVal[i] < gBestVal:
            gBest = local_best[i][:]
            gBestVal = local_bestVal[i]

    for i in xrange(size):
        vel[i] = update_velocity(pos[i], vel[i], pBest[i], local_best[i])
        pos[i] = update_position(pos[i], vel[i])

    print("\nIterations: ", count)
    print("Position=", pos)
    print("Velocity=", vel)
    print("Global Best Value", gBestVal)

    count = count + 1
    if count > iteration:
        done = 1

print("\n")
print("--------------------------------- Ring topology results-----------------------------------\n")

print("Dimension:",n )
print("Iterations:", iteration)

print("Swarm size:", size)
print("Inertia inertia_weight:", inertia_weight)
print("Velocity constriction factor:", constriction)

print("Global Best positon:", round(gBest[0],2),round(gBest[1],2))
print("Global Best value:", gBestVal)

