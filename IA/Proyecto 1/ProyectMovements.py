__author__ = "David Lopez Hernandez"
__author__ = "Uriel Onofre Resendiz"
__author__ = "Alejandro Escamilla Sánchez"
__name__ = "Practica de laboratorio 2"
__asginatura__ = "Inteligencia Artificial"

import os
import pygame
import pygame_menu

from LibsGameV3.LibAEstrella import *


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


def initGame(agent1):
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    IA = True

    colorrgb = agent1.GiveColor()

    pygame.display.set_caption(
        "Laberinto - David Lopez Hernandez, Alejandro Escamilla Sanchez, Uriel Onofre Resendiz " + str(costHuman))
    width = len(agent1.stage) * 50 + 50
    height = len(agent1.stage[0]) * 50 + 50
    screen = pygame.display.set_mode((width, height))

    clock = pygame.time.Clock()
    walls = []
    player = Player(x=agent1.InitialCords[1], y=agent1.InitialCords[0], agent=agent1, width=width, height=height)
    # Holds the level layout in a list of strings.
    level = agent1.stage
    # Parse the level string above. W = wall, E = exit
    prefinal = []
    prefinal += agent1.PreFinalCords[::]
    x = y = 0

    # Initialize
    for crow, row in enumerate(level):  # x
        for ccol, col in enumerate(row):  # y
            if not agent1.isValidPosition((ccol, crow)):
                Wall((crow * 50, ccol * 50))

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
                        if len(agent1.memoryCells) == contador:
                            running = False
                        else:
                            player.setPosition(50 * agent1.memoryCells[contador][1],
                                               50 * agent1.memoryCells[contador][0])
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
        # if player.rect.colliderect(end_rect):
        # end_rect.move(final[0] * 50,  final[1] * 50, 50, 50)
        # end_rect = pygame.Rect()
        # running = False
        # Draw the scene
        screen.blit(back, (0, 0))
        # for wall in walls:
        # pygame.draw.ellipse(screen, (255, 128, 64), wall.rect)
        # pygame.draw.rect(screen, (255, 0, 0), end_rect)
        pygame.draw.rect(screen, colorrgb, player.rect)
        # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,128))
        pygame.display.flip()


# Octopus    10,'B'
# Human      14,'C'
# Monkey     14,'E'
# PortalKey  15,'N'
# DarkTemple 7,'H'
# MagicStone 3,'O'
# Final      13,'D'
a = Stage(textPlain=readFile("./lab5.txt"))

OI = (10, 'B')
HI = (14, 'C')
MI = (14, 'E')
K = (15, 'N')
T = (7, 'H')
S = (3, 'O')
P = (13, 'D')
agent1 = Agent("humano", TypeAgent.humano, initialCoords=HI, FinalCords=P,
               PreFinalCords=(T, S, K), stageText=readFile("./lab5.txt"), Hide=True)
costHuman = agent1.proyect()
print(f"Costos para el humano:{costHuman}")
initGame(agent1)


# agent2 = Agent("Octupus", TypeAgent.pulpo, initialCoords=OI, FinalCords=P,
#               PreFinalCords=(T, S, K), stageText=readFile("./lab5.txt"), Hide=True)
# agent3 = Agent("Monkey", TypeAgent.mono, initialCoords=MI, FinalCords=P,
#               PreFinalCords=(T, S, K), stageText=readFile("./lab5.txt"), Hide=True)
# costOcutpus = agent2.proyect()
# costMonkey = agent3.proyect()
# print(f"Human:{costHuman}")
# print(f"Octupus:{costOcutpus}")
# print(f"Monkey:{costMonkey}")



# for x in range(3):
#    print(CFA1[x], CFA2[x], CFA3[x])
#    if int(CFA1[x]) < int(CFA2[x]) and int(CFA1[x]) < int(CFA3[x]):

# print('El agente uno hara la mision: ', x)
# elif int(CFA2[x]) < int(CFA1[x]) and int(CFA2[x]) < int(CFA3[x]):

#    print('El agente dos hara la mision: ', x)
# elif int(CFA3[x]) < int(CFA1[x]) and int(CFA3[x]) < int(CFA1[x]):

#     print('El agente tres hara la mision: ', x)
