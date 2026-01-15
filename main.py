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

noodleBg = pygame.image.load(os.path.join(ASSETS, "noodlebg.png")).convert_alpha()
noodleBg_rect = noodleBg.get_rect(center=(WIDTH / 2, HEIGHT / 2))

# other shit

clock = pygame.time.Clock()
die = 0

gameState = 1
'''
important

0 = starting menu
1 = clicker ui
2 = shop ? 
'''
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

def collision(rec: pygame.Rect, x: int, y: int):
    return rec.collidepoint(x, y)

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
    
    # BACKGROUND
    screen.blit(noodleBg, noodleBg_rect)

    # starting 
    if not gameState:
        pass 

    if gameState:
        screen.blit(beewu, beewu_rect)
        clock.tick(120)

    pygame.display.flip()


