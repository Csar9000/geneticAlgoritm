import math
import random
import numpy as np
import matplotlib.pyplot as plt

signsCount = 100

def rounding(value, r=2):
    return round(value, r)


def targetFunction():
    x0 = []
    y0 = []
    for i in range(signsCount):
        x0.append(i / 10)
        y0.append(rounding(np.sin(2 * x0[i])))
    targetFunctionT = [x0, y0]
    return targetFunctionT


targetFunction = targetFunction()
minValue = np.min(targetFunction)
maxValue = np.max(targetFunction)


def startPopulation(amount):
    population = []
    for i in range(amount):
        pop = []
        for i in range(signsCount):
            pop.append(rounding(random.uniform(minValue, maxValue)))
        population.append(pop)
    return population


def onePointKrossingover(Parent1, Parent2):
    point = random.randint(1, 98)
    child1 = []
    child2 = []
    for i in range(len(Parent1)):
        if (i < point):
            child1.append(Parent1[i])
            child2.append(Parent2[i])
        else:
            child1.append(Parent2[i])
            child2.append(Parent1[i])
    childs = [child1, child2]
    return childs


def getIntRandomArray(countOfElements):
    randomArray = []
    for i in range(countOfElements):
        randomArray.append(int(random.random() * ((signsCount - 0) + 1)) + 0)
    return randomArray


def crossoverByThreePoints(parent1, parent2):
    countOfSigns = signsCount
    countOfSigns = int(countOfSigns)
    points = getIntRandomArray(3)

    leftPoint = points[0]
    rightPoint = points[0]
    midPoint = points[0]

    for i in range(len(points)):
        if points[i] <= leftPoint:
            leftPoint = points[i]
        elif points[i] >= rightPoint:
            rightPoint = points[i]
        else:
            midPoint = points[i]

    child1 = []
    child2 = []

    # print(f"{leftPoint}   {rightPoint}    {midPoint}")
    for p in range(leftPoint):
        # print(f"{len(parent2.signs)}  {len(parent2.signs)}")
        child1.append(parent1[p])
        child2.append(parent2[p])

    for p in range(leftPoint, midPoint):
        child1.append(parent2[p])
        child2.append(parent1[p])

    for p in range(midPoint, rightPoint):
        child1.append(parent1[p])
        child2.append(parent2[p])

    for p in range(rightPoint, countOfSigns):
        child1.append(parent2[p])
        child2.append(parent1[p])

    individiduals = [child1, child2]
    # print(f"Three  {len(individiduals[0])}")
    return individiduals

def individualEuclideanDistance(ind):
    euclDist = 0
    for j in range(signsCount):
        euclDist += abs(targetFunction[1][j] - ind[j])
    return euclDist


def populationEuclideanDistance(population):
    euclDist = 0
    for i in range(len(population)):
        euclDist += individualEuclideanDistance(population[i])
    return euclDist


def reproduction(population):
    random.shuffle(population)
    for i in range(0, len(population), 2):

        newIndividuals = crossoverByThreePoints(population[i], population[i + 1])

        if evk_dist > 10:
            chance = random.randint(0, 3)
            if chance == 0:
                ind = random.randint(0, 1)
                mutant = mutationSwitchSigns(newIndividuals[ind])
                newIndividuals[ind] = mutant
            if chance == 1:
                ind = random.randint(0, 1)
                mutant = mutationGetNewGen(newIndividuals[ind])
                newIndividuals[ind] = mutant
        else:
            ind = random.randint(0, 1)
            mutant = mutationGetGenForSmallSigns(newIndividuals[ind])
            newIndividuals[ind] = mutant

        population.append(newIndividuals[0])
        population.append(newIndividuals[1])

    return population


def mutationSwitchSigns(child):
    genInd1 = random.randint(0, 99)
    genInd2 = random.randint(0, 99)

    gen1 = child[genInd1]
    gen2 = child[genInd2]
    # gen3 = Child[genInd3];
    child[genInd1] = gen2
    child[genInd2] = gen1

    #child[random.randint(1, 30):random.randint(30, 99):].reverse()
    return child


def mutationGetNewGen(child):
    genInd = random.randint(0, 99)
    gen = rounding(random.uniform(minValue, maxValue))
    child[genInd] = gen
    return child

def mutationGetGenForSmallSigns(child):
    genInd = random.randint(0, 99)
    gen = rounding(random.uniform(-0.999, 0.999))
    child[genInd] = gen
    return child

def selection(population):
    euclDist = []
    for i in range(len(population)):
        euclDist.append(individualEuclideanDistance(population[i]));

    for i in range(20):
        maxInd = np.argmax(euclDist)
        population.remove(population[maxInd])
        euclDist.remove(euclDist[maxInd])
    return population


population = startPopulation(20)

evk_dist = populationEuclideanDistance(population)


#print(ED)
count = 0
while evk_dist > 0.5:
    population = reproduction(population)
    population = selection(population)
    evk_dist = populationEuclideanDistance(population)
    EDTest = evk_dist
    print(f"{evk_dist} | iter {count}")
    count += 1

euclDist = []
for i in range(len(population)):
    euclDist.append(individualEuclideanDistance(population[i]))
theBest = []
for i in range(20):
    minInd = np.argmin(euclDist)
    theBest = population[minInd]

figure, axis = plt.subplots(2, 1)
axis[0].scatter(targetFunction[0], targetFunction[1], color="green")
axis[1].scatter(targetFunction[0], theBest, color="red")

plt.show()


