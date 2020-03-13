''' 
Congklak GUI (Using congklak_model script)
To do :
    - OOP implementation
    - Import sprite
    - Player
    - Overlay on hover
    - Button hover and click
    - Remove uncertainty (banyak) from CongklakModel
    - Custom font assets
'''


import pygame
from congklak_model import CongklakModel
from congklak_player1 import CongklakPlayer1
from congklak_player2 import CongklakPlayer2

# Initialization
pygame.init()
screen = pygame.display.set_mode((800,600))             # Set resolution
pygame.display.set_caption("Congklak (alpha) v0.1")     # Set window title

# Load font
font_idx_hole = pygame.font.SysFont('Lato Medium', 24)
font_idx_bank = pygame.font.SysFont('Lato Bold', 60)
font_biji     = pygame.font.SysFont('Lato Black', 80)

# Congklak Initialiation and Global Variables
board = CongklakModel(30)
p1 = CongklakPlayer1()
p2 = CongklakPlayer2()

# Asset Import
window_frame = pygame.image.load('assets/window_frame.png')
window_scoreboard = pygame.image.load('assets/window_scoreboard.png')
title = [pygame.image.load('assets/title_congklak.png'),pygame.image.load('assets/title_ep.png'),pygame.image.load('assets/title_biji.png')]
button = [pygame.image.load('assets/button_play.png'),pygame.image.load('assets/button_reset.png')]
arena_frame = pygame.image.load('assets/arena_frame.png')
arena_hole = pygame.image.load('assets/arena_hole.png')
arena_hole_active = pygame.image.load('assets/arena_hole_active.png')
hole_overlay = pygame.image.load('assets/hole_overlay.png')
hole_overlay_large = pygame.image.load('assets/hole_overlay_large.png')

# Global Variable / Dictionary
colors = {
    'BLACK': (0,0,0),
    'WHITE': (255,255,255)
}

# Update screen (full frame)
def update_screen(board,screen):
    screen.fill(colors['WHITE'])
    load_template(screen)
    update_active_player(board,screen)
    update_hole_overlay(board,screen)
    update_hole(board,screen)
    update_biji(board,screen)
    pygame.display.update()

# Load template
def load_template(screen):
    screen.blit(window_frame, (0,0))            # Frame full screen
    screen.blit(window_scoreboard, (295,490))   # Bottom scoreboard frame
    screen.blit(title[0], (225,31))             # 'CONGKLAK' title
    screen.blit(title[1], (229,90))             # 'Engineering Physics' title
    screen.blit(title[2], (378,137))            # 'BIJI' title
    screen.blit(button[0], (47,39))             # Play button
    screen.blit(button[1], (49,91))             # Reset button
    screen.blit(arena_frame, (50,280))          # Frame
    screen.blit(arena_hole, (97,300))           # Hole (7 small + 1 bank each side)

# Update hole display
def update_hole(board,screen):
    hole_1 = board.getLubang(0)
    hole_2 = board.getLubang(1)
    b1 = board.getTabungan(0)
    b2 = board.getTabungan(1)

    # Convert single-digit to two-digit
    if b1 < 10:
        b1 = '0' + str(b1)
    if b2 < 10:
        b2 = '0' + str(b2)

    # Top row
    for i in range(0,7):
        screen.blit(font_idx_hole.render('(' + str(hole_2[i]) + ')',1,(colors['BLACK'])), (203 + 60*i,245))
    screen.blit(font_idx_bank.render(str(b2),1,colors['BLACK']), (635,337))

    # Bottom row
    for i in range(0,7):
        screen.blit(font_idx_hole.render('(' + str(hole_1[6-i]) + ')',1,(colors['BLACK'])), (203 + 60*i,440))
    screen.blit(font_idx_bank.render(str(b1),1,colors['BLACK']), (112,337))

# Update active player overlay
def update_active_player(board,screen):
    p = board.getPemain()
    screen.blit(arena_hole_active, (192,361 - p*61))

# Update moving overlay
def update_hole_overlay(board,screen):
    p = board.getPemain()
    x, move = board.getLangkah()

    if move == 7:
        screen.blit(hole_overlay_large, (97 + 525*p,318))
    elif move < 7 and move >= 0:
        if p == 0:
            if x == 0:
                screen.blit(hole_overlay, (552 - 60*move,361))
            elif x == 1:
                screen.blit(hole_overlay, (192 + 60*move,300))
        if p == 1:
            if x == 0:
                screen.blit(hole_overlay, (192 + 60*move,300))
            elif x == 1:
                screen.blit(hole_overlay, (552 - 60*move,361))

# Update biji count
def update_biji(board,screen):
    b = board.getBiji()
    screen.blit(font_biji.render(str(b),1,colors['BLACK']), (378,150))

# Conglak main
def main_congklak(p1,p2,board,screen):
    # Initialize attribute and game parameter
    p1.setNomor(0)
    p2.setNomor(1)
    status = 0
    player = [p1,p2]
    update_active_player(board,screen)
    print('L0: ', board.getLubang(0))
    print('L1: ', board.getLubang(1))
    
    # Game loop until all hole are empty
    while not board.akhir():
        print("loop")
        if board.bisaMain():
            print("bisamain")
            p = board.getPemain()
            move = player[p].main(board)
            status = board.main(move)
        else:
            print("mati")
            status = board.S_MATI
        
        while status == board.S_LANJUT:
            status = board.jalan()
            update_screen(board,screen)

        if status == board.S_ULANG:
            pass
            # Warning: invalid move

        elif status == board.S_TABUNG:
            update_screen(board,screen)

        elif status == board.S_TEMBAK:
            update_screen(board,screen)
            board.gantian()

        elif status >= board.S_MATI:
            # Update display: change turn
            board.gantian()
            #update_screen(board,screen)
    print('pemenang:')
    print(board.pemenang())
    # Update display: winner
    # Update score

# Main loop
def main():
    runningState = True
    while runningState:
        # Frame rate
        pygame.time.delay(30)
        
        # Get quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningState = False
        
        # Load interface template
        screen.fill(colors['WHITE'])
        load_template(screen)
        pygame.display.update()
        main_congklak(p1,p2,board,screen)

        # Update screen
        pygame.display.update()

# Main program
main()
pygame.quit()