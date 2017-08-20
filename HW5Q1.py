# the intial framework for a real-valued GA
# author: Charles Nicholson
# for ISE/DSA 5113

# need some python libraries
import copy
import math
from random import Random
import numpy as np

# to setup a random number generator, we will specify a "seed" value
seed = 5113
myPRNG = Random(seed)

dimensions = 200  # set dimensions for Schwefel Function search space
lowerBound = -500  # bounds for Schwefel Function search space
upperBound = 500  # bounds for Schwefel Function search space

# you may change anything below this line that you wish too -----------------------------------------------------------------

# Student name(s): Jiwon Jeon and Andrew Rocha
# Date: 05/06/2017


populationSize = 200  # size of GA population
Generations = 500  # number of GA generations

crossOverRate = 0.8
mutationRate = 0.05


# create an continuous valued chromosome
def createChromosome(d, lBnd, uBnd):
    x = []
    for i in range(d):
        x.append(myPRNG.uniform(lBnd, uBnd))  # creating a randomly located solution

    return x


# create initial population
def initializePopulation():  # n is size of population; d is dimensions of chromosome
    population = []
    populationFitness = []

    for i in range(populationSize):
        population.append(createChromosome(dimensions, lowerBound, upperBound))
        populationFitness.append(evaluate(population[i]))

    tempZip = zip(population, populationFitness)
    popVals = sorted(tempZip, key=lambda tempZip: tempZip[1])

    # the return object is a sorted list of tuples:
    # the first element of the tuple is the chromosome; the second element is the fitness value
    # for example:  popVals[0] is represents the best individual in the population
    # popVals[0] for a 2D problem might be  ([-70.2, 426.1], 483.3)  -- chromosome is the list [-70.2, 426.1] and the fitness is 483.3

    return popVals


# implement a linear crossover
def crossover(x1, x2):
    d = len(x1)  # dimensions of solution

    # choose crossover point

    # we will choose the smaller of the two [0:crossOverPt] and [crossOverPt:d] to be unchanged
    # the other portion be linear combo of the parents

    crossOverPt = myPRNG.randint(1, d - 1)  # notice I choose the crossover point so that at least 1 element of parent is copied

    beta = myPRNG.random()  # random number between 0 and 1

    # note: using numpy allows us to treat the lists as vectors
    # here we create the linear combination of the solutions
    new1 = list(np.array(x1) - beta * (np.array(x1) - np.array(x2)))
    new2 = list(np.array(x2) + beta * (np.array(x1) - np.array(x2)))

    # the crossover is then performed between the original solutions "x1" and "x2" and the "new1" and "new2" solutions
    if crossOverPt < d / 2:
        offspring1 = x1[0:crossOverPt] + new1[crossOverPt:d]  # note the "+" operator concatenates lists
        offspring2 = x2[0:crossOverPt] + new2[crossOverPt:d]
    else:
        offspring1 = new1[0:crossOverPt] + x1[crossOverPt:d]
        offspring2 = new2[0:crossOverPt] + x2[crossOverPt:d]

    return offspring1, offspring2  # two offspring are returned


# function to evaluate the Schwefel Function for d dimensions
def evaluate(x):
    val = 0
    d = len(x)
    for i in range(d):
        val = val + x[i] * math.sin(math.sqrt(abs(x[i])))

    val = 418.9829 * d - val

    return val


# function to provide the rank order of fitness values in a list
# not currently used in the algorithm, but provided in case you want to...
def rankOrder(anyList):
    rankOrdered = [0] * len(anyList)
    for i, x in enumerate(sorted(range(len(anyList)), key=lambda y: anyList[y])):
        rankOrdered[x] = i

    return rankOrdered


# performs tournament selection; k chromosomes are selected (with repeats allowed) and the best advances to the mating pool
# function returns the mating pool with size equal to the initial population
def tournamentSelection(pop, k):
    # randomly select k chromosomes; the best joins the mating pool
    matingPool = []

    while len(matingPool) < populationSize:
        ids = [myPRNG.randint(0, populationSize - 1) for i in range(k)]
        competingIndividuals = [pop[i][1] for i in ids]
        bestID = ids[competingIndividuals.index(min(competingIndividuals))]
        matingPool.append(pop[bestID][0])

    return matingPool


