import copy

from congklak_model import CongklakModel
from congklak_player import CongklakPlayer


class CongklakPlayer01(CongklakPlayer):

    def __init__(self):
        super().__init__('Barbar')

    def main(self, papan):  # fungsi eksplorasi
        hole0 = papan.getLubang(self.nomor)[0:7]
        tab0 = papan.getTabungan(self.nomor)
        hole0.append(tab0)
        if(self.nomor == 1):
            hole1 = papan.getLubang(0)[0:7]
            tab1 = papan.getTabungan(0)
            hole1.append(tab1)
        if(self.nomor == 0):
            hole1 = papan.getLubang(1)[0:7]
            tab1 = papan.getTabungan(1)
            hole1.append(tab1)
        hole = [hole0, hole1]
        nexts = []
        for i in range(len(hole[0])-1):  # loop sepanjang sawah
            #for debugging purpose
            #i=0
            dead = 0  # tidak berhenti
            status = 0  # status=0 -> sawah milik pemain
            hole_test = copy.deepcopy(hole)
            if hole_test[0][i] == 0:  # skip yang isinya 0
                continue
            if hole_test[0][i] == 9:
                delta_avg = []
                for j in range(6, 9):
                    seed = hole_test[0][i]  # ambil biji
                    hole_test[0][i] = 0  # sawah yang diambil jadi kosong
                    k = j
                    while dead == 0:  # jalan
                        if k != 6:  # tidak berada di ujung
                            k += 1  # pindah ke sawah sebelah
                            # habis, di sawah kosong milik sendiri (tembak)
                            if seed == 1 and status == 0 and hole_test[status][k] == 0:
                                hole_test[status][7] += hole_test[1][6-k]
                                hole_test[1][6-k] = 0
                                hole_test[status][k] = 1
                                seed -= 1
                                dead = 1  # keluar dari loop
                            # habis, di sawah kosong milik lawan (berhenti)
                            elif seed == 1 and status == 1 and hole_test[status][k] == 0:
                                hole_test[status][k] += 1
                                seed -= 1
                                dead = 1  # keluar dari loop
                            elif seed == 1:  # habis, tidak di sawah kosong, jalan terus
                                hole_test[status][k] += 1
                                seed = hole_test[status][k]
                                hole_test[status][k] = 0
                            else:  # jalan biasa
                                hole_test[status][k] += 1
                                seed -= 1

                        else:  # jika di ujung (sawah ke-7)
                            if seed == 1 and status == 0:  # berhenti di lumbung milik sendiri
                                hole_test[status][k+1] += 1
                                seed -= 1
                                dead = 1  # keluar dari loop
                            elif seed == 1 and status == 1:  # memindah perjalanan ketika habis
                                k = 0
                                status = 0
                                #hole_test[status][j]+=1
                                seed += hole_test[status][k]
                                hole_test[status][k] = 0
                            # memindah perjalanan ke sawah milik sendiri (agar tidak masuk lumbung lawan)
                            elif status == 1:
                                k = 0
                                status = 0
                                hole_test[status][k] += 1
                                seed -= 1
                            else:  # memindah perjalanan ke sawah milik lawan
                                hole_test[status][k+1] += 1
                                seed -= 1
                                status = 1
                                k = -1

                        delta = hole_test[0][7]-hole_test[1][7]
                        delta_avg.append(delta)

                    for l in range(len(delta_avg)):
                        delta += delta_avg[l]

                    delta = delta/len(delta_avg)
                    nexts.append([delta, i])
            else:
                seed = hole_test[0][i]  # ambil biji
                hole_test[0][i] = 0  # sawah yang diambil jadi kosong
                j = i
                while dead == 0:  # jalan

                    #for debugging purpose
                    '''
                    print("i =",i)
                    print("j =",j)
                    print("status =",status)
                    print("seed =",seed)
                    print(hole_test)
                    '''
                    if j != 6:  # tidak berada di ujung
                        j += 1  # pindah ke sawah sebelah
                        # habis, di sawah kosong milik sendiri (tembak)
                        if seed == 1 and status == 0 and hole_test[status][j] == 0:
                            hole_test[status][7] += hole_test[1][6-j]
                            hole_test[1][6-j] = 0
                            hole_test[status][j] = 1
                            seed -= 1
                            dead = 1  # keluar dari loop
                        # habis, di sawah kosong milik lawan (berhenti)
                        elif seed == 1 and status == 1 and hole_test[status][j] == 0:
                            hole_test[status][j] += 1
                            seed -= 1
                            dead = 1  # keluar dari loop
                        elif seed == 1:  # habis, tidak di sawah kosong, jalan terus
                            hole_test[status][j] += 1
                            seed = hole_test[status][j]
                            hole_test[status][j] = 0
                        else:  # jalan biasa
                            hole_test[status][j] += 1
                            seed -= 1

                    else:  # jika di ujung (sawah ke-7)
                        if seed == 1 and status == 0:  # berhenti di lumbung milik sendiri
                            hole_test[status][j+1] += 1
                            seed -= 1
                            dead = 1  # keluar dari loop
                        elif seed == 1 and status == 1:  # memindah perjalanan ketika habis
                            j = 0
                            status = 0
                            #hole_test[status][j]+=1
                            seed += hole_test[status][j]
                            hole_test[status][j] = 0
                        # memindah perjalanan ke sawah milik sendiri (agar tidak masuk lumbung lawan)
                        elif status == 1:
                            j = 0
                            status = 0
                            hole_test[status][j] += 1
                            seed -= 1
                        else:  # memindah perjalanan ke sawah milik lawan
                            hole_test[status][j+1] += 1
                            seed -= 1
                            status = 1
                            j = -1

                    #for debugging purpose
                    '''
                    print("after")
                    print(hole_test)
                    print("seed =",seed)
                    print()
                    '''
                    delta = hole_test[0][7]-hole_test[1][7]
                    nexts.append([delta, i])

            nexts.sort(reverse=True)

            #for debugging purpose
            #print("i= ",i)
            #print(hole_test)

            #for debugging purpose
            #print("delta = ",delta)
            #break

        #for debugging purpose
        #print(nexts)

        return nexts[0][1]
