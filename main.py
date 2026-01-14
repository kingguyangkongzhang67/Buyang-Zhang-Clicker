import pygame, random, sys, math, time

pygame.init()

# setup 
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Charlie Clicker 5000")

# load sprites
beewu = pygame.image.load(r"beewu.png").convert_alpha()
beewu_rect = beewu.get_rect(center=(WIDTH / 2, HEIGHT / 2))

clock = pygame.time.Clock()
die = 0

# other shit
gameState = 0
noodles = 0
while not die:
    # RECOGNIZE QUIT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            die = 1
    
    if not gameState:
        print("Hello!")
    if gameState:
        print("Goodbye")

