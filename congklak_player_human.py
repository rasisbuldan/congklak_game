# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 08:04:48 2020

@author: Mursito
"""

import random
import pygame
from congklak_model import CongklakModel
from congklak_player import CongklakPlayer

class CongklakPlayerHuman(CongklakPlayer):
    
    def __init__(self):
        super().__init__('Human')

    

    # Pemain beraksi
    # Gunakan informasi dari papan untuk memilih nomor 
    # lubang mulai
    def main(self, papan):
        nexts = []
        lubang = papan.getLubang(self.nomor)
        sel = -1
        
        # Get valid available move
        for i in range(len(lubang)):
            if (lubang[i] > 0):
                nexts.append(i)
        
        # Assumption: player always on P1
        pygame.event.clear()
        while True:
            print('Waiting for input..')
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    sel = 6
                elif event.key == pygame.K_2:
                    sel = 5
                elif event.key == pygame.K_3:
                    sel = 4
                elif event.key == pygame.K_4:
                    sel = 3
                elif event.key == pygame.K_5:
                    sel = 2
                elif event.key == pygame.K_6:
                    sel = 1
                elif event.key == pygame.K_7:
                    sel = 0
            if sel in nexts:
                return sel
            else:
                print('Invalid input...')