# function to mutate solutions (Random Mutation Operator)
def mutate(x):
    # choose mutate point
    mutationPt = myPRNG.randint(0, dimensions - 1)

    # change the values at the mutation point
    x[mutationPt] = myPRNG.uniform(lowerBound, upperBound)

    # variate the value at the mutation point
    # variation = myPRNG.randint(-10,10)
    # x[mutationPt] += variation

    return x


# another mutation function (Gaussian Mutation Operator)
def mutate2(x):
    mu, sigma = 0, 0.01  # mean and standard deviation
    variation = np.random.normal(mu, sigma, dimensions)
    list = []
    for i in range(0, dimensions - 1):
        list.append(myPRNG.randint(0, dimensions - 1))

    for j in range(0, dimensions - 1):
        x[myPRNG.randint(0, dimensions - 1)] = x[myPRNG.randint(0, dimensions - 1)] + sigma * variation[myPRNG.randint(0, dimensions - 1)]

    return x


def breeding(matingPool):
    # the parents will be the first two individuals, then next two, then next two and so on
    # this process is to construct new generation population from the previous generation
    # upon crossover rate, the parents from the previous generation may be included

    children = []
    childrenFitness = []
    for i in range(0, populationSize - 1, 2):

        # cross over the parents to offsprings with a certain crossover rate
        pCO = myPRNG.random()  # random number between 0 and 1 for a crossover probability

        if pCO < crossOverRate:
            child1, child2 = crossover(matingPool[i], matingPool[i + 1])

        else:
            child1, child2 = matingPool[i], matingPool[i + 1]

        # mutate the offsprings(together with parents) with a certain mutation rate
        pMT = myPRNG.random()  # random number between 0 and 1 for a mutation probability

        if pMT < mutationRate:
            child1 = mutate2(child1)
            child2 = mutate2(child2)

        children.append(child1)
        children.append(child2)

        childrenFitness.append(evaluate(child1))
        childrenFitness.append(evaluate(child2))

    tempZip = zip(children, childrenFitness)
    popVals = sorted(tempZip, key=lambda tempZip: tempZip[1])

    # the return object is a sorted list of tuples:
    # the first element of the tuple is the chromosome; the second element is the fitness value
    # for example:  popVals[0] is represents the best individual in the population
    # popVals[0] for a 2D problem might be  ([-70.2, 426.1], 483.3)  -- chromosome is the list [-70.2, 426.1] and the fitness is 483.3

    return popVals


# insertion step
def insert(pop, kids):
    # replacing the previous generation completely...  probably a bad idea -- please implement some type of elitism

    # combine the old generation and new generation
    combine = pop + kids
    # another way to combine...
    # combine = []
    # combine.extend(pop)
    # combine.extend(kids)

    # sort the combined population with the ascending order of fitness value, then select the best(least) fitness values
    combineVals = sorted(combine, key=lambda combine: combine[1])
    newPop = combineVals[0:populationSize]

    return newPop


# perform a simple summary on the population: returns the best chromosome fitness, the average population fitness, and the variance of the population fitness
def summaryFitness(pop):
    a = np.array(list(zip(*pop))[1])
    return np.min(a), np.mean(a), np.var(a), np.std(a)


# the best solution should always be the first element... if I coded everything correctly...
def bestSolutionInPopulation(pop):
    print(pop[0])


# optional: you can output results to a file
f = open('out.txt', 'w')

# GA main code
Population = initializePopulation()

for j in range(Generations):
    mates = tournamentSelection(Population, 3)
    Offspring = breeding(mates)
    Population = insert(Population, Offspring)

    minVal, meanVal, varVal, stdVal = summaryFitness(Population)
    f.write(str(minVal) + " " + str(meanVal) + " " + str(varVal) + " " + str(stdVal) + "\n")

f.close()

print(summaryFitness(Population))
bestSolutionInPopulation(Population)

print(Population)

