__author__ = "David Lopez Hernandez"
__author__ = "Uriel Onofre Resendiz"
__author__ = "Alejandro Escamilla Sánchez"
__name__ = "Practica de laboratorio 2"
__asginatura__ = "Inteligencia Artificial"

from typing import Dict
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import enum
import array as arr


class MovsTerrainCosts:
    def __init__(self, agent):
        self.movsCost = arr.array('i', 7 * [0])
        if agent == TypeAgent.humano:
            self.movsCost[int(Terrain.Mountain.value)] = 0
            self.movsCost[int(Terrain.Land.value)] = 1
            self.movsCost[int(Terrain.Water.value)] = 2
            self.movsCost[int(Terrain.Sand.value)] = 3
            self.movsCost[int(Terrain.Forest.value)] = 4
            self.movsCost[int(Terrain.Swamp.value)] = 5
            self.movsCost[int(Terrain.Snow.value)] = 5
        elif agent == TypeAgent.mono:
            self.movsCost[int(Terrain.Mountain.value)] = 0
            self.movsCost[int(Terrain.Land.value)] = 2
            self.movsCost[int(Terrain.Water.value)] = 4
            self.movsCost[int(Terrain.Sand.value)] = 3
            self.movsCost[int(Terrain.Forest.value)] = 1
            self.movsCost[int(Terrain.Swamp.value)] = 5
            self.movsCost[int(Terrain.Snow.value)] = 0
        elif agent == TypeAgent.pulpo:
            self.movsCost[int(Terrain.Mountain.value)] = 0
            self.movsCost[int(Terrain.Land.value)] = 2
            self.movsCost[int(Terrain.Water.value)] = 1
            self.movsCost[int(Terrain.Sand.value)] = 0
            self.movsCost[int(Terrain.Forest.value)] = 3
            self.movsCost[int(Terrain.Swamp.value)] = 2
            self.movsCost[int(Terrain.Snow.value)] = 0
        elif agent == TypeAgent.sasquatch:
            self.movsCost[int(Terrain.Mountain.value)] = 15
            self.movsCost[int(Terrain.Land.value)] = 4
            self.movsCost[int(Terrain.Water.value)] = 0
            self.movsCost[int(Terrain.Sand.value)] = 0
            self.movsCost[int(Terrain.Forest.value)] = 4
            self.movsCost[int(Terrain.Swamp.value)] = 5
            self.movsCost[int(Terrain.Snow.value)] = 3


class Terrain(enum.Enum):
    Mountain = 0  # 128,128,128
    Land = 1  # 250,191,143
    Water = 2  # 0,175,255
    Sand = 3  # 255,192,0
    Forest = 4  # 150,210,80
    Swamp = 5  # 178,162,198
    Snow = 6  # 242,242,242


class Mov(enum.Enum):
    Left = 0
    Right = 1
    Up = 2
    Down = 3
    UpLeft = 4
    UpRight = 5
    DownLeft = 6
    DownRight = 7


class TypeAgent(enum.Enum):
    humano = 0
    mono = 1
    pulpo = 2
    sasquatch = 3


