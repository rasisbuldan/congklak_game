''' 
Congklak GUI (Using congklak_model script)
To do :
    - OOP implementation
    - Import sprite
    - Overlay on hover
    - Button hover and click

'''


import pygame
#from congklak_model import CongklakModel

# Initialization
pygame.init()
screen = pygame.display.set_mode((800,600))             # Set resolution
pygame.display.set_caption("Congklak (alpha) v0.1")     # Set window title
font = pygame.font.SysFont('Lato Semibold', 30, True)   # Load font

# Asset Import
window_frame = pygame.image.load('assets/window_frame.png')
window_scoreboard = pygame.image.load('assets/window_scoreboard.png')
title = [pygame.image.load('assets/title_congklak.png'),pygame.image.load('assets/title_ep.png')]
button = [pygame.image.load('assets/button_play.png'),pygame.image.load('assets/button_reset.png')]
arena_frame = pygame.image.load('assets/arena_frame.png')
arena_hole = pygame.image.load('assets/arena_hole.png')
arena_hole_active = pygame.image.load('assets/arena_hole_active.png')
hole_overlay = pygame.image.load('assets/hole_overlay.png')

# Global Variable
colors = {
    'BLACK': (0,0,0),
    'WHITE': (255,255,255)
}

# Load template
def load_template(surface):
    surface.blit(window_frame, (0,0))   # Frame full screen
    surface.blit(window_scoreboard, (295,490))
    surface.blit(title[0], (225,31))    # 'CONGKLAK' title
    surface.blit(title[1], (229,90))    # 'Engineering Physics' title
    surface.blit(button[0], (47,39))    # Play button
    surface.blit(button[1], (49,91))    # Reset button
    surface.blit(arena_frame, (50,280)) # Frame
    surface.blit(arena_hole, (100,300)) # Hole (7 small + 1 bank each side)

def main():
    runningState = True
    while runningState:
        # Frame rate
        pygame.time.delay(500)

        # Get quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningState = False
        
        # Load interface template
        screen.fill(colors['WHITE'])
        load_template(screen)

        # Update screen
        pygame.display.update()

main()
pygame.quit()

'''
Trash:
#text = font.render('Test: ' + str(i), 1, (255,128,0))
#screen.blit(text, (100,100))
'''