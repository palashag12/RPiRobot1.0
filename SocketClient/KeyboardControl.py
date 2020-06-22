import pygame
import pygame.locals
import NetworkCommunications as ncms
from time import sleep
from SocketClient.Client import Client

# variables
WIDTH = 640
HEIGHT = 320
DELTA_TIME = 0.1
running = True
client = Client(ncms.ip, ncms.Ports.SOCKET)

# user decided variables
forwardKey = pygame.locals.K_UP
leftKey = pygame.locals.K_LEFT
rightKey = pygame.locals.K_RIGHT
backwardKey = pygame.locals.K_DOWN
stopKey = pygame.locals.K_SPACE
forwardSensitivity = 0.5

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.flip()

forwardSpeed = 0

def getTurnSpeeds(right = True, reverse = False):
    if right and not reverse or not right and reverse:
        return 1, -1
    else:
        return -1, 1

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        pressedKeys = pygame.key.get_pressed()

    # forward and back
    if pressedKeys[forwardKey] and pressedKeys[backwardKey]:
        pass
    elif pressedKeys[forwardKey]:
        forwardSpeed += DELTA_TIME * forwardSensitivity
    elif pressedKeys[backwardKey]:
        forwardSpeed -= DELTA_TIME * forwardSensitivity

    if forwardSpeed > 1:
        forwardSpeed = 1

    if forwardSpeed < -1:
        forwardSpeed = -1

    leftSpeed = rightSpeed = forwardSpeed 

    # turning (overrides forward movement)
    if pressedKeys[leftKey] and pressedKeys[rightKey]:
        pass
    elif pressedKeys[leftKey]:
        leftSpeed, rightSpeed = getTurnSpeeds(False, forwardSpeed < 0)
    elif pressedKeys[rightKey]:
        leftSpeed, rightSpeed = getTurnSpeeds(True, forwardSpeed < 0)

    # stopping overrides all movement
    if pressedKeys[stopKey]:
        forwardSpeed = 0
        leftSpeed = 0
        rightSpeed = 0

    client.sendSpeeds(leftSpeed, rightSpeed)
    sleep(DELTA_TIME)        





 










