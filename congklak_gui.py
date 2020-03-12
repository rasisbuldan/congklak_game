import pygame
#from congklak_model import CongklakModel

pygame.init()
# Global Variable
font = pygame.font.SysFont('Arial', 30, True)

# Initialization
i = 0

# Set display parameter
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("pygame test")

runningState = True
while runningState:
    pygame.time.delay(500)
    i += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runningState = False
    screen.fill((255,255,255))
    text = font.render('Test: ' + str(i), 1, (255,128,0))
    screen.blit(text, (100,100))
    pygame.display.update()

pygame.quit()
