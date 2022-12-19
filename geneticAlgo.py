import string
import pandas as pd
import numpy as np
import random

def generatePopulation(choromosomeLen: int, populationSize: int):
    population = []
    for i in range(populationSize):
        choromosome = [random.randint(0,1) for i in range(choromosomeLen)]
        population.append(choromosome)
        
    return population

def crossover(population, populationSize):
    newPopulation = []
    if populationSize % 2 == 1:
        residual = population.pop(1)
        newPopulation.append(residual)

    it = iter(population)
    for gene in it:
        nextGene = next(it)
        i = random.randint(0,len(population))
        newGene = gene[0:i] + nextGene[i::]
        newGene2 = nextGene[0:i] + gene[i::]
        newPopulation.extend([newGene, newGene2])

    return newPopulation

def mutation(population, prob): 
    for i in range(len(population)):
        choromosome = population[i]
        mutationProb = random.uniform(0, 1)
        if mutationProb < prob:
            mutatedGene = random.randint(0,len(choromosome)-1)
            choromosome[mutatedGene] = 1 - choromosome[mutatedGene]
            population[i] = choromosome

    return population

def fitnessFunc(values, weights, population, weightLimit):
    fitnessScores = []
    for sol in population:
        score = np.dot(values, sol)    
        totalWeight = np.dot(weights, sol)
        if totalWeight > weightLimit:
            fitnessScores.append(0)
        else:
            fitnessScores.append(score)

    return fitnessScores

def geneticAlgo(fileName: string, weightLimit, populationSize, time):

    data = pd.read_excel(fileName)

    values = list(data['Values'])
    weights = list(data['Weights'])

    #1-initial population
    population = generatePopulation(len(values), populationSize)

    for i in range(time):
        #2-fitness function
        fitnessScores = fitnessFunc(values, weights, population, weightLimit)
        try:
            fitnessWeights = list(map(lambda x: x/sum(fitnessScores), fitnessScores))
        except ZeroDivisionError:
            print("Could not find the solution")
            return 0, []

        #3-selection 
        choosenPopulation = []
        for i in range(populationSize):
            choosenGene = random.choices(population=population,weights=fitnessWeights)
            choosenPopulation.append(choosenGene[0])

        #4-crossover
        population = crossover(choosenPopulation, populationSize)

        #5-mutation
        prob = 0.3
        population = mutation(population, prob)

    fitnessScores = fitnessFunc(values, weights, population, weightLimit)
    highestFitScore = max(fitnessScores)
    highestFitIndex = fitnessScores.index(highestFitScore)
    
    return highestFitScore, population[highestFitIndex]

if __name__ == "__main__":

    while True:
        try:
            weightLimit = int(input("What is the maximum weight that your bag can take? \n"))
            populationSize = int(input("What is your desired population size? (ex:10) \n"))
            time = int(input("How many cycles you want to wait? \n"))
            break
        except ValueError:
            print("Your answers must be numeric!")

    fileName = "knapsack.xlsx"

    score, solution = geneticAlgo(fileName, weightLimit, populationSize, time)

    if score == 0:
        print("Algorithm could not found the solution.")
    else:
        print("The solution is: {} by the score of {}".format(solution,score))