class Stage:
    # cells hide

    def __init__(self, textPlain):
        self.stage = [[int(x) for x in word.split(",")] for word in textPlain]
        self.stageLetras = [["" for x in word.split(",")] for word in textPlain]
        self.cellsHide = []

    def addStageLetras(self, x, y, text):
        if not self.stageLetras[x][y].__contains__(text):
            indiceSalto = self.stageLetras[x][y].rfind('\n')
            if indiceSalto == -1:
                indiceSalto = 0
            if len(self.stageLetras[x][y][indiceSalto:]+text) > 10:
                self.stageLetras[x][y] += "\n"
            self.stageLetras[x][y] += str(text + ",")

    def addCellsHide(self, number, letter):
        if not self.cellsHide.__contains__((number, letter)):
            self.cellsHide.append((number, letter))

    def existsInCellsHide(self, Coords):
        if self.cellsHide.__contains__(giveNumLetter(Coords)):
            return True
        return False

    def hideAllStage(self):
        for x, xcontain in enumerate(self.stage):
            for y, ycontain in enumerate(xcontain):
                self.addCellsHide(giveNumLetter((x, y))[0], giveNumLetter((x, y))[1])

    def unHide(self, Coords=None, num=None, letter=None):  # remove de cellsHide
        if Coords == None:
            if self.existsInCellsHide(giveCords(num, letter)):
                self.cellsHide.remove((num, letter))
        else:
            if self.existsInCellsHide(Coords):
                self.cellsHide.remove(giveNumLetter(Coords))

    def printStage(self):
        for x in self.stage:
            for y in x:
                print(y, end=" ")
            print()

    def printStageLetter(self):
        print("Stage")
        for x in self.stageLetras:
            for y in x:
                print(f"[{y:<8}]", end=' ')
            print()

    def cellInfo(self, Coords=None, num=None, letter=None):
        if Coords != None:
            return Terrain(self.stage[Coords[0]][Coords[1]])
        else:
            Coords = giveCords((num, letter))
            return Terrain(self.stage[Coords[0]][Coords[1]])

    def changeTerrain(self, num, letter, terrain):
        self.stage[num - 1][ord(letter) - 65] = terrain.value

    def stageToImage(self, path):
        colors = [
            [128, 128, 128],
            [250, 191, 143],
            [0, 175, 255],
            [255, 192, 0],
            [150, 210, 80],
            [178, 162, 198],
            [242, 242, 242],
        ]
        w, h = 750, 750
        wf, hf = w / len(self.stage), h / len(self.stage)
        data = np.zeros((h + 50, w + 50, 3), dtype=np.uint8)
        # data = np.zeros((h , w, 3), dtype=np.uint8)
        for countx, frameX in enumerate(self.stage):
            for county, frameY in enumerate(frameX):
                for countc, color in enumerate(colors):
                    if int(frameY) == countc:
                        if self.existsInCellsHide((countx, county)):
                            data[countx * int(wf):(countx + 1) * int(wf),
                            county * int(hf):(county + 1) * int(hf)] = [0, 0, 0]
                        else:
                            data[countx * int(wf):(countx + 1) * int(wf),
                            county * int(hf):(county + 1) * int(hf)] = color

                        if (countx == 14):
                            data[(countx + 1) * int(wf):(countx + 2) * int(wf),
                            (county) * int(hf):(county + 1) * int(hf)] = [213, 213, 213]
                        if (county == 14):
                            data[(countx) * int(wf):(countx + 1 + 1) * int(wf),
                            (county + 1) * int(hf):(county + 1 + 1) * int(hf)] = [213, 213, 213]

                        # cuadrado
                        if countx > 0 or countx < 750 and county > 0 or county < 750:
                            data[countx * int(wf):(countx + 1) * int(wf), county * int(hf)] = [0, 0, 0]  # izquierda
                            data[countx * int(wf), county * int(hf):(county + 1) * int(hf)] = [0, 0, 0]  # abajo
                        break
        self.optionsStage = self.stageLetras
        img = Image.fromarray(data, 'RGB')
        img.save(path + '.png')
        # Reopen
        my_image = Image.open(path + '.png')
        image_editable = ImageDraw.Draw(my_image)
        title_font = ImageFont.truetype("LibsGameV3/Roboto/Roboto-Light.ttf", 12)
        # title_font = ImageFont.truetype("Roboto/Roboto-Light.ttf", 13)
        for countx, frameX in enumerate(self.stageLetras):
            for county, frameY in enumerate(frameX):
                if countx == 14:
                    image_editable.text((county * wf, int(hf) * (countx + 1)),
                                        "\n" + str(county), (0, 0, 0),
                                        font=title_font)
                if county == 14:
                    image_editable.text(((county + 1) * wf, int(hf) * (countx)),
                                        str(countx), (0, 0, 0),
                                        font=title_font)
                if len(frameY) > 0:
                    image_editable.text((county * wf, int(hf) * countx),
                                        self.stageLetras[countx][county], (0, 0, 0),
                                        font=title_font)
        my_image.save(path + ".png")
        # img.show()


class Movement:
    def __init__(self, initialCoords, FinalCords, Hide):
        self.Hide = Hide
        self.InitialCords = giveCords(initialCoords)
        self.ActualCords = giveCords(initialCoords)
        self.FinalCords = giveCords(FinalCords)
        if self.Hide:
            self.hideAllStage()
        self.stageToImage(self.Name)

    def upCord(self, coords=None):
        if coords is None:
            return self.ActualCords[0] - 1, self.ActualCords[1]
        else:
            return coords[0] - 1, coords[1]

    def downCord(self, coords=None):
        if coords is None:
            return self.ActualCords[0] + 1, self.ActualCords[1]
        else:
            return coords[0] + 1, coords[1]

    def leftCord(self, coords=None):
        if coords is None:
            return self.ActualCords[0], self.ActualCords[1] - 1
        else:
            return coords[0], coords[1] - 1

    def rightCord(self, coords=None):
        if coords is None:
            return self.ActualCords[0], self.ActualCords[1] + 1
        else:
            return coords[0], coords[1] + 1


