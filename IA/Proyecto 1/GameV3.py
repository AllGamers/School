__author__ = "David Lopez Hernandez"
__author__ = "Uriel Onofre Resendiz"
__author__ = "Alejandro Escamilla Sánchez"
__name__ = "Practica de laboratorio 2"
__asginatura__ = "Inteligencia Artificial"

import os
import pygame
import pygame_menu
import tkinter as tk
from tkinter import filedialog
from typing import Tuple

from LibsGameV3.MazeAgentV3 import *


class Player(object):
    # global agent1, width, height, walls

    def __init__(self, x, y, agent, width, height):
        self.height = height
        self.agent1 = agent
        self.width = width

        self.rect = pygame.Rect(x * 50, y * 50, 50, 50)

    def move(self, dx, dy):
        if dx != 0 and dy == 0:
            return self.move_single_axis(dx, 0)
        if dy != 0 and dx == 0:
            return self.move_single_axis(0, dy)
        return self.move_diagonal_axis(dx, dy)

    def setPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y
        pygame.image.load(self.agent1.Name + ".png")

    def move_single_axis(self, dx, dy):
        if 0 <= (self.rect.x + dx) <= (self.width - 50):
            if dx > 0:
                self.agent1.movRight()
            elif dx < 0:
                self.agent1.movLeft()
            self.rect.x += dx
        if 0 <= (self.rect.y + dy) <= (self.height - 50):
            if dy > 0:
                self.agent1.movDown()
            elif dy < 0:
                self.agent1.movUp()
            self.rect.y += dy
        self.collision(dx, dy)
        return pygame.image.load(self.agent1.Name + ".png")

    def move_diagonal_axis(self, dx, dy):
        if 0 <= (self.rect.x + dx) <= (self.width - 50) and 0 <= (self.rect.y + dy) <= (self.height - 50):
            if dx > 0 and dy > 0:
                self.agent1.movDownRight()
            elif 0 > dx and dy < 0:
                self.agent1.movUpLeft()
            elif dx > 0 > dy:
                self.agent1.movUpRight()
            elif dx < 0 < dy:
                self.agent1.movDownLeft()
            self.rect.x += dx
            self.rect.y += dy
        self.collision(dx, dy)
        return pygame.image.load(self.agent1.Name + ".png")

    def collision(self, dx, dy):
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom


class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 50, 50)


walls = []


