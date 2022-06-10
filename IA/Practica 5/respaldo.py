import random
import sys
import operator


class Knapsack(object):

    # initialize variables and lists
    def __init__(self):

        self.C = 0
        self.weights = []
        self.profits = []
        self.opt = []
        self.parents = []
        self.newparents = []
        self.bests = []
        self.best_p = []
        self.iterated = 1
        self.population = 0

        # increase max recursion for long stack
        iMaxStackSize = 15000
        sys.setrecursionlimit(iMaxStackSize)

    # create the initial population
    def initialize(self):

        for i in range(self.population):
            parent = []
            for k in range(0, 5):
                k = random.randint(0, 1)
                parent.append(k)
            self.parents.append(parent)

    # set the details of this problem
    def properties(self, weights, profits, opt, C, population):

        self.weights = weights
        self.profits = profits
        self.opt = opt
        self.C = C
        self.population = population
        self.initialize()

    # calculate the fitness function of each list (sack)
    def fitness(self, item):

        sum_w = 0
        sum_p = 0

        # get weights and profits
        for index, i in enumerate(item):
            if i == 0:
                continue
            else:
                sum_w += self.weights[index]
                sum_p += self.profits[index]

        # if greater than the optimal return -1 or the number otherwise
        if sum_w > self.C:
            return -1
        else:
            return sum_p

    # run generations of GA
    def evaluation(self):

        # loop through parents and calculate fitness
        best_pop = self.population // 2
        for i in range(len(self.parents)):
            parent = self.parents[i]
            ft = self.fitness(parent)
            self.bests.append((ft, parent))

        # sort the fitness list by fitness
        self.bests.sort(key=operator.itemgetter(0), reverse=True)
        self.best_p = self.bests[:best_pop]
        self.best_p = [x[1] for x in self.best_p]

    # mutate children after certain condition
    def mutation(self, ch):

        for i in range(len(ch)):
            k = random.uniform(0, 1)
            if k > 0.5:
                # if random float number greater that 0.5 flip 0 with 1 and vice versa
                if ch[i] == 1:
                    ch[i] = 0
                else:
                    ch[i] = 1
        return ch

    # crossover two parents to produce two children by miixing them under random ration each time
    def crossover(self, ch1, ch2):

        threshold = random.randint(1, len(ch1) - 1)
        tmp1 = ch1[threshold:]
        tmp2 = ch2[threshold:]
        ch1 = ch1[:threshold]
        ch2 = ch2[:threshold]
        ch1.extend(tmp2)
        ch2.extend(tmp1)

        return ch1, ch2

    # run the GA algorithm
    def run(self):

        # run the evaluation once
        self.evaluation()
        newparents = []
        pop = len(self.best_p) - 1

        # create a list with unique random integers
        sample = random.sample(range(pop), pop)
        for i in range(0, pop):
            # select the random index of best children to randomize the process
            if i < pop - 1:
                r1 = self.best_p[i]
                r2 = self.best_p[i + 1]
                nchild1, nchild2 = self.crossover(r1, r2)
                newparents.append(nchild1)
                newparents.append(nchild2)
            else:
                r1 = self.best_p[i]
                r2 = self.best_p[0]
                nchild1, nchild2 = self.crossover(r1, r2)
                newparents.append(nchild1)
                newparents.append(nchild2)

        # mutate the new children and potential parents to ensure global optima found
        for i in range(len(newparents)):
            newparents[i] = self.mutation(newparents[i])

        if self.opt in newparents:
            print("optimal found in {} generations".format(self.iterated))
        else:
            self.iterated += 1
            print("recreate generations for {} time".format(self.iterated))
            self.parents = newparents
            self.bests = []
            self.best_p = []
            self.run()


# properties for this particular problem
weights = [12, 7, 11, 8, 9]
profits = [24, 13, 23, 15, 16]
opt = [0, 1, 1, 1, 0]
C = 26
population = 10

k = Knapsack()
k.properties(weights, profits, opt, C, population)
k.run()

"""__author__ = "David Lopez Hernandez"
__author__ = "Uriel Onofre Resendiz"
__author__ = "Alejandro Escamilla Sánchez"
__name__ = "Practica de laboratorio 4"
__asginatura__ = "Inteligencia Artificial"

from pyeasyga import pyeasyga

data = [(741, 1, 100), (1632, 1, 132), (845, 0.5, 123), (522, 0.7, 121),
        (112, 0.7, 150), (1022, 0.9, 122), (1732, 0.8, 119), (1165, 0.7, 200),
        (119, 1, 111), (215, 2, 208), (976, 0.6, 100), (1438, 0.7, 312),
        (910, 0.5, 208), (106, 0.8, 141), (1523, 0.7, 101), (211, 0.8, 100)]

ga = pyeasyga.GeneticAlgorithm(data)
ga.population_size = 10


def fitness(individual, data):
    weight, volume, price = 0, 0, 0
    for (selected, item) in zip(individual, data):
        if selected:
            weight += item[0]
            volume += item[1]
            price += item[2]
    if weight > 10000 or volume > 10:
        price = 0
    return price


ga.fitness_function = fitness
ga.run()
for individual in ga.last_generation():
    print(individual)
print(ga.best_individual())"""

"""
# For the crossover function, supply two individuals (i.e. candidate
# solution representations) as parameters,
def crossover(parent_1, parent_2):
    crossover_index = random.randrange(1, len(parent_1))
    child_1 = parent_1[:index] + parent_2[index:]
    child_2 = parent_2[:index] + parent_1[index:]
    return child_1, child_2

# and set the Genetic Algorithm's ``crossover_function`` attribute to
# your defined function
ga.crossover_function = crossover


# For the mutate function, supply one individual (i.e. a candidate
# solution representation) as a parameter,
def mutate(individual):
    mutate_index = random.randrange(len(individual))
    if individual[mutate_index] == 0:
        individual[mutate_index] = 1
    else:
        individual[mutate_index] = 0

# and set the Genetic Algorithm's ``mutate_function`` attribute to
# your defined function
ga.mutate_function = mutate
"""