class Agent(MovsTerrainCosts, Stage, Movement):  # Create the class Agent

    def __init__(self, Name, typeAgent, initialCoords, FinalCords, PreFinalCords, stageText,
                 Hide=False, ):
        global a
        self.Name = Name
        self.TypeAgent = typeAgent
        # Memory
        self.memoryCells = []
        self.cost = 0

        MovsTerrainCosts.__init__(self, agent=typeAgent)
        Stage.__init__(self, textPlain=stageText)
        if not self.isValidPosition(giveCords(initialCoords)):
            print(f"Error con Cordenadas iniciales")
            exit()
        elif not self.isValidPosition(giveCords(FinalCords)):
            print(f"Error con Cordenadas finales")
            exit()
        else:
            Movement.__init__(self, initialCoords=initialCoords, FinalCords=FinalCords, Hide=Hide)
            self.addStageLetras(self.InitialCords[0], self.InitialCords[1], " I")
            self.addStageLetras(self.FinalCords[0], self.FinalCords[1], " F")

            for x, preFinal in enumerate(PreFinalCords):
                if not self.isValidPosition(giveCords(preFinal)):
                    print(f"Error con Cordenadas de elementos extras")
                    exit()
                else:
                    tmp = giveCords(preFinal)
                    self.addStageLetras(tmp[0], tmp[1], "F" + str(x))
                    self.PreFinalCords = PreFinalCords

    def proyect(self):
        print(f"Agente:{self.Name}")
        arrayResults = []
        for i, pre in enumerate(self.PreFinalCords):
            memory, cost, lastCoord = self.aStart(self.InitialCords, giveCords(pre), str(i)+'-0')
            self.memoryCells += memory
            arrayResults.append(cost)
            memory, cost, lastCoord = self.aStart(lastCoord, self.FinalCords, str(i)+'-1')
            self.memoryCells += memory
            arrayResults.append(cost)
        return arrayResults

    ######################
    # scans and returns f (x), cost
    def scanCostAndEvaluation(self, coords, finalCords):
        distance = distanceManhatan(coords, finalCords)
        if not self.isValidPosition(coords):
            cost = None
        else:
            cost = self.giveCost(coords)
        if cost is None:
            return None, None
        if cost == 0:
            self.unHide(Coords=coords)
            self.addStageLetras(coords[0], coords[1], f"N/A")
            return None, None
        self.unHide(Coords=coords)
        self.addStageLetras(coords[0], coords[1], f"{distance + cost}")
        return distance + cost, cost

    # Explore position to the UP , LEFT , RIGHT AND DOWN and return valid roads and costs
    def explorePosition(self, memory, coords, finalCords):
        scanned = []
        costs = []
        #################################################################################
        x, cost = self.scanCostAndEvaluation(self.upCord(coords), finalCords)
        if not x is None and not cost is None and not self.existInMemory(memory, self.upCord(coords)):
            scanned.append((x, self.upCord(coords)))
            costs.append(cost)
        #################################################################################
        x, cost = self.scanCostAndEvaluation(self.downCord(coords), finalCords)
        if not x is None and not cost is None and not self.existInMemory(memory, self.downCord(coords)):
            scanned.append((x, self.downCord(coords)))
            costs.append(cost)
        #################################################################################
        x, cost = self.scanCostAndEvaluation(self.leftCord(coords), finalCords)
        if not x is None and not cost is None and not self.existInMemory(memory, self.leftCord(coords)):
            scanned.append((x, self.leftCord(coords)))
            costs.append(cost)
        #################################################################################
        x, cost = self.scanCostAndEvaluation(self.rightCord(coords), finalCords)
        if not x is None and not cost is None and not self.existInMemory(memory, self.rightCord(coords)):
            scanned.append((x, self.rightCord(coords)))
            costs.append(cost)
        return scanned, costs

    # From the series of roads return the best roads
    @staticmethod
    def giveOptimalOptions(options, costs, FinalCords):
        lowerValues = []
        costMinorValues = []
        if len(options) != 0:
            # validate Final
            for i, ContainOption in enumerate(options):
                if ContainOption[1] == FinalCords:
                    lowerValues.append(ContainOption)
                    costMinorValues.append(costs[i])
                    return lowerValues, costMinorValues
            hypnoticLowerValue = options[0]
            # Obtain the lower Cost
            for ContainOption in options:
                if ContainOption[0] < hypnoticLowerValue[0]:
                    hypnoticLowerValue = ContainOption
            # return the equal lowerValue
            for i, ContainOption in enumerate(options):
                if ContainOption[0] == hypnoticLowerValue[0]:
                    lowerValues.append(ContainOption)
                    costMinorValues.append(costs[i])
            return lowerValues, costMinorValues
        return lowerValues, costMinorValues

    # Search coords in the particular memory
    @staticmethod
    def existInMemory(memoryGeneral, coords):
        for memoryCamino in memoryGeneral:
            for x in memoryCamino:
                if memoryCamino[1] == coords:
                    return True
        return False

    @staticmethod
    # create copies, the method branches memory
    def createCopies(RoadAndCostAccumulatedMemories, j, validRoads, costs):
        # print(f"j={j}")
        copyMem = RoadAndCostAccumulatedMemories[j][::]  # Base Copy
        x = len(RoadAndCostAccumulatedMemories[j]) - 1  # last index memory
        for i, Road in enumerate(validRoads):
            # create value to insert
            var = (Road[0], Road[1], copyMem[x][2] + costs[i], costs[i])
            # print(var)
            # if it is the first value, the modification is at the same index in memory
            if i == 0:
                RoadAndCostAccumulatedMemories[j].append(var)
            # if not, duplicate the memory and append the value
            else:
                auxCopyMem = copyMem[::]
                auxCopyMem.append(var)
                RoadAndCostAccumulatedMemories.append(auxCopyMem)

    def aStart(self, initialPoint, FinalPoint, id):
        # [
        # [(f(x),coord,CostAccumulate,particularCost),(f(x),coord,CostAccumulate,particularCost)],
        # [(f(x),coord,CostAccumulate,particularCost),(f(x),coord,CostAccumulate,particularCost)],
        # ]
        RoadAndCostAccumulatedMemories = [[(0, initialPoint, 0, 0)]]
        z = 0
        IndexesToExplore = [0]  # Initialize in 0 for the first evaluation
        roadsComplete = []
        roadsTruncated = []
        while True:
            # >>>> EXPLORATION <<<<
            repeatDepth = False
            # IF THE COST IS EQUAL TO THE COST OF EXPLORING, THEN YOU WILL EXPLORE THIS BRANCH WITHOUT
            # EXPLORING in the search of the same values
            for ITE in IndexesToExplore:
                LastIndex_Repeat = len(RoadAndCostAccumulatedMemories[ITE]) - 1
                explored, costs = self.explorePosition(RoadAndCostAccumulatedMemories[ITE],
                                                       RoadAndCostAccumulatedMemories[ITE][LastIndex_Repeat][
                                                           1],
                                                       FinalPoint
                                                       )
                validRoads, costs = self.giveOptimalOptions(explored, costs, FinalPoint)
                if len(validRoads) != 0:
                    valorMasChico = RoadAndCostAccumulatedMemories[ITE][LastIndex_Repeat][0]
                    # Detect if cost repeats, then change flag repeatDepth and break the for
                    # for indexToExplore in IndexesToExplore:
                    if validRoads[0][0] == valorMasChico:
                        repeatDepth = True
                        break
            for j in IndexesToExplore:
                # print(f"------------------Explore index {j}------------------")
                # If the road reached the destination
                if RoadAndCostAccumulatedMemories[j][len(RoadAndCostAccumulatedMemories[j]) - 1][1] == FinalPoint:
                    # append to roadsComplete the actual Road
                    roadsComplete.append(RoadAndCostAccumulatedMemories[j][::])
                    # delete for the indexesToExplore
                    IndexesToExplore.remove(j)
                else:
                    # Path exploration in the last coordinates of each path validate for the ARRAY FOR BEST CANDIDATES
                    # Last Index in particular memory
                    LastIndex = len(RoadAndCostAccumulatedMemories[j]) - 1
                    explored, costs = self.explorePosition(RoadAndCostAccumulatedMemories[j],
                                                           RoadAndCostAccumulatedMemories[j][LastIndex][1],
                                                           FinalPoint
                                                           )
                    # if the length when exploring it is 0, the path is truncated
                    if len(explored) == 0:
                        # append to the roadsTruncated
                        roadsTruncated.append(RoadAndCostAccumulatedMemories[j][::])
                    # if the length when exploring it is 0, the path is truncated
                    else:
                        # Get the best options for the explored paths
                        validRoads, costss = self.giveOptimalOptions(explored, costs, FinalPoint)
                        # if repeatDepth  and actual value of memory repeat , create copies
                        if repeatDepth and validRoads[0][0] == RoadAndCostAccumulatedMemories[j][LastIndex][0]:
                            self.createCopies(RoadAndCostAccumulatedMemories, j, validRoads, costss)
                        # In case it is not repeated, explore normally, create copies
                        elif not repeatDepth:
                            self.createCopies(RoadAndCostAccumulatedMemories, j, explored, costs)
            # >>>>> ARRAY OF BEST CANDIDATES <<<<<
            exploration = 0  # 0 for f(x)
            # Obtain the lowest, that is to say, the best candidate, who is not in the final roads.
            for i, mems in enumerate(RoadAndCostAccumulatedMemories):
                if not roadsComplete.__contains__(mems) and not roadsTruncated.__contains__(mems):
                    hypotheticalLowerCostPart = mems[len(mems) - 1][exploration]  # F(X)
                    break
            # Compare the lowest cost with other values, who is not in the final roads.
            for i, mems in enumerate(RoadAndCostAccumulatedMemories):
                if mems[len(mems) - 1][exploration] < hypotheticalLowerCostPart and not roadsComplete.__contains__(
                        mems) and not roadsTruncated.__contains__(mems):
                    hypotheticalLowerCostPart = mems[len(mems) - 1][exploration]  # F(X)
                    hypotheticalCost = mems[len(mems) - 1][2]
            # Obtain the lowest Road in the completes
            if len(roadsComplete) > 4:
                break
            # Clear the indexes to explore
            IndexesToExplore.clear()
            # Obtain the indexes with the lower cost
            for i, mems in enumerate(RoadAndCostAccumulatedMemories):
                # and mems[len(mems) - 1][2] < hypotheticalCost \
                if mems[len(mems) - 1][exploration] == hypotheticalLowerCostPart \
                        and not roadsComplete.__contains__(mems) \
                        and not roadsTruncated.__contains__(mems):
                    IndexesToExplore.append(i)
            z += 1
        #######################################################################################
        # SEARCH IN THE ARRAY roadsComplete
        hypotheticalValue = roadsComplete[0]  # Suponemos que el camino es el menor
        cost = hypotheticalValue[len(hypotheticalValue) - 1][2]
        for finalRoad in roadsComplete:
            if finalRoad[len(finalRoad) - 1][2] < hypotheticalValue[len(hypotheticalValue) - 1][2]:
                hypotheticalValue = finalRoad
                cost = finalRoad[len(finalRoad) - 1][2]
        memory = []
        for mem in hypotheticalValue:
            self.addStageLetras(mem[1][0], mem[1][1], f"C{id}")
            memory.append(mem[1])
        print("MazeSolved")
        self.updateStage()
        lastCoord = memory[len(memory) - 1]
        print(f"Camino:{memory}")
        print(f"Costo:{cost}")
        print(f"LastCoord:{lastCoord}")
        return memory, cost, lastCoord

    ######################################################################

    def unHideActualPosition(self):
        self.unHide(self.ActualCords)
        self.unHide(self.upCord())
        self.unHide(self.downCord())
        self.unHide(self.leftCord())
        self.unHide(self.rightCord())

    def addToMemory(self, coords):
        if not self.existsInMemory(coords):
            self.memoryCells.append(coords)

    def existsInMemory(self, coords):
        return self.memoryCells.__contains__(coords)

    def isValidPosition(self, Coords):
        return 0 <= Coords[0] < len(self.stageLetras) and 0 <= Coords[1] < len(self.stageLetras[0]) \
               and self.giveCost(Coords) >= 0

    def giveCost(self, Coords):
        return self.movsCost[self.cellInfo(Coords=Coords).value]

    def returnCost(self, typeTerrain):
        return self.movsCost[typeTerrain.value]

    def printAgent(self):
        print(f"~~~~~~~~~~~~\nNombre:{self.Name} \nTipo:{self.TypeAgent.name} \nMovs")
        for num, x in enumerate(self.movsCost):
            print("- {}: {}".format(Terrain(num).name, x))
        print("~~~~~~~~~~~~")

    def GiveColor(self):
        if self.TypeAgent == TypeAgent.pulpo:
            return (70, 0, 130)
        if self.TypeAgent == TypeAgent.humano:
            return (193, 178, 36)
        if self.TypeAgent == TypeAgent.mono:
            return (122, 88, 13)
        if self.TypeAgent == TypeAgent.sasquatch:
            return (3, 184, 159)

    def updateStage(self):
        self.stageToImage(self.Name)


def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words


def distanceManhatan(origen, end):
    return abs(end[0] - origen[0]) + abs(end[1] - origen[1])


def giveCords(tuplaNumLetter):
    return (tuplaNumLetter[0] - 1), (ord(tuplaNumLetter[1]) - 65)


def giveNumLetter(Coords):
    return (Coords[0] + 1), chr(Coords[1] + 65)