def initGame(Name, TypeAgent, stageText, InitialCoord, FinalCords, Hide, PriorMovements,
             Algorithm, NodeByNode, IA):
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    agent1 = Agent(Name, TypeAgent, InitalCords=InitialCoord, stageText=stageText, FinalCords=FinalCords, Hide=Hide,
                   PriorMovements=PriorMovements)

    if IA:
        if Algorithm == "DepthFirstSearch":
            agent1.depthFirstSearch(NodeByNode=NodeByNode)
        if Algorithm == "BreadthFirstSearch":
            agent1.breadthFirstSearch()
        if Algorithm == "A*":
            agent1.aEstrella()

    colorrgb = agent1.GiveColor()

    pygame.display.set_caption("Laberinto - David Lopez Hernandez, Alejandro Escamilla Sanchez, Uriel Onofre Resendiz")
    width = len(agent1.stage) * 50
    height = len(agent1.stage[0]) * 50
    screen = pygame.display.set_mode((width, height))

    clock = pygame.time.Clock()
    walls = []
    player = Player(x=agent1.InitialCords[1], y=agent1.InitialCords[0], agent=agent1, width=width, height=height)
    # Holds the level layout in a list of strings.
    level = agent1.stage
    # Parse the level string above. W = wall, E = exit
    final = agent1.FinalCords
    x = y = 0

    # Initialize
    for crow, row in enumerate(level):  # x
        for ccol, col in enumerate(row):  # y
            if not agent1.isValidPosition((ccol, crow)):
                Wall((crow * 50, ccol * 50))
            if crow == final[0] and ccol == final[1]:
                end_rect = pygame.Rect(ccol * 50, crow * 50, 50, 50)

    running = True
    back = pygame.image.load(agent1.Name + ".png")

    contador = 0
    while running:
        # Here Selector IA OR HUMAN
        # Memoria del agente
        # Camino Optimo en base a la memoria
        for i, e in enumerate(pygame.event.get()):
            if e.type == pygame.QUIT:
                running = False
                surface = pygame.display.set_mode((1500, 800))
                menu = pygame_menu.Menu('Welcome',
                                        1500, 800,
                                        theme=pygame_menu.themes.THEME_DARK)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
                surface = pygame.display.set_mode((1500, 800))

                menu = pygame_menu.Menu('Welcome',
                                        1500, 800,
                                        theme=pygame_menu.themes.THEME_DARK)
            if IA:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        player.setPosition(50 * agent1.memoryCells[contador][1], 50 * agent1.memoryCells[contador][0])
                        contador += 1
            else:
                # Move the player if an KEYPAD key is pressed
                if e.type == pygame.KEYDOWN:
                    # valid out of bounds
                    if e.key == pygame.K_KP4:
                        back = player.move(-50, 0)
                    if e.key == pygame.K_KP6:
                        back = player.move(50, 0)
                    if e.key == pygame.K_KP2:
                        back = player.move(0, 50)
                    if e.key == pygame.K_KP8:
                        back = player.move(0, -50)
                    if agent1.DiagonalMovs:
                        if e.key == pygame.K_KP7:
                            back = player.move(-50, -50)
                        if e.key == pygame.K_KP9:
                            back = player.move(50, -50)
                        if e.key == pygame.K_KP3:
                            back = player.move(50, 50)
                        if e.key == pygame.K_KP1:
                            back = player.move(-50, 50)
        # Just added this to make it slightly fun ;)
        if player.rect.colliderect(end_rect):
            running = False
            surface = pygame.display.set_mode((1500, 800))

            menu = pygame_menu.Menu('Welcome',
                                    1500, 800,
                                    theme=pygame_menu.themes.THEME_DARK)
        # Draw the scene
        screen.blit(back, (0, 0))
        # for wall in walls:
        # pygame.draw.ellipse(screen, (255, 128, 64), wall.rect)
        pygame.draw.rect(screen, (255, 0, 0), end_rect)
        pygame.draw.rect(screen, colorrgb, player.rect)
        # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,128))
        pygame.display.flip()


def disableButtons(value: Tuple, enabled: bool) -> None:
    selectorAlgorithm = menu.get_widget('idAlgorithm')
    selectorMode = menu.get_widget('idMode')
    priorEntry = menu.get_widget('idPrior')
    priorEntry1 = menu.get_widget('idPrior1')
    priorEntry2 = menu.get_widget('idPrior2')
    priorEntry3 = menu.get_widget('idPrior3')
    priorEntry4 = menu.get_widget('idPrior4')
    assert isinstance(value, tuple)
    if enabled:
        selectorAlgorithm.show()
        selectorMode.show()
        priorEntry.show()
        priorEntry1.show()
        priorEntry2.show()
        priorEntry3.show()
        priorEntry4.show()
    else:
        selectorAlgorithm.hide()
        selectorMode.hide()
        priorEntry.hide()
        priorEntry1.hide()
        priorEntry2.hide()
        priorEntry3.hide()
        priorEntry4.hide()


def disableButtons2(value: Tuple, enabled: bool) -> None:
    selectorAlgorithm = menu.get_widget('idAlgorithm')
    selectorMode = menu.get_widget('idMode')
    priorEntry = menu.get_widget('idPrior')
    priorEntry1 = menu.get_widget('idPrior1')
    priorEntry2 = menu.get_widget('idPrior2')
    priorEntry3 = menu.get_widget('idPrior3')
    priorEntry4 = menu.get_widget('idPrior4')
    if value[1] == 2:
        selectorMode.hide()
        priorEntry.hide()
        priorEntry1.hide()
        priorEntry2.hide()
        priorEntry3.hide()
        priorEntry4.hide()
    else:
        selectorMode.show()
        priorEntry.show()
        priorEntry1.show()
        priorEntry2.show()
        priorEntry3.show()
        priorEntry4.show()


# file explorer window
def browseFiles():
    root = tk.Tk()
    filename = filedialog.askopenfilename(initialdir="",
                                          title="Select a File",
                                          filetypes=[('Text', '*.txt')])
    labelFile = menu.get_widget('labelFile')
    labelFile.set_title(filename)
    root.destroy()


