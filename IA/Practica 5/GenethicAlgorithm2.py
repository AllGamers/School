__author__ = "David Lopez Hernandez"
__author__ = "Uriel Onofre Resendiz"
__author__ = "Alejandro Escamilla Sánchez"
__name__ = "Practica de laboratorio 4"
__asginatura__ = "Inteligencia Artificial"

import numpy

from cffi.backend_ctypes import xrange
from pyeasyga import pyeasyga


def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words


data = readFile("p5.txt")
ga = pyeasyga.GeneticAlgorithm(data, maximise_fitness=True)


def create_individual(data):
    for item in data:
        data_s = item.split(",")
        return [numpy.random.randint(0, int(data_s[2])) for _ in xrange(len(data))]


def create_individual_2(data):
    return [numpy.random.randint(0, 1) for _ in xrange(len(data))]


def fitness(individual, data):
    weight, importance = 0, 0
    type = []
    for (selected, item) in zip(individual, data):
        if selected:
            item_s = item.split(",")
            if int(item_s[2]) > 0:
                weight += int(item_s[0]) * selected
                importance += int(item_s[1]) * selected
                item_s[2] = - selected
                type.append(item_s[3])

    if "Liquid" in type:
        if "Electronic" in type or "Document" in type:
            importance = 0

    if "Food" in type:
        if "Document" in type:
            importance = 0

    if weight > l_weight:
        importance = 0
    return importance


def fitness_2(individual, data):
    weight, importance = 0, 0
    type = []
    for (selected, item) in zip(individual, data):
        if selected:
            item_s = item.split(",")
            if int(item_s[2]) > 0:
                weight += int(item_s[0]) * selected
                importance += int(item_s[1]) * selected
                item_s[2] = - selected
                type.append(item_s[3])

    if weight > l_weight:
        importance = 0
    return importance


l_weight = int(input("Peso maximo que soporta la mochila: "))
l_type = int(input("Posibilidad (0=Sin Existencia, 1=Con Existencia, 2=Tomando en cuenta los tipos): "))
l_chromosome = int(input("Numero de choromosomas: "))
l_generations = int(input("Numero de generaciones: "))

if l_type == 0:
    ga.fitness_function = fitness
    ga.create_individual = create_individual_2
if l_type == 1:
    ga.fitness_function = fitness
    ga.create_individual = create_individual
if l_type == 2:
    ga.fitness_function = fitness_2
    ga.create_individual = create_individual

ga.population_size = l_chromosome
ga.generations = l_generations

ga.run()

for individual in ga.last_generation():
    print(individual)

print("==================Finalizo==================")
print(ga.best_individual())
