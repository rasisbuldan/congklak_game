''' 
Congklak GUI (Using congklak_model script)
To do :
    - OOP implementation
    - Import sprite
    - Button hover and click
        - Overlay on hover
    - Customization 
    - Custom font assets
    - Player name attribute display
'''

import pygame
from congklak_model import CongklakModel
from congklak_player1 import CongklakPlayer1
from congklak_player2 import CongklakPlayer2
from congklak_player_human import CongklakPlayerHuman

# Initialization
pygame.init()
screen = pygame.display.set_mode((800,600))             # Set resolution
pygame.display.set_caption("Congklak (alpha) v0.1")     # Set window title

# Load font
font_idx_hole = pygame.font.SysFont('Lato Medium', 24)
font_idx_bank = pygame.font.SysFont('Lato Bold', 60)
font_biji     = pygame.font.SysFont('Lato Black', 80)
font_score    = pygame.font.SysFont('Lato Bold', 100)

# Congklak Initialiation and Global Variables
#p1 = CongklakPlayer1()
p1 = CongklakPlayerHuman()
p2 = CongklakPlayer2()

# Asset Import
window_frame = pygame.image.load('assets/window_frame.png')
window_scoreboard = pygame.image.load('assets/window_scoreboard.png')
title = [pygame.image.load('assets/title_congklak.png'),pygame.image.load('assets/title_ep.png'),pygame.image.load('assets/title_biji.png')]
button = [pygame.image.load('assets/button_play.png'),pygame.image.load('assets/button_reset.png')]
arena_frame = pygame.image.load('assets/arena_frame.png')
arena_hole = pygame.image.load('assets/arena_hole.png')
arena_hole_active = pygame.image.load('assets/arena_hole_active.png')
player_name = [pygame.image.load('assets/player_1.png'), pygame.image.load('assets/player_2.png')]
score_ddots = pygame.image.load('assets/score_ddots.png')
hole_overlay = pygame.image.load('assets/hole_overlay.png')
hole_overlay_large = pygame.image.load('assets/hole_overlay_large.png')
hole_count = []
for i in range(0,13):
    hole_count.append(pygame.image.load('assets/biji/' + str(i) + '.png'))


# Global Variable / Dictionary
colors = {
    'BLACK': (0,0,0),
    'WHITE': (255,255,255)
}
score = [0,0,0]

# Update screen (full frame)
def update_screen(board,screen):
    load_template(screen)
    update_active_player(board,screen)
    update_hole_overlay(board,screen)
    update_hole_count(board,screen)
    update_hole(board,screen)
    update_biji(board,screen)
    update_score(screen)
    pygame.display.update()

# Load template
def load_template(screen):
    screen.fill(colors['WHITE'])
    screen.blit(window_frame, (0,0))            # Frame full screen
    screen.blit(window_scoreboard, (295,490))   # Bottom scoreboard frame
    screen.blit(title[0], (225,31))             # 'CONGKLAK' title
    screen.blit(title[1], (229,90))             # 'Engineering Physics' title
    screen.blit(title[2], (378,137))            # 'BIJI' title
    screen.blit(button[0], (47,39))             # Play button
    screen.blit(button[1], (49,91))             # Reset button
    screen.blit(arena_frame, (50,280))          # Frame
    screen.blit(arena_hole, (97,300))           # Hole (7 small + 1 bank each side)
    screen.blit(player_name[0], (145,545))      # Player 1 name
    screen.blit(player_name[1], (520,545))      # Player 2 name
    screen.blit(score_ddots, (390,525))         # Player score separator

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


# Update hole illustration based on how many biji count in hole
def update_hole_count(board,screen):
    hole_1 = board.getLubang(0)
    hole_2 = board.getLubang(1)

    # Hole count traversal
    for i in range(0,7):
        # Top row
        c = hole_2[i]
        if hole_2[i] > 12:
            c = 12
        #print('c_top: ',str(c))
        screen.blit(hole_count[c], (192 + 60*i,300))

        # Bottom row
        c = hole_1[6-i]
        if hole_1[6-i] > 12:
            c = 12
        #print('c_bot: ',str(c))
        screen.blit(hole_count[c], (192 + 60*i,361))

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

# Update score (p1 vs p2)
def update_score(screen):
    screen.blit(font_score.render(str(score[0]),1,colors['BLACK']), (330,505))
    screen.blit(font_score.render(str(score[2]),1,colors['BLACK']), (420,505))

# Conglak main
def main_congklak(p1,p2,screen):
    # Initialize attribute and game parameter
    board = CongklakModel(30)
    board.awal()
    p1.setNomor(0)
    p2.setNomor(1)
    status = 0
    player = [p1,p2]
    update_screen(board,screen)
    
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
            status = board.jalan(0.2)
            update_screen(board,screen)

        if status == board.S_ULANG:
            pass
            # Warning: invalid move

        elif status == board.S_TABUNG:
            update_screen(board,screen)

        elif status == board.S_TEMBAK:
            update_screen(board,screen)
            board.gantian(0.1)

        elif status >= board.S_MATI:
            # Update display: change turn
            print('gantian')
            board.gantian(1)
            #update_screen(board,screen)
    return board.pemenang()

# Main loop
def main():
    runningState = True
    gameEnd = False
    while runningState:
        # Frame rate
        pygame.time.delay(30)

        # Get quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningState = False

        if not gameEnd:
            for i in range(4):
                s,m = main_congklak(p1,p2,screen)
                print('selesaimain')
                score[m] += 1
                screen.fill(colors['WHITE'])
                load_template(screen)
                update_score(screen)
                pygame.display.update()
            gameEnd = True

        # Update screen
        # pygame.display.update()

# Main program
main()
pygame.quit()