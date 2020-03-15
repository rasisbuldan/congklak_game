# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 08:04:48 2020

@author: Mursito
"""
# Dimas Apeco Putra 13316015
# Rasis Syauqi Buldan 13316043
# Thoriq Fauzan Ariandi 13316063

import random
from congklak_model import CongklakModel
from congklak_player import CongklakPlayer


class CongklakPlayer04(CongklakPlayer):

    def __init__(self):
        super().__init__('PruneMast3r999')

    # Pemain beraksi
    # Gunakan informasi dari papan untuk memilih nomor
    # lubang mulai
    def main_old(self, papan):
        nexts = []
        lubang = papan.getLubang(self.nomor)
        # cari maksimal
        max = 0
        for i in range(len(lubang)):
            if (lubang[i] > max):
                max = lubang[i]

        # tambahkan yang maksimal
        for i in range(len(lubang)):
            if (lubang[i] >= max):
                nexts.append((lubang[i], i))

        print(nexts)
        pilih = random.randint(0, len(nexts)-1)
        return nexts[pilih][1]

# --------holy limit----------

    def initial_state(self, p, i=None):
        # initial_state() --> list of lubang
        # Indeks lubang: (0) 0-6, 7 tabung
        #                (1) 8-14, 15 tabung

        h0 = CongklakModel(9).getLubang(0)
        h0 = h0 + [CongklakModel(9).getTabungan(0)]
        h1 = CongklakModel(9).getLubang(1)
        h1 = h1 + [CongklakModel(9).getTabungan(1)]
        print('h0: ', h0)
        print('h1: ', h1)
        if i == 0:
            return h0
        elif i == 1:
            return h1
        elif i == None:
            return [(h0 + h1), 0, 0, 0, 0, False]

    def advance(self, x, p, initial):
        # advance(move,initial_state) --> [bank0,bank1,stepover0,stepover1]
        # Get initial position value
        # x : index lubang
        # p : index player
        # initial : initial array (i=None)

        # Local variable
        #print('------ layer:',p,' x: ',x)
        #print('(adv) initial: ',initial)
        h = initial[0]
        initial_bank0 = h[7]
        initial_bank1 = h[15]
        stepover0 = 0
        stepover1 = 0
        again = False
        k = 0
        j = 0

        if initial[4] == True:
            return [initial[0], initial[1], initial[2], initial[3]]
        else:
            # get_hole --> value, index
            def get_hole(k):
                j = h[k]
                h[k] = 0
                return j

            # Initial value
            k = x + 8*p
            j = j0 = get_hole(k)

            # Termination
            while j > 0:
                #print('k: ',k,' j: ',j,' | ',h[0:7],' ',h[8:15])
                #print('j: ',j)
                # Biji banyak
                if j != 1:
                    # Maju satu langkah
                    k = (k + 1) % 16
                    h[k % 16] += 1
                    j -= 1

                # Prepare for termination
                elif j == 1:
                    # Not empty next
                    # -- Tabungan
                    if (((k+1) == 15) or ((k+1) == 7)):
                        # Adv
                        k = (k + 1) % 16
                        h[k % 16] += 1
                        j -= 1

                        again = True
                        break

                    # -- Lubang
                    elif h[(k + 1) % 16] != 0:
                        # Adv
                        k = (k + 1) % 16
                        h[k % 16] += 1
                        j -= 1

                        j = get_hole(k)

                    # Empty next
                    elif h[(k + 1) % 16] == 0:
                        # Nembak
                        if k < 7 and k >= 0 and h[14 - (k + 1)] != 0:
                            # Adv
                            k = (k + 1) % 16
                            h[k % 16] += 1
                            j -= 1

                            # ...
                            h[7] += h[k] + h[14 - k]
                            h[k] = h[14 - k] = 0
                            break
                        # Mati
                        else:
                            # Adv
                            k = (k + 1) % 16
                            h[k % 16] += 1
                            j -= 1

                            break

                # Stepover
                if k > 7 and k != 15:
                    stepover1 += 1
                if k < 7 and k >= 0:
                    stepover0 += 1

            b0 = h[7] - initial_bank0
            b1 = h[15] - initial_bank1
            s0 = stepover0
            s1 = stepover1
            #print('(adv) final: ',[h, b0, b1, s0, s1, again])
            return [h, b0, b1, s0, s1, again]

    def move_possibility(self, initial, p):
        # move_possibility(initial_state,p) --> list of move of player p
        move = []
        h = initial[0]
        #print('initial h: ',h)
        for i in range(0, 7):
            #print('initial i: ',i)
            if h[i + 8*p] != 0:
                move.append([i, h[i + 8*p]])
        #print('move: ',move[0])
        return move

    def main(self, papan):
        #dari keadaan board initial, catat banyak_tabungan kita & lawan
        p = self.nomor
        print('no: ', p)
        state0 = self.initial_state(0)
        print('state0: ', state0)
        h_bank_x0 = state0[0][(7 + 8*p) % 16]
        h_bank_y0 = state0[0][(15 + 8*p) % 16]
        w = [0.4, 0.1, 0.4, 0.1]
        max_of_min = [-999, -999, -999]
        print('p: ', p)
        print(self.move_possibility(state0, p))

        if len(self.move_possibility(state0, 1-p)) == 0:
            return self.move_possibility(state0, p)[0][0]
        elif len(self.move_possibility(state0, p)) == 1:
            print('tinggal satu')
            return self.move_possibility(state0, p)[0][0]
        elif len(self.move_possibility(state0, p)) == 2:
            print('tinggal dua')
            return self.move_possibility(state0, p)[0][0]
        else:
            #loop untuk semua kemungkinan gerakan kita
            # todo: define our_possibility
            for x in self.move_possibility(state0, p):
                #run langkah x1 sampai keadaan ending langkah, lalu
                state1 = self.advance(x[0], p, state0)
                #catat banyak_tabungan kita dan jumlah lubang lawan yg disinggahi, lalu
                h_bank_x1 = state1[1]
                h_stepover_x1 = state1[3]  # harusnya suatu method
                fe_buffer_y = []
                #loop untuk semua kemungkinan gerakan lawan
                # todo: define opponent_possibility
                for y in self.move_possibility(state1, 1-p):
                    #run langkah y lawan sampai keadaan ending langkah lawan, lalu
                    state2 = self.advance(y[0], 1-p, state1)
                    print('state1: ', state1)
                    print('state ({},{}): '.format(x[0], y[0]), state2)
                    #catat banyak_tabungan lawan dan jumlah lubang kita yg disinggahi lawan, lalu
                    h_bank_y1 = state2[1]
                    h_stepover_y1 = state2[3]  # harusnya suatu method
                    #hitung fungsi evaluasi,
                    f_e = w[0] * (h_bank_x1 - h_bank_x0)
                    f_e -= w[1] * h_stepover_x1
                    f_e -= w[2] * (h_bank_y1 - h_bank_y0)
                    f_e += w[3] * h_stepover_y1
                    print('fe: ', f_e)
                    #simpan f_e di array all_f_e[x,y]
                    if p == 0:
                        fe_buffer_y.append([round(f_e, 3), x[0], y[0]])
                    elif p == 1:
                        fe_buffer_y.append([round(f_e, 3), 6-x[0], 6-y[0]])
                    print('fe_buffer: ', fe_buffer_y)
                    #jika selain x1, maka
                    if x[0] != 0:
            			#jika f_e lebih kecil dari max_of_min,
                        if f_e < max_of_min[0]:
                            #lanjut ke x selanjutnya
                        	break
            			#else lanjut ke y selanjutnya
                #jika x = x1, maka
                if x[0] == 0:
                    #max_of_min = min(all_f_e[x1,:])
                    #index_max_of_min = indexof(min(all_f_e[x1,:]))
                    print('fe_buffer: ', fe_buffer_y)
                    if fe_buffer_y == []:
                        break
                    max_of_min = min(fe_buffer_y[:])
                #else
                elif len(fe_buffer_y[:]) != 0:
                    #jika min(all_f_e[x,:]) > max_of_min , maka
                    buf_min = min(fe_buffer_y[:])[0]
                    print('mom: ', max_of_min[0])
                    if buf_min > max_of_min[0]:
                        #max_of_min = min(all_f_e[x,:])
                        #index_max_of_min = indexof(min(all_f_e[x,:]))
                        max_of_min = min(fe_buffer_y[:])
                        print(max_of_min)
            print('mom: ', max_of_min[0], 'x: ', max_of_min[1],
                  ' val: ', state0[0][(max_of_min[1] + 8*p) % 16])
            if max_of_min[1] == -999:
                #print('move available:', self.move_possibility(state0, p)[0][0])
                print('returning1: ', self.move_possibility(state0, 1-p)[0][0])
                return self.move_possibility(state0, p)[0][0]
            else:
                if p == 0:
                    print('returning2: ', max_of_min[1])
                    return max_of_min[1]
                elif p == 1:
                    print('returning3: ', 6-max_of_min[1])
                    return (6-max_of_min[1])
