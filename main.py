import pygame, random, sys, math, time, os, threading

pygame.init()

# setup 
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Charlie Clicker 5000")

# load sprites / assets

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")

beewu = pygame.image.load(os.path.join(ASSETS, "beewu.png")).convert_alpha()
beewu_rect = beewu.get_rect(center=(WIDTH / 2, HEIGHT / 2))

clock = pygame.time.Clock()
die = 0

# other shit
gameState = 0
noodles = 0
nps = 0

# THREADING
def test1():
    while True:
        print("FPS: " + str(math.floor(clock.get_fps())))
        time.sleep(1)
th1 = threading.Thread(target=test1, daemon=True)
th1.start()

# keeps track of running time
def counter():
    num = 1
    while True:
        if num % 3 == 0 and num % 5 == 0:
            print("FizzBuzz!")
        elif num % 3 == 0:
            print("Fizz")
        elif num % 5 == 0:
            print("buzz")
        else:
            print(num)
        num += 1
        time.sleep(1)

th2 = threading.Thread(target=counter, daemon=True)
th2.start()

def addAuto():
    global noodles, nps

    while True:
        noodles += nps 
        print(str(nps) + " noodles added.")
        time.sleep(1)

th3 = threading.Thread(target=addAuto, daemon=True)
th3.start()

import pygame

def collision(rec: pygame.Rect, x: int, y: int):
    return rec.rect.collidepoint(x, y)

# main running loop type shiiiittt
while not die:
    # RECOGNIZE QUIT
    for event in pygame.event.get():
        # DIE
        if event.type == pygame.QUIT:
            die = 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            # button 1 = left mouse
            if event.button == 1:
                mouse_pos = event.pos  # pos xy
                print(f"THIS IS A TEST FUNCTION. your cursor has been clicked at: {mouse_pos}")
                (x, y) = mouse_pos
                print(str(x) + "\n" + str(y))
                print(collision(beewu_rect, x, y))
                #y bound: 200, 600
                #x bound: 400, 660
                if mouse_pos[0] <= 600 and mouse_pos >= 200 and mouse_pos[1] <= 660 and mouse_pos[1] >= 400:
                  noodles += 1
      

    if not gameState:
        screen.fill((255, 255, 0))
        screen.blit(beewu, beewu_rect)
        pygame.display.flip()
        clock.tick(120)

    if gameState:
        print("Goodbye")


