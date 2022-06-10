__author__ = "David Lopez Hernandez"
__author__ = "Uriel Onofre Resendiz"
__author__ = "Alejandro Escamilla Sánchez"
__name__ = "Practica de laboratorio 1"
__asginatura__ = "Inteligencia Artificial"

import os, sys, pygame
from LibsGame.MazeAgent import *


class Player(object):

    def __init__(self):
        self.rect = pygame.Rect(agent1.InitialCords[1] * 50, agent1.InitialCords[0] * 50, 50, 50)

    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        if 0 <= (self.rect.x + dx) <= (width - 50):
            if dx > 0:
                agent1.movRight()
            elif dx < 0:
                agent1.movLeft()
            self.rect.x += dx
        if 0 <= (self.rect.y + dy) <= (height - 50):
            if dy > 0:
                agent1.movDown()
            elif dy < 0:
                agent1.movUp()
            self.rect.y += dy
        self.collision(dx, dy)

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


os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

agent1 = Agent("Human", TypeAgent.humano, InitalCords=(2, 'B'), stageText=readFile("lab2.txt"), FinalCords=(2, 'E'),
               Hide=False)
# agent1 = Agent("pulpo", TypeAgent.pulpo, InitalCords=(1, 'B'), stageText=readFile("lab2.txt"), FinalCords=(15, 'A'))
# agent1 = Agent("mono", TypeAgent.mono, InitalCords=(1, 'B'), stageText=readFile("lab2.txt"), FinalCords=(15, 'A'))
# agent1 = Agent("sasquatch", TypeAgent.sasquatch, InitalCords=(1, 'B'), stageText=readFile("lab2.txt"), FinalCords=(15, 'A'))


if agent1.TypeAgent == TypeAgent.pulpo:
    colorrgb = (70, 0, 130)
if agent1.TypeAgent == TypeAgent.humano:
    colorrgb = (193, 178, 36)
if agent1.TypeAgent == TypeAgent.mono:
    colorrgb = (122, 88, 13)
if agent1.TypeAgent == TypeAgent.sasquatch:
    colorrgb = (3, 184, 159)

pygame.display.set_caption("Laberinto - David Lopez Hernandez, Alejandro Escamilla Sanchez, Uriel Onofre Resendiz")
width = len(agent1.Stage.stage) * 50
height = len(agent1.Stage.stage) * 50
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
walls = []
player = Player()
# Holds the level layout in a list of strings.
level = agent1.Stage.stage
# Parse the level string above. W = wall, E = exit
final = agent1.FinalCords
x = y = 0
for crow, row in enumerate(level):  # x
    for ccol, col in enumerate(row):  # y
        if agent1.isValidPosition((ccol, crow)) == 0:
            Wall((crow * 50, ccol * 50))
        if crow == final[0] and ccol == final[1]:
            end_rect = pygame.Rect(ccol * 50, crow * 50, 50, 50)

running = True
back = pygame.image.load(agent1.Name + ".png")
while running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

        # Here Selector IA OR HUMAN
        # Move the player if an arrow key is pressed
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                # valid out of bounds
                validOOB = agent1.leftCord()
                if validOOB[0] != -1 and validOOB[1] != -1 and agent1.isValidPosition(validOOB):
                    if not agent1.existsInMemory(validOOB):
                        agent1.Stage.textToImage(validOOB[1], validOOB[0], "V", agent1.Name + ".png")
                    player.move(-50, 0)
                    back = pygame.image.load(agent1.Name + ".png")
            if e.key == pygame.K_RIGHT:
                validOOB = agent1.rightCord()
                if validOOB[0] < len(agent1.Stage.stage) and validOOB[1] < len(
                        agent1.Stage.stage) and agent1.isValidPosition(agent1.rightCord()):
                    if not agent1.existsInMemory(validOOB):
                        agent1.Stage.textToImage(validOOB[1], validOOB[0], "V", agent1.Name + ".png")
                    player.move(50, 0)
                    back = pygame.image.load(agent1.Name + ".png")
            if e.key == pygame.K_UP:
                validOOB = agent1.upCord()
                if validOOB[0] != -1 and validOOB[1] != -1 and agent1.isValidPosition(agent1.upCord()):
                    if not agent1.existsInMemory(validOOB):
                        agent1.Stage.textToImage(validOOB[1], validOOB[0], "V", agent1.Name + ".png")
                    player.move(0, -50)
                    back = pygame.image.load(agent1.Name + ".png")
            if e.key == pygame.K_DOWN:
                validOOB = agent1.downCord()
                if validOOB[0] < len(agent1.Stage.stage) and validOOB[1] < len(
                        agent1.Stage.stage) and agent1.isValidPosition(agent1.downCord()):
                    if not agent1.existsInMemory(validOOB):
                        agent1.Stage.textToImage(validOOB[1], validOOB[0], "V", agent1.Name + ".png")
                    player.move(0, 50)
                    back = pygame.image.load(agent1.Name + ".png")

    # Just added this to make it slightly fun ;)

    if player.rect.colliderect(end_rect):
        pygame.quit()
        sys.exit()

    # Draw the scene
    screen.blit(back, (0, 0))
    # for wall in walls:
    # pygame.draw.ellipse(screen, (255, 128, 64), wall.rect)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, colorrgb, player.rect)
    # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,128))
    pygame.display.flip()

pygame.quit()

"""
.------..------..------.
|D.--. ||A.--. ||U.--. |
| :/\: || (\/) || (\/) |
| (__) || :\/: || :\/: |
| '--'D|| '--'A|| '--'U|
`------'`------'`------'
"""
