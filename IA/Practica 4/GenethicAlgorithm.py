__author__ = "David Lopez Hernandez"
__author__ = "Uriel Onofre Resendiz"
__author__ = "Alejandro Escamilla Sánchez"
__name__ = "Practica de laboratorio 4"
__asginatura__ = "Inteligencia Artificial"

import numpy
import math


class GenethicAlgorithm:
    def __init__(self, expression, expect, chromosomes, generations, interval):
        self.Expression = expression
        self.Expect = expect
        self.Chromosomes = chromosomes
        self.Generations = generations
        self.Interval = interval
        self.Population = []
        self.Evaluation = []

    def initialize_generation(self):
        new_population = numpy.random.randint(low=self.Interval[0], high=self.Interval[1], size=self.Chromosomes,
                                              dtype=int)

        seen = set()
        uniq = []
        for x in new_population:
            if x not in seen:
                uniq.append(x)
                seen.add(x)
            else:
                while 1:
                    new_value = self.invalid_case(x)
                    if new_value[0] not in seen:
                        uniq.append(new_value[0])
                        seen.add(new_value[0])
                        break
        print("Population :", uniq)
        self.Population = uniq

    def evaluate_function(self):
        if self.Expression == 1:
            for element in self.Population:
                evaluation = pow(element, 2)
                self.Evaluation.append(evaluation)
        elif self.Expression == 2:
            for element in self.Population:
                evaluation = numpy.sin(element) * 40
                self.Evaluation.append(evaluation)
        elif self.Expression == 3:
            for element in self.Population:
                evaluation = math.cos(element) + element
                self.Evaluation.append(evaluation)
        elif self.Expression == 4:
            for element in self.Population:
                with numpy.errstate(divide='ignore'):
                    x = element
                    if x != 50:
                        evaluation = (1000 / numpy.abs(50 - element)) + element
                    else:
                        while 1:
                            new_value = self.invalid_case(x)
                            if new_value[0] not in self.Population:
                                evaluation = (1000 / numpy.abs(50 - new_value[0])) + new_value[0]
                                break
                    self.Evaluation.append(evaluation)
        elif self.Expression == 5:
            for element in self.Population:
                with numpy.errstate(divide='ignore'):
                    x = element
                    if x != 50 and x != 30 and x != 80:
                        evaluation = (1000 / numpy.abs(30 - element)) + (1000 / numpy.abs(50 - element)) + (
                                1000 / numpy.abs(80 - element)) + element
                    else:
                        while 1:
                            new_value = self.invalid_case(x)
                            if new_value[0] not in self.Population:
                                evaluation = (1000 / numpy.abs(30 - new_value[0])) + (
                                        1000 / numpy.abs(50 - new_value[0])) + (
                                                     1000 / numpy.abs(80 - new_value[0])) + new_value[0]
                                break
                    self.Evaluation.append(evaluation)

        # print("Evaluation :", self.Evaluation)
        # self.select_evaluation()

    def crossing_funtion(self, valid0, valid1, index):
        # print(valid0)
        # print(valid1)
        max_amount_of_bit = len(bin(numpy.max(self.Population))[2:])
        # print(max_amount_of_bit)
        bin_representation_0 = bin(valid0)[2:].zfill(max_amount_of_bit)
        bin_representation_1 = bin(valid1)[2:].zfill(max_amount_of_bit)
        # print("a ", bin_representation_0[:index])
        # print("b ", bin_representation_1[index:])
        # print("a ", bin_representation_0)
        # print("b ", bin_representation_1)
        new_bin_repesentation = bin_representation_0[:index] + bin_representation_1[index:]
        # print("c ", new_bin_repesentation)
        new_value_b = int(new_bin_repesentation, 2)
        while 1:
            new_value = self.invalid_case(new_value_b)
            if new_value[0] not in self.Population:
                break
        return new_value

    def select_evaluation(self):
        # self.Evaluation.sort()
        for x in range(self.Generations):
            print("G" + str(x))
            self.Population = [x for _, x in sorted(zip(self.Evaluation, self.Population))]
            self.Evaluation.sort()
            print("Population: ", self.Population)
            print("Evaluation :", self.Evaluation)
            half = self.Chromosomes / 2
            new_values = []
            first_time = True
            if self.Expect == 1:
                rhalfpo = self.Population[int(half):]
                for x in range(int(half)):
                    if first_time:
                        first_time = False
                        new_values.append(self.crossing_funtion(rhalfpo[x - 1], rhalfpo[x - 2], int(half)))
                    else:
                        first_time = True
                        new_values.append(self.crossing_funtion(rhalfpo[x - 2], rhalfpo[x - 1], int(half)))
                    # print("Nuevo valor: ", new_values)
                del self.Population[:int(half)]
                for new_value in new_values:
                    self.Population.insert(0, new_value[0])
            else:
                lhalfpo = self.Population[:int(half)]
                for x in range(int(half)):
                    if first_time:
                        first_time = False
                        new_values.append(self.crossing_funtion(lhalfpo[x - 1], lhalfpo[x - 2], int(half)))
                    else:
                        first_time = True
                        new_values.append(self.crossing_funtion(lhalfpo[x - 2], lhalfpo[x - 1], int(half)))

                del self.Population[int(half):]
                for new_value in new_values:
                    self.Population.append(new_value[0])

            self.Evaluation.clear()
            self.evaluate_function()
        if self.Expect == 1:
            self.Population = [x for _, x in sorted(zip(self.Evaluation, self.Population))]
            self.Evaluation.sort()
            print("==================Finalizo==================")
            print("Population: ", self.Population)
            print("Evaluation: ", self.Evaluation)
            print("Best Evaluation: ", self.Population[-1], " - ", self.Evaluation[-1])
        else:
            self.Population = [x for _, x in sorted(zip(self.Evaluation, self.Population))]
            self.Evaluation.sort()
            print("==================Finalizo==================")
            print("Population: ", self.Population)
            print("Evaluation: ", self.Evaluation)
            print("Best Evaluation: ", self.Population[0], " - ", self.Evaluation[0])

    @staticmethod
    def modify_bit(v, index, x):
        mask = 1 << index
        return (v & ~mask) | ((x << index) & mask)

    def mutation_function(self, value):
        print(
            "This case apply for mutate")
        max_amount_of_bit = len(bin(numpy.max(self.Population))[2:])
        bin_representation = bin(value)[2:].zfill(max_amount_of_bit)
        random_num = numpy.random.randint(low=0, high=max_amount_of_bit, size=1, dtype=int)
        # print("a", bin_representation)
        # print("b", random_num)
        if bin_representation[int(random_num)] == 1:
            new_value = self.modify_bit(int(bin_representation, 2), random_num, 0)
        else:
            new_value = self.modify_bit(int(bin_representation, 2), random_num, 1)
        # print(new_bin_repesentation)

        return new_value

    def invalid_case(self, value):
        print(
            "This case is not valid for two reasons, divide by zero or is a repeated value, in this case we gonna "
            "apply a generate random function")
        # print("Valor invalido: ", value)
        new_value = numpy.random.randint(low=self.Interval[0], high=self.Interval[1], size=1, dtype=int)
        print("Nuevo valor de un dato invalido: ", new_value)
        return new_value


expression = int(input("Expresion a evaluar con respecto a las 5 opciones disponibles (1-5): "))
expect = int(input("Gusta obtener el maximo o el minimo (1 = max, 0 = min): "))
chromosome = int(input("Numero de choromosomas: "))
generations = int(input("Numero de generaciones: "))
interval = []
for i in range(0, 2):
    if i == 0:
        interval_x = int(input("Limite inferior: "))
        interval.append(interval_x)
    else:
        interval_y = int(input("Limite superior: "))
        interval.append(interval_y)

ga = GenethicAlgorithm(expression=expression, expect=expect, chromosomes=chromosome, generations=generations,
                       interval=interval)
ga.initialize_generation()
ga.evaluate_function()
ga.select_evaluation()