def start_the_game():
    userAgentName = agentNameInput.get_value()
    agentType = agentTypeInput.get_value()[0][1]
    iaValue = IAInput.get_value()[0][1]
    hideValue = hideInput.get_value()[0][1]
    stageText = readFile(labelFile.get_title())
    InitialCoord = (int(InitialCoordInput.get_value().split(",")[0]), InitialCoordInput.get_value().split(",")[1])
    FinalCords = (int(FinalCordsInput.get_value().split(",")[0]), FinalCordsInput.get_value().split(",")[1])
    PriorMovements = [priorInput1.get_value()[0][1], priorInput2.get_value()[0][1], priorInput3.get_value()[0][1],
                      priorInput4.get_value()[0][1]]

    Algorithm = AlogorithmInput.get_value()[0][0]
    NodeByNode = nodeOrStepInput.get_value()[0][1]
    if len(userAgentName) > 10:
        agentNameInput.set_background_color((255, 0, 0))
        Error.set_title("Error: Longitud AgentName")
        Error.show()
    initGame(Name=userAgentName, TypeAgent=agentType, stageText=stageText, InitialCoord=InitialCoord,
             FinalCords=FinalCords, Hide=hideValue, PriorMovements=PriorMovements,
             Algorithm=Algorithm, NodeByNode=NodeByNode, IA=iaValue)


# GAME MENU
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
pygame.display.set_caption("Laberinto - David Lopez Hernandez, Alejandro Escamilla Sanchez, Uriel Onofre Resendiz")
surface = pygame.display.set_mode((1500, 800))

menu = pygame_menu.Menu('Welcome',
                        1500, 800,
                        theme=pygame_menu.themes.THEME_DARK)
# COMPONENTES #
############################################### GENERAL ##############################################
agentNameInput = menu.add.text_input('Agent Name :', default="Name", font_size=20)
agentTypeInput = menu.add.selector('AgentType',
                                   [('humano', TypeAgent.humano),
                                    ('mono', TypeAgent.mono),
                                    ('pulpo', TypeAgent.pulpo),
                                    ('sasquatch', TypeAgent.sasquatch)], font_size=20)  #########
IAInput = menu.add.selector('IA:', [('IA', True), ('HUMAN', False)], onchange=disableButtons, font_size=20)  #########
menu.add.vertical_margin(margin=20)
hideInput = menu.add.selector('Hide :', [('True', True), ('False', False)], font_size=20)  #########
menu.add.vertical_margin(margin=20)
fileInput = menu.add.button('File', action=browseFiles, font_size=20)
fileInput.set_background_color((255, 53, 25))
labelFile = menu.add.label("Lab1.txt", label_id="labelFile", font_size=20)
menu.add.vertical_margin(margin=20)
InitialCoordInput = menu.add.text_input('InitialCoords:', default='10,A', font_size=20)
FinalCordsInput = menu.add.text_input('FinalCoords:', default='2,O', font_size=20)
menu.add.vertical_margin(margin=20)
############################################### IA ##############################################
AlogorithmInput = menu.add.selector('Algorithm :', [('BreadthFirstSearch', 1), ('DepthFirstSearch', 2), ('A*', 3)],
                                    selector_id="idAlgorithm", font_size=20, onchange=disableButtons2)
nodeOrStepInput = menu.add.selector('Node or Step :', [('NodeByNode', True), ('StepByStep', False)],
                                    selector_id="idMode", font_size=20)
PriorInput = menu.add.label('Prior:', label_id="idPrior", font_size=20)
options = [("Up", Mov.Up), ("Right", Mov.Right), ("Left", Mov.Left), ("Down", Mov.Down)]
priorInput1 = menu.add.selector('Prior 1', options, selector_id="idPrior1", default=0, font_size=18)
priorInput2 = menu.add.selector('Prior 2', options, selector_id="idPrior2", default=1, font_size=18)
priorInput3 = menu.add.selector('Prior 3', options, selector_id="idPrior3", default=2, font_size=18)
priorInput4 = menu.add.selector('Prior 4', options, selector_id="idPrior4", default=3, font_size=18)
############################################### IA ##############################################
Error = menu.add.label('Error', font_color=(255, 0, 0), font_size=20)
Error.hide()
menu.add.vertical_margin(margin=20)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface, disable_loop=False, clear_surface=True)
##       GRAVITY       ##
