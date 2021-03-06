# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 08:58:54 2020

Program utama, bekerja sebagai controller

@author: Mursito
"""


import random
from congklak_model import CongklakModel
from congklak_view import CongklakView
from congklak_player1 import CongklakPlayer1
from congklak_player2 import CongklakPlayer2
from congklak_player3 import CongklakPlayer3
from congklak_player4 import CongklakPlayer4
from congklak_player04 import CongklakPlayer04

def congklak(p1, p2, banyak):
    p1.setNomor(0)
    p2.setNomor(1)
    pemain=[p1, p2]    
    papan = CongklakModel(banyak)
    layar = CongklakView()
    status = 0
    papan.awal()
    layar.tampilAwal(papan, pemain)
    while not papan.akhir():
        layar.tampilMain(papan, pemain)
        if papan.bisaMain():
            p = papan.getPemain()
            langkah = pemain[p].main(papan)
            status=papan.main(langkah)
        else:
            status = papan.S_MATI

        while status == papan.S_LANJUT:
            status = papan.jalan()
            layar.tampilJalan(papan, pemain)
        if status == papan.S_ULANG:
            layar.tampilUlang(papan, pemain)
        elif status == papan.S_TABUNG:
            layar.tampilTabung(papan, pemain)
        elif status == papan.S_TEMBAK:
            layar.tampilTembak(papan, pemain)
            papan.gantian()
        elif status >= papan.S_MATI:
            layar.tampilMati(papan, pemain)
            papan.gantian()
        # periksa key, kalau ESCAPE berhenti
        """ if layar.keyEscape():
            break """
    layar.tampilAkhir(papan, pemain)
    return papan.pemenang()


#p1=CongklakPlayer1()
#p2=CongklakPlayer2()
#p1=CongklakPlayer3()
p1=CongklakPlayer04()
p2=CongklakPlayer4()

menang=[0,0,0]
skor=[]

batas_banyak = 6

# main 10 kali
for i in range (10):
    s,m = congklak(p1,p2, batas_banyak)
    menang[m] += 1
    skor.append(s)
    s,m = congklak(p2,p1, batas_banyak)
    menang[m] += 1
    s.reverse()
    skor.append(s)

print(p1.nama, 'vs', p2.nama)
print('Menang ', menang)
print('Skor ', skor)