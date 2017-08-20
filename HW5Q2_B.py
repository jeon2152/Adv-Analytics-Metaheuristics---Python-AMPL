# QUESTION 2: Particle Swarm Optimization Implementation
# (B)

"""---------------------------- library -------------------------"""

import copy
import math
from random import Random
import numpy as np


"""-------------------------- parameters -------------------------"""

seed = 12345
myPRNG = Random(seed)

# number of dimension
n = 2

# number of particles in swarm
size = 5

iteration = 3 # stopping criteria


# velocity update formula parameters
phi1 = 2
phi2 = 2
vel_limit = 10 # limits on particle velocity
pos_limit = 500 # limits on particle position


inertia_weight = 1
constriction = 1

"""-------------------------- functions -------------------------"""

# Schwefel function to evaluate a real-valued solution x
# note: the feasible space is an n-dimensional hypercube centered at the origin with side length = 2 * 500

def evaluate(x):
      val = 0
      d = len(x)
      for i in xrange(d):
            val = val + x[i]*math.sin(math.sqrt(abs(x[i])))
      val = 418.9829*d - val
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


"""--------------------------------- variables  -----------------------------------"""

# the swarm will be represented as a list of positions, velocities, values, pbest, and pbest values

pos = [[] for _ in xrange(size)]      #position of particles -- will be a list of lists
vel = [[] for _ in xrange(size)]      #velocity of particles -- will be a list of lists

curValue = [] #value of current position  -- will be a list of real values
pbest = []    #particles' best historical position -- will be a list of lists
pbestVal = [] #value of pbest position  -- will be a list of real values


"""-------------------------- initialize swarm positions  -------------------------"""


# initialize the swarm randomly

for i in xrange(size):
      for j in xrange(n):
            pos[i].append(myPRNG.uniform(-pos_limit,pos_limit))    #assign random value between -500 and 500
            vel[i].append(myPRNG.uniform(-1,1))        #assign random value between -1 and 1
      curValue.append(evaluate(pos[i]))   #evaluate the current position

pBest = pos[:]  # initialize pbest to the starting position
pBestVal = curValue[:]  # initialize pbest to the starting position

gBest = pos[0]
gBestVal = curValue[0]


"""-------------------------------------- main -------------------------------------"""

positions = []
velocities = []
evaluations = []

done = 0
counter = 0

while done == 0:
      for i in xrange(size):
            curValue[i] = evaluate(pos[i])
            if curValue[i] < pBestVal[i]:
                  pBestVal[i] = curValue[i]
                  pBest[i] = pos[i][:]
            if pBestVal[i] < gBestVal:
                  gBest = pBest[i][:]
                  gBestVal = pBestVal[i]
      for i in xrange(size):
            vel[i] = update_velocity(pos[i], vel[i], pBest[i], gBest)
            pos[i] = update_position(pos[i], vel[i])
            positions.append(pos[i])
            velocities.append(vel[i])
            evaluations.append(evaluate(pos[i]))
      counter = counter + 1
      if counter > iteration:
            done = 1


print("\n")
print("--------------------------------- 2D Schwefel problem solutions -----------------------------------\n")

print("Dimension:",n )
print("Iterations:", iteration)

print("Swarm size:", size)
print("Inertia weight:", inertia_weight)
print("Velocity constriction factor:", constriction)

print("Global Best positon:", round(gBest[0],2),round(gBest[1],2))
print("Global Best value:", gBestVal)

