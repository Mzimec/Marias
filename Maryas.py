'''
Marias - zakladni hra proti pocitaci
Stepan Svaty I. rocnik
zimni semestr 2022/23
Programming I
'''

import random #importujeme pro nahodne michani

# objekt karty, jmeno zkratkovite, barva(s,l,k,z), hodnota (od 7 do esa), trumfarna je hodnota, ve ktere je ulozeno jakou ma karta hodnotu pri voleni trumfu
class Karta:

    def __init__(self,hodnota,barva):
        self.hodnota = hodnota
        self.barva = barva
        self.jmeno = None
        self.trumfarna = 10


# objekt hrace: na tahu urcuje zacinajiciho hrace v kole, poradi urcuje, kdo je fort, ai zda je to ovladane programem, ruka seznam karet v ruce
class Hrac:

    def __init__(self,poradi):
        self.na_tahu = False
        self.poradi = poradi
        self.ai = True
        self.ruka = None


# funkce vytvori serazeny seznam karet a da jim jmena
def vytvor_balik():
    balicek = []
    for i in range(4):
        for j in range(7,15):
            a = Karta(j,i)
            if j == 10:
                a.jmeno = 'sp'
            elif j == 11:
                a.jmeno = 'sv'
            elif j == 12:
                a.jmeno = 'k'
            elif j == 13:
                a.jmeno = '10'
            elif j == 14:
                a.jmeno = 'e'
            else:
                a.jmeno = str(j)
            if i == 1:
                a.jmeno += ' s'
            elif i == 2:
                a.jmeno += ' l'
            elif i == 3:
                a.jmeno += ' k'
            else:
                a.jmeno += ' z'
            balicek.append(a)
    return balicek


#zamicha karty pomoci random funkce (nastavi jejich index nahodne)
def zamichej_balicek(balicek_a):
    balicek_b = []
    for _ in range(32):
        a = random.randint(0,len(balicek_a)-1)
        balicek_b.append(balicek_a[a])
        balicek_a.pop(a)
    return balicek_b

#vytiskne jmena karet daneho seznamu karet
def print_karty(karty):
    if len(karty) != 0:
        for i in range(len(karty)-1):
            print(karty[i].jmeno, end=', ')
        print(karty[len(karty)-1].jmeno)

#rozda prvni kolo karet hracum, prvnimu hraci 7 karet, ostatnim po peti
def prvni_rozdani(balicek):
    #prvni hrac dostava v prvnim rozdani o dve karty vice nez ostatni hraci
    a = balicek[:7]
    b = balicek[7:12]
    c = balicek[12:17]
    return a, b, c

#dorozda zbztek karet, vsem da po peti
def druhe_rozdani(balicek,a,b,c):
    a.extend(balicek[17:22])
    b.extend(balicek[22:27])
    c.extend(balicek[27:])
    return a, b, c

#srovna hracovi karty tak aby byly roydeleny do ctyr podseznamu barev, ve kterych serazeny vzestupne podle hodnoty
def srovnej_ruku(a):
    #ruka je seznam ctyr podseznamu, ktere odpovidaji seznamum karet hrace urcite barvy
    ruka = [[],[],[],[]]
    #priradime rozdane karty do ruky
    for i in range(len(a)):
        if type(a[i]) is list:
            ruka[i] = a[i]
        else:
            ruka[a[i].barva].append(a[i])
    #srovname ruku
    for i in range(4):
        ruka[i].sort(key=lambda x: x.hodnota)
    return ruka

#vytvori hrace a nahodne urci za koho hrajeme
def svolej_hrace():
    hraci = []
    for i in range(3):
        hraci.append(Hrac(i))
    hraci[random.randint(0,2)].ai = False
    return hraci

#vybira trumfy za AI hrace
def vyber_trumfy_AI(ruka):
    #promenne
    trumfy = 0
    #trumfy hodnota udavaji nejvyssi hodnotu z promennych barev
    trumfy_hodnota = 0
    for i in range(4):
        #barva udava soucet trumfaren vsech karet v dane barve
        barva = 0
        for j in range(len(ruka[i])):
            #zmenime hodnoty trumfarny pro dulezitejsi karty
            #eso
            if ruka[i][j].hodnota == 14:
                ruka[i][j].trumfarna = 14
                #desitka kdyz mame eso
                if ruka[i][j-1] and ruka[i][j-1].hodnota == 13:
                    ruka[i][j-1].trumfarna = 13
            #kral
            if ruka[i][j].hodnota == 12:
                ruka[i][j].trumfarna = 15
                #svrsek, kdzy mame krale
                if ruka[i][j-1] and ruka[i][j-1].hodnota == 11:
                    ruka[i][j-1].trumfarna = 25
            #svrsek
            elif ruka[i][j].hodnota == 11:
                ruka[i][j].trumfarna == 15
            barva += ruka[i][j].trumfarna
        #zmena trumfy_hodnota a nastaveni hodnoty trumfu
        if barva > trumfy_hodnota:
            trumfy_hodnota = barva
            trumfy = i
        elif barva == trumfy_hodnota and barva > 0:
            if ruka[i][-1].hodnota > ruka[trumfy][-1].hodnota:
                trumfy_hodnota =barva
                trumfy = i
    return trumfy

#UI pro vyber trumfu hrace
def vyber_trumfy_PC(ruka):
    #vypise karty v ruce
    for i in range(4):
        print_karty(ruka[i])
    #Dokud nezada hrac spravne trumfy
    while True:
        barva = input('Napis prvni pismeno barvy, ktere volis: ')
        if barva == 'z':
            return 0
        elif barva == 's':
            return 1
        elif barva == 'l':
            return 2
        elif barva == 'k':
            return 3
        else:
            print('Trumfy byly zadany chybne')

#vybere trumfy prvniho hrace a vypise co je za trumfy
def vyber_trumfy(hrac):
    if hrac.ai == True:
        trumfy = vyber_trumfy_AI(hrac.ruka)
    else:
        trumfy = vyber_trumfy_PC(hrac.ruka)
    if trumfy == 0:
        print("Trumfy jsou z")
    elif trumfy == 1:
        print("Trumfy jsou s")
    elif trumfy == 2:
        print("Trumfy jsou l")
    else:
        print("Trumfy jsou k")
    return trumfy

#vybere pocitaci v jakych barvach se vyplati vyhodit barvy
def zbav_se_barvy(hrac,a):
    #vztvori seznam hodnot barev, kam  se budou ukladat ty ktere jsou idealni na odstraneni a nakonec vzdy ulozi o jakou se jedna moznost vyhazovu
    barva_zbaveni = []
    #moznost 1, kdy mame dve netrumfove barvy delky 1
    if a.count(1) == 2:
        for i in range(4):
            if len(hrac.ruka[i]) == 1 and hrac.ruka[i][0].hodnota < 13 and i != trumfy:
                barva_zbaveni.append(i)
        if len(barva_zbaveni) == 2:
            barva_zbaveni.append(1)
            return barva_zbaveni
    #moznost 2, mame netrumfove barvy delky 2 a jedna, nejsou tam ani vysoke (az na potencialni eso u 2) ani hlaska
    if a.count(2) > 0 and a.count(1) > 0:
        for i in range(4):
            if len(hrac.ruka[i]) == 2 and i != trumfy and hrac.ruka[i][0].hodnota != 13 and hrac.ruka[i][1].hodnota != 13 and (hrac.ruka[i][0].hodnota != 11 or hrac.ruka[i][1].hodnota != 12):
                        barva_zbaveni.append(i)
            if len(hrac.ruka[i]) == 1 and hrac.ruka[i][0].hodnota < 13 and i != trumfy:
                barva_zbaveni.append(i)
        if len(barva_zbaveni) > 1:
            barva_zbaveni.append(2)
            return barva_zbaveni
    #moznost 3, mame netrumfovou barvu delky 2 nenjsou v ni vysoke ani hlaska
    if a.count(2) > 0:
        for i in range(4):
            if len(hrac.ruka[i]) == 2 and i != trumfy and (hrac.ruka[i][0].hodnota != 11 or hrac.ruka[i][1].hodnota != 12):
                good = True
                for j in range(2):
                    if hrac.ruka[i][j].hodnota > 12:
                        good = False
                if good == True:
                    barva_zbaveni.append(i)
        if len(barva_zbaveni) > 0:
            barva_zbaveni.append(3)
            return barva_zbaveni
    #moznost 4, netrumfovou barvu delky 1 a zadnou jinou kratsi nez 3, nejsou v ni vysoke 
    if a.count(1) > 0:
        for i in range(4):
            if len(hrac.ruka[i]) == 1 and hrac.ruka[i][0].hodnota < 13 and i != trumfy:
                barva_zbaveni.append(i)
        if len(barva_zbaveni) > 0:
            barva_zbaveni.append(4)
            return barva_zbaveni
    #moznost 5, mame netrumfovou barvu delky 3, kde neni desitka ani hlaska
    if a.count(3) > 0:
        for i in range(4):
            if len(hrac.ruka[i]) == 3 and i != trumfy and hrac.ruka[i][2].hodnota != 13:
                good = True
                for j in range(2):
                    if hrac.ruka[i][j].hodnota == 13 and (hrac.ruka[i][j].hodnota == 11 or hrac.ruka[i][j+1].hodnota == 12):
                        good = False
                if good == True:
                    barva_zbaveni.append(i)
        if len(barva_zbaveni) > 0:
            barva_zbaveni.append(5)
            return barva_zbaveni
    #moznost 6, mame jen dlouhe barvy
    barva_zbaveni.append(6)
    return barva_zbaveni


#funkce vybere talon za pocitac
def vyber_talon_AI(hrac):
    #vztvorime seznam delek barev
    delky_barev = []
    for i in range(4):
        delky_barev.append(len(hrac.ruka[i]))
    zbavit = zbav_se_barvy(hrac,delky_barev)
    #zjistime s jakou moznosti z zbav_se_barvy() pracujeme
    #moznost 1: vyhodime obe karty
    if zbavit[-1] == 1:
        hrac.ruka[zbavit[0]].pop(0)
        hrac.ruka[zbavit[1]].pop(0)
        return hrac
    #moznost 2: z kazde ze dvou moznych barev odstranime jednu kartu
    elif zbavit[-1] == 2:
        for i in range(len(zbavit[0:-1])):
            if len(hrac.ruka[zbavit[i]]) == 1:
                hrac.ruka[zbavit[i]].pop(0)
        for i in range(len(zbavit[0:-1])):
            if len(hrac.ruka[zbavit[i]]) == 2:
                hrac.ruka[zbavit[i]].pop(0)
                return hrac
    #moznost 3: odstrnime obe karty
    elif zbavit[-1] == 3:
        hrac.ruka[zbavit[0]].pop(0)
        hrac.ruka[zbavit[0]].pop(0)
        return hrac
    #moznost 4:
    elif zbavit[-1] == 4:
        for i in range(len(zbavit[0:-1])):
            #najdeme barvu s delkou jedna a odstranime z ni kartu
            if len(hrac.ruka[zbavit[i]]) == 1:
                hrac.ruka[zbavit[i]].pop(0)
        for i in range(4):
            #zbavi se nejnizsi karty z libovolne netrumfove nevysoke karty, ktera netvori hlasku
            if len(hrac.ruka[i]) > 2 and i != trumfy and (hrac.ruka[i][0].hodnota != 11 or hrac.ruka[i][1].hodnota != 12) and hrac.ruka[i][0].hodnota < 13:
                hrac.ruka[i].pop(0)
                return hrac
        #jinak se ybavi nejnizsiho trumfu, ktery neni vysoky a netvori hlasku
        if (hrac.ruka[trumfy][0].hodnota != 11 or hrac.ruka[trumfy][1].hodnota != 12) and hrac.ruka[trumfy][0].hodnota < 13:
                hrac.ruka[trumfy].pop(0)
                return hrac
        for i in range(4):
            #zbavi se nejnizsi karty z libovolne netrumfove nevysoke karty
            if len(hrac.ruka[i]) > 2 and i != trumfy and hrac.ruka[i][0].hodnota < 13:
                hrac.ruka[i].pop(0)
                return hrac
    #moznost 5: odhodis spodni dve karty
    elif zbavit[-1] == 5:
        hrac.ruka[zbavit[0]].pop(0)
        hrac.ruka[zbavit[0]].pop(0)
        return hrac
    else: #moznost 6
        #pocet odhozenych karet
        x=0
        for i in range(4):
           #odhodi netrumfovou nevyskou kartu, ktera netvori hlasku
           if len(hrac.ruka[i]) > 2 and i != trumfy and (hrac.ruka[i][0].hodnota != 11 or hrac.ruka[i][1].hodnota != 12) and hrac.ruka[i][0].hodnota < 13:
                hrac.ruka[i].pop(0)
                x+=1
                #pokud je to druha odhozena ukonci vyber
                if x == 2:
                    return hrac
                #opakujeme to same na tu samou barvu
                if (hrac.ruka[i][0].hodnota != 11 or hrac.ruka[i][1].hodnota != 12) and hrac.ruka[i][0].hodnota < 13:
                    hrac.ruka[i].pop(0)
                    return hrac
        #odhodi trumfovou nevyskou kartu, ktera netvori hlasku
        if len(hrac.ruka[trumfy]) > 2 and (hrac.ruka[trumfy][0].hodnota != 11 or hrac.ruka[trumfy][1].hodnota != 12) and hrac.ruka[trumfy][0].hodnota < 13:
                hrac.ruka[trumfy].pop(0)
                x+=1
                #pokud je to druha odhozena ukonci vyber
                if x == 2:
                    return hrac
                #opakujeme to same na tu samou barvu
                if (hrac.ruka[trumfy][0].hodnota != 11 or hrac.ruka[trumfy][1].hodnota != 12) and hrac.ruka[trumfy][0].hodnota < 13:
                    hrac.ruka[i].pop(0)
                    return hrac
        #odhodi netrumfovou nevyskou kartu, ktera netvori hlasku
        for i in range(4):
           if i != trumfy and len(hrac.ruka[i]) > 2 and hrac.ruka[i][0].hodnota < 13 and hrac.ruka[i][0].hodnota == 11 or hrac.ruka[i][1].hodnota == 12:
                hrac.ruka[i].pop(0)
                #pokud je to druha odhozena ukonci vyber
                if x == 2:
                    return hrac
                hrac.ruka[i].pop(0)
                return hrac

#funkce odhodi talon podle inputu hrace
def vyber_talon_PC(hrac):
    #vytiskne nam karty v ruce
    for i in range(4):
        print_karty(hrac.ruka[i])
    #chyba je true pokud uddelal hrac v zadavani karty chybu
    chyba = True
    #opkauje se dokud hrac nezada spravne kartu do talonu
    while chyba == True:
        #necha hrace vypsat kartu, kterou chce odhodit
        prvni = input("Napis jmeno prvni karty, kterou volis do talonu: ")
        #rozpozna barvu vyhozene karty
        if prvni[-1] == 'z':
            for i in range(len(hrac.ruka[0])):
                #projdeme jestli v dane barve mame zadanou kartu
                if hrac.ruka[0][i].jmeno == prvni and hrac.ruka[0][i].hodnota < 13:
                    #chybu nastavime,ze neni
                    chyba = False
                    #kartu odhodime
                    hrac.ruka[0].pop(i)
                    break
        elif prvni[-1] == 's':
            for i in range(len(hrac.ruka[1])):
                if hrac.ruka[1][i].jmeno == prvni and hrac.ruka[1][i].hodnota < 13:
                    chyba = False
                    hrac.ruka[1].pop(i)
                    break
        elif prvni[-1] == 'l':
            for i in range(len(hrac.ruka[2])):
                if hrac.ruka[2][i].jmeno == prvni and hrac.ruka[2][i].hodnota < 13:
                    chyba = False
                    hrac.ruka[2].pop(i)
                    break
        elif prvni[-1] == 'k':
            for i in range(len(hrac.ruka[3])):
                if hrac.ruka[3][i].jmeno == prvni and hrac.ruka[3][i].hodnota < 13:
                    chyba = False
                    hrac.ruka[3].pop(i)
                    break
        #pokud tam mame stale chybu
        if chyba == True:
            print("Prvni karta do talonu byla zadana spatne")
    #analogicky postup pro druhou kartu do talonu
    for i in range(4):
        print_karty(hrac.ruka[i])
    chyba = True
    while chyba == True:
        druha = input("Napis jmeno druhe karty, kterou volis do talonu: ")
        if druha[-1] == 'z':
            for i in range(len(hrac.ruka[0])):
                if hrac.ruka[0][i].jmeno == druha and hrac.ruka[0][i].hodnota < 13:
                    chyba = False
                    hrac.ruka[0].pop(i)
                    break
        elif druha[-1] == 's':
            for i in range(len(hrac.ruka[1])):
                if hrac.ruka[1][i].jmeno == druha and hrac.ruka[1][i].hodnota < 13:
                    chyba = False
                    hrac.ruka[1].pop(i)
                    break
        elif druha[-1] == 'l':
            for i in range(len(hrac.ruka[2])):
                if hrac.ruka[2][i].jmeno == druha and hrac.ruka[2][i].hodnota < 13:
                    chyba = False
                    hrac.ruka[2].pop(i)
                    break
        elif druha[-1] == 'k':
            for i in range(len(hrac.ruka[3])):
                if hrac.ruka[3][i].jmeno == druha and hrac.ruka[3][i].hodnota < 13:
                    chyba = False
                    hrac.ruka[3].pop(i)
                    break
        else:
            print("Druha karta do talonu byla zadana spatne")
    return hrac

#funkce vybere funkci odstranovani talou, bud AI nebo PC
def odstran_talon(hrac):
    #pro grace ovladane pocitacem
    if hrac.ai == True:
        return vyber_talon_AI(hrac)
    #pro hrace ovladane hracem
    else:
        return vyber_talon_PC(hrac)

    #odehraje druhou kartu stychu
def zahraj_prvni_kartu(hrac,pamet,stych,a,b,pocitadlo):
    #vypise odehranou kartu
    print(str(hrac.poradi+1)+". hrac je na tahu: " + hrac.ruka[a][b].jmeno)
    #pokud mame hlasku, pricte body
    if len(hrac.ruka[a]) > 1 and ((hrac.ruka[a][b] != hrac.ruka[a][-1] and hrac.ruka[a][b].hodnota == 11 and hrac.ruka[a][b+1].hodnota == 12) or (hrac.ruka[a][b] != hrac.ruka[a][0] and hrac.ruka[a][b].hodnota == 12 and hrac.ruka[a][b-1].hodnota == 11)):
        #netrumfova hlaska
        if a != trumfy:
            print("Hlaska")
            if hrac.poradi == 0:
                pocitadlo[0] += 20
            else:
                pocitadlo[1] += 20
        #trumfova hlaska
        else:
            print("Trumfova hlaska")
            if hrac.poradi == 0:
                pocitadlo[0] += 40
            else:
                pocitadlo[1] += 40
    #zapise kartu do pameti
    pamet[a][hrac.ruka[a][b].hodnota-7] = True
    #nastavi, kdo bere stych, prirozene na hrace, ktery vynasel
    stych[0] = hrac.ruka[a][b]
    #da kartu do stychu
    stych[3] = hrac.poradi
    #odhodi kartu z ruky hrace
    hrac.ruka[a].pop(b)
    return hrac, pamet, stych, pocitadlo

#odehraje druhou kartu stychu
def zahraj_druhou_kartu(hrac,pamet,stych,a,b,pocitadlo):
    #vypise odehranou kartu
    print(str(hrac.poradi+1)+". hrac je na tahu: " + hrac.ruka[a][b].jmeno)
    #pokud mame hlasku, pricte body
    if len(hrac.ruka[a]) > 1 and ((hrac.ruka[a][b] != hrac.ruka[a][-1] and hrac.ruka[a][b].hodnota == 11 and hrac.ruka[a][b+1].hodnota == 12) or (hrac.ruka[a][b] != hrac.ruka[a][0] and hrac.ruka[a][b].hodnota == 12 and hrac.ruka[a][b-1].hodnota == 11)):
        #netrumfova hlaska
        if a != trumfy:
            print("Hlaska")
            if hrac.poradi == 0:
                pocitadlo[0] += 20
            else:
                pocitadlo[1] += 20
        #trumfova hlaska
        else:
            print("Trumfova hlaska")
            if hrac.poradi == 0:
                pocitadlo[0] += 40
            else:
                pocitadlo[1] += 40
    #zapise kartu do pameti
    pamet[a][hrac.ruka[a][b].hodnota-7] = True
    #da kartu do stychu
    stych[1] = hrac.ruka[a][b]
    #odhodi kartu z ruky hrace
    hrac.ruka[a].pop(b)
    return hrac, pamet, stych, pocitadlo

#odehraje treti kartu stychu
def zahraj_treti_kartu(hrac,pamet,stych,a,b,pocitadlo):
    #vypise odehranou kartu
    print(str(hrac.poradi+1)+". hrac je na tahu: " + hrac.ruka[a][b].jmeno)
    #pokud mame hlasku, pricte body
    if len(hrac.ruka[a]) > 1 and ((hrac.ruka[a][b] != hrac.ruka[a][-1] and hrac.ruka[a][b].hodnota == 11 and hrac.ruka[a][b+1].hodnota == 12) or (hrac.ruka[a][b] != hrac.ruka[a][0] and hrac.ruka[a][b].hodnota == 12 and hrac.ruka[a][b-1].hodnota == 11)):
        #netrumfova hlaska
        if a != trumfy:
            print("Hlaska")
            if hrac.poradi == 0:
                pocitadlo[0] += 20
            else:
                pocitadlo[1] += 20
        #trumfova hlaska
        else:
            print("Trumfova hlaska")
            if hrac.poradi == 0:
                pocitadlo[0] += 40
            else:
                pocitadlo[1] += 40
    #zapise kartu do pameti
    pamet[a][hrac.ruka[a][b].hodnota-7] = True
    #da kartu do stychu
    stych[2] = hrac.ruka[a][b]
    #odhodi kartu z ruky hrace
    hrac.ruka[a].pop(b)
    return hrac, pamet, stych, pocitadlo

#funkce, ktera ovlada AI hrace, co maji zahrat,kdyz jsou prvni na rade
def vynes_kartu(hrac,pamet,stych,pocitadlo):
    #zbavujeme se esa a desitky
    for i in range(4):
        #ma kartu v barve i, ktera nejsou trumfy, nikomu barva nechybi snad
        if len(hrac.ruka[i]) > 0 and pamet[4][i] == False and pamet[5][i] == False and pamet[6][i] == False and i != trumfy and 6 > len(hrac.ruka[i])+pamet[i].count(True):
            #pokud jsi prvni hrac a oponenti maji barvu i
            if hrac.poradi == 0 and pamet[5][i] == False and pamet[6][i] == False and pamet[i].count(True) + len(hrac.ruka[i]) < 8:
                #mame barvu min delky dva, kde mame eso a deset, pak hrajeme eso
                if len(hrac.ruka[i]) > 1 and hrac.ruka[i][-2].hodnota == 13 and hrac.ruka[i][-1].hodnota == 14:
                    return zahraj_prvni_kartu(hrac,pamet,stych,i,-1,pocitadlo)
                #mame deset a eso uz slo
                elif hrac.ruka[i][-1].hodnota == 13 and pamet[i][-1] == True:
                    return zahraj_prvni_kartu(hrac,pamet,stych,i,-1,pocitadlo)
            #pokud nejsi prvni hrac a prvni hrac ma barvu i
            if hrac.poradi > 0 and pamet[4][i] == False and pamet[i].count(True) + len(hrac.ruka[i]) < 8:
                #mame barvu min delky dva, kde mame eso a deset, pak hrajeme eso
                if len(hrac.ruka[i]) > 1 and hrac.ruka[i][-2].hodnota == 13 and hrac.ruka[i][-1].hodnota == 14:
                    return zahraj_prvni_kartu(hrac,pamet,stych,i,-1,pocitadlo)
                #mame deset a eso uz slo
                elif hrac.ruka[i][-1].hodnota == 13 and pamet[i][-1] == True:
                    return zahraj_prvni_kartu(hrac,pamet,stych,i,-1,pocitadlo)
    #stouchnuti esa
    #stouchnuti esa
    for i in range(4):
        #mame netrumfovou barvu delky min 3 a desitku (nemame eso vylucuje se s prvni casti), hrajeme kartu pod deset, ykusime z oponenta vystouchnout eso
        if len(hrac.ruka[i]) > 2 and pamet[i][-1] != True and i != trumfy and hrac.ruka[i][-1].hodnota == 13:
            return zahraj_prvni_kartu(hrac,pamet,stych,i,-2,pocitadlo)
    #trumfni to
    #jsme akter, mame trumfy a lespon jeden oponent ma taky trumfy
    if hrac.poradi == 0 and len(hrac.ruka[trumfy]) > 0 and (pamet[5][trumfy] != True or pamet[6][trumfy] != True) and pamet[trumfy].count(True)+len(hrac.ruka[trumfy]) < 8:
        #pomocna promenna
        good = True
        #pro eso vzdy plati
        if hrac.ruka[trumfy][-1].hodnota != 14:
            for i in range(hrac.ruka[trumfy][-1].hodnota-6,8):
                #kontrola zda mame nejvyssi trumf
                if pamet[trumfy][i] == False:
                    good = False
                    break
        #mame nejvyssi trumf ve hre, zahrajeme ho, udrzime si pozici nad hrou
        if good == True:
            return zahraj_prvni_kartu(hrac,pamet,stych,trumfy,-1,pocitadlo)
    #vynos esa
    for i in range(4):
        #mam netrumfove eso oponenti snad barvu maji a nevim co dal, zkusim ulovit se stestim plonkovou desitku
        if i != trumfy and len(hrac.ruka[i]) > 0 and hrac.ruka[i][-1].hodnota == 14 and ((pamet[4][i] == False and pamet[5][i] == False and pamet[6][i] == False) or pamet[trumfy].count(True) + len(hrac.ruka[trumfy]) == 8):
            return zahraj_prvni_kartu(hrac,pamet,stych,i,-1,pocitadlo)
    #vytahovani trumfu z oponentu
    #jsem akter
    if hrac.poradi == 0:
        for i in range(4):
            #pokud ani jeden z oponentu nema barvu zahrajeme ji, ale neobetujem vysoke karty
            if i != trumfy and len(hrac.ruka[i]) > 0 and pamet[5][i] == True and pamet[6][i] == True and pamet[trumfy].count(True)+len(hrac.ruka[trumfy]) < 8 and hrac.ruka[i][0].hodnota < 13:
                return zahraj_prvni_kartu(hrac,pamet,stych,i,0,pocitadlo)
        for i in range(4):
            #pokud alespon jeden z oponentu nema barvu zahrajeme ji, ale neobetujem vysoke karty
            if i != trumfy and len(hrac.ruka[i]) > 0 and (pamet[5][i] == True or pamet[6][i] == True) and pamet[trumfy].count(True)+len(hrac.ruka[trumfy]) < 8 and hrac.ruka[i][0].hodnota < 13:
                return zahraj_prvni_kartu(hrac,pamet,stych,i,0,pocitadlo)
    #nejsme akter
    if hrac.poradi > 0:
        for i in range(4):
            #pokud kamarad ma barvu i, ale oponent nema a my neobetujem vysoke karty
            if i != trumfy and len(hrac.ruka[i]) > 0 and pamet[4][i] == True and pamet[5][i] == False and pamet[6][i] == False and pamet[4][trumfy] == False and hrac.ruka[i][0].hodnota < 13:
                return zahraj_prvni_kartu(hrac,pamet,stych,i,0,pocitadlo)
        for i in range(4):
            #pokud oponent ani spoluhrac nema, vytahneme trumfy z obou, ale neobetujem vysoke karty
            if i != trumfy  and len(hrac.ruka[i]) > 0 and pamet[4][i] == True and (pamet[5][i] == False or pamet[6][i] == False) and pamet[4][trumfy] == False and hrac.ruka[i][0].hodnota < 13:
                return zahraj_prvni_kartu(hrac,pamet,stych,i,0,pocitadlo)
    #jinak
    #pomocna promenna
    h = 0
    for i in range(4):
        #hledam nejdelsi netrumfovou barvu
        if i != trumfy and len(hrac.ruka[i]) > h:
            h = len(hrac.ruka[i])
    if h > 0:
        for i in range(4):
            #hraju plivu z nejdelsi netrumfove barvy
            if i != trumfy and len(hrac.ruka[i]) == h and hrac.ruka[i][0].hodnota < 13:
                return zahraj_prvni_kartu(hrac,pamet,stych,i,0,pocitadlo)
    for i in range(4):
        #plivu z libovolne netrumfove barvy
        if i != trumfy and len(hrac.ruka[i]) > 0 and hrac.ruka[i][0].hodnota < 13:
            return zahraj_prvni_kartu(hrac,pamet,stych,i,0,pocitadlo)
    #hraju nevysoky trumf
    if len(hrac.ruka[trumfy]) > 0 and hrac.ruka[trumfy][0].hodnota < 13:
        return zahraj_prvni_kartu(hrac,pamet,stych,trumfy,0,pocitadlo)
    #hraju libovolnou kartu z libovolne netrumfove barvy
    for i in range(4):
        if len(hrac.ruka[i]) > 0 and i != trumfy:
            return zahraj_prvni_kartu(hrac,pamet,stych,i,0,pocitadlo)
    #hraju libovolnou kartu z barvy, kterou jeste mam
    for i in range(4):
        if len(hrac.ruka[i]) > 0:
            return zahraj_prvni_kartu(hrac,pamet,stych,i,0,pocitadlo)

#funkce, ktera ovlada AI hrace, co maji zahrat,kdyz jsou druzi na rade
def druha_karta_stychu(hrac,pamet,stych,pocitadlo):
    #mam vynesenou barvu
    if len(hrac.ruka[stych[0].barva]) > 0:
            #Davam deset nebo eso jelikoz muzu
            #eso slo v predchozich stychach, nebo je v me ruce
            if (pamet[stych[0].barva][-1] == True and stych[0].hodnota != 14) or hrac.ruka[stych[0].barva][-1].hodnota == 14:
                #neni za mnou spoluhrac
                if hrac.poradi != 1:
                    #predpokladame ze ten za nami ma barvu stychu, nebo vime, ze nema trumfy
                    if pamet[((hrac.poradi+1)%3)+4][stych[0].barva] != False or pamet[stych[0].barva].count(True) + len(hrac.ruka[stych[0].barva]) < 8 or pamet[((hrac.poradi+1)%3)+4][trumfy] == True or pamet[stych[0].barva].count(True) + len(hrac.ruka[stych[0].barva]) == 8:
                        #mame eso, a desitka jiz sla
                        if hrac.ruka[stych[0].barva][-1].hodnota == 14 and pamet[stych[0].barva][-2] == True:
                            stych[3] = hrac.poradi
                            return zahraj_druhou_kartu(hrac,pamet,stych,stych[0].barva,-1,pocitadlo)
                        #mame desitku
                        if hrac.ruka[stych[0].barva][-1].hodnota == 13:
                            stych[3] = hrac.poradi
                            return zahraj_druhou_kartu(hrac,pamet,stych,stych[0].barva,-1,pocitadlo)
                #je za mnou spoluhrac
                else:
                    if hrac.ruka[stych[0].barva][-1].hodnota == 14 and pamet[stych[0].barva][-2] == True:
                        stych[3] = hrac.poradi
                        return zahraj_druhou_kartu(hrac,pamet,stych,stych[0].barva,-1,pocitadlo)
                    #mame desitku
                    if hrac.ruka[stych[0].barva][-1].hodnota == 13:
                        stych[3] = hrac.poradi
                        return zahraj_druhou_kartu(hrac,pamet,stych,stych[0].barva,-1,pocitadlo)
            #Nadhazuji
            for i in range(len(hrac.ruka[stych[0].barva])):
                #podminka, kdyz mam v ruce kartu s vetsi hodnotou nez prvni karta
                if hrac.ruka[stych[0].barva][i].hodnota > stych[0].hodnota:
                    stych[3] = hrac.poradi
                    return zahraj_druhou_kartu(hrac,pamet,stych,stych[0].barva,i,pocitadlo)
            #Jinak hraji nejnizsi kartu barvy
            return zahraj_druhou_kartu(hrac,pamet,stych,stych[0].barva,0,pocitadlo)
    #nemam barvu, ale mam trumf
    #nastavim pamet, ze nemam barvu
    if pamet[hrac.poradi+4][stych[0].barva] == False:
        pamet[hrac.poradi+4][stych[0].barva] == True
    #mam trumfy
    if len(hrac.ruka[trumfy]) > 0:
        stych[3] = hrac.poradi
        #uhravam deset
        if hrac.ruka[trumfy][-1].hodnota == 13 and pamet[trumfy][-1] == True:
            return zahraj_druhou_kartu(hrac,pamet,stych,trumfy,-1,pocitadlo)
        #jinak hraju nejnizsi trumf
        return zahraj_druhou_kartu(hrac,pamet,stych,trumfy,0,pocitadlo)
    #nemam chci namazat
    #nastavim pamet ze nemam trumfy
    if pamet[hrac.poradi+4][trumfy] == False:
        pamet[hrac.poradi+4][trumfy] == True
    #mam spoluhrace za sebou, ktery bud ma trumfy a nema barvu, nbo bylo zahrano jen par karet barvy
    if hrac.poradi == 1 and ((pamet[6][trumfy] == False and pamet[trumfy].count(True) < 8 and (pamet[6][stych[0].barva] == True or pamet[stych[0].barva].count(True) == 8)) or pamet[stych[0].barva].count(True)) < 5:
        for i in range(4):
            #namazu plonkovou desitku
            if len(hrac.ruka[i]) == 1 and hrac.ruka[i][0].hodnota == 13 and stych[0].barva != trumfy:
                return zahraj_treti_kartu(hrac,pamet,stych,i,0,pocitadlo)
        for i in range(4):
            #namazu desitku
            if len(hrac.ruka[i]) > 0 and hrac.ruka[i][-1].hodnota == 13 and stych[0].barva != trumfy:
                return zahraj_druhou_kartu(hrac,pamet,stych,i,-1,pocitadlo)
            #namzu eso
            elif len(hrac.ruka[i]) > 0 and hrac.ruka[i][-1].hodnota == 14 and pamet[i][-2] == True and stych[0].barva != trumfy:
                return zahraj_druhou_kartu(hrac,pamet,stych,i,-1,pocitadlo)
    #mam za sebou protihrace
    if hrac.poradi == 2:
        #pomocna promenna
        h = True
        #pokud prvni karta neni eso
        if stych[0].hodnota != 14:
            #prvni karta talonu byla nejvetsi dane barvy, ktera je jeste ve hre
            for i in range(stych[0].hodnota-6,8):
                if pamet[stych[0].barva][i] == False:
                    h = False
        #hrac za nami nema trumfy ani pravdepodobne barvu nebo prvni karta se neda prebyt a protihrac ma snad jeste barvu
        if ((pamet[4][trumfy] == True or pamet[trumfy].count(True) == 8) and (pamet[4][stych[0].barva] == True or pamet[stych[0].barva].count(True) > 7)) or (h == True and pamet[4][stych[0].barva] == False and pamet[stych[0].barva].count(True) < 7):
            for i in range(4):
                #namazu plonkovou desitku
                if len(hrac.ruka[i]) == 1 and hrac.ruka[i][0].hodnota == 13:
                    return zahraj_treti_kartu(hrac,pamet,stych,i,0,pocitadlo)
            for i in range(4):
                #namazu deset
                if len(hrac.ruka[i]) > 0 and hrac.ruka[i][-1].hodnota == 13:
                    return zahraj_druhou_kartu(hrac,pamet,stych,i,-1,pocitadlo)
                #namazu eso
                elif len(hrac.ruka[i]) > 0 and hrac.ruka[i][-1].hodnota == 14 and pamet[i][-2] == True:
                    return zahraj_druhou_kartu(hrac,pamet,stych,i,-1,pocitadlo)
    #jinak
    h = 0
    #hledam nejdelsi barvu
    for i in range(4):
        if len(hrac.ruka[i]) > h:
            h = len(hrac.ruka[i])
    #hraju nejslabsi kartu nejdelsiho retezce, ktera neni ma hodnotu mene nez deset
    for i in range(4):
        if len(hrac.ruka[i]) == h and hrac.ruka[i][0].hodnota < 13:
            return zahraj_druhou_kartu(hrac,pamet,stych,i,0,pocitadlo)
    #hraju nejslabsi kartu libovolne barvy, ktera ma nizsi hodnotu jak deset
    for i in range(4):
        if len(hrac.ruka[i]) > 0 and hrac.ruka[i][0].hodnota < 13:
            return zahraj_druhou_kartu(hrac,pamet,stych,i,0,pocitadlo)
    #hraju nejslabsi kartu
    for i in range(4):
        if len(hrac.ruka[i]) > 0:
            return zahraj_druhou_kartu(hrac,pamet,stych,i,0,pocitadlo)

#funkce, ktera ovlada AI hrace, co maji zahrat,kdyz jsou treti na rade
def treti_karta_stychu(hrac,pamet,stych,pocitadlo):
    #mam barvu
    if len(hrac.ruka[stych[0].barva]) > 0:
        #druha karta ma barvu stychu
        if stych[1].barva == stych[0].barva:
            #zadna karta stychu neni eso
            if stych[0].hodnota != 14 and stych[1].hodnota != 14:
                #mame deset te barvy hrajeme ji
                for i in range(len(hrac.ruka[stych[0].barva])):
                    if hrac.ruka[stych[0].barva][i].hodnota == 13:
                        stych[3] = hrac.poradi
                        return zahraj_treti_kartu(hrac,pamet,stych,stych[0].barva,i,pocitadlo)
                #mame eso barvy a deset uz slo, hrajeme ji
                if hrac.ruka[stych[0].barva][-1].hodnota == 14 and pamet[stych[0].barva][-2] == True:
                    stych[3] = hrac.poradi
                    return zahraj_treti_kartu(hrac,pamet,stych,stych[0].barva,-1,pocitadlo)
            #stych bere muj kamarad
            if stych[3] > 0 and hrac.poradi > 0:
                #mam deset barvy stychu, dam mu ji tam
                for i in range(len(hrac.ruka[stych[0].barva])):
                    if hrac.ruka[stych[0].barva][i].hodnota == 13:
                        return zahraj_treti_kartu(hrac,pamet,stych,stych[0].barva,i,pocitadlo)
            #nadhazuji
            for i in range(len(hrac.ruka[stych[0].barva])):
                #jestli mam kartu barvy s hodnotou vyssi nez protihraci, beru
                if hrac.ruka[stych[0].barva][i].hodnota > stych[1].hodnota and hrac.ruka[stych[0].barva][i].hodnota > stych[0].hodnota:
                    stych[3] = hrac.poradi
                    return zahraj_treti_kartu(hrac,pamet,stych,stych[0].barva,i,pocitadlo)
            #jinak podhazuji nejslabsi kartu barvy
            return zahraj_treti_kartu(hrac,pamet,stych,stych[0].barva,0,pocitadlo)
        #druhy hrac hral trumfy
        elif stych[1].barva == trumfy:
            #stych bere muj kamarad
            if stych[3] > 0 and hrac.poradi > 0:
                #mam deset barvy, hraju ji
                for i in range(len(hrac.ruka[stych[0].barva])):
                    if hrac.ruka[stych[0].barva][i].hodnota == 13:
                        return zahraj_treti_kartu(hrac,pamet,stych,stych[0].barva,i,pocitadlo)
                #mam eso barvy a deset jiz slo, hraju ji
                if hrac.ruka[stych[0].barva][-1].hodnota == 14 and pamet[stych[0].barva][-2] == True:
                    return zahraj_treti_kartu(hrac,pamet,stych,stych[0].barva,-1,pocitadlo)
            #odhazuji nejslabsi kartu barvy
            return zahraj_treti_kartu(hrac,pamet,stych,stych[0].barva,0,pocitadlo)
        #druhy hrac shazoval
        else:
            #prvni karta nebyla eso
            if stych[0].hodnota != 14:
                #mam deset hraji ji
                for i in range(len(hrac.ruka[stych[0].barva])):
                    if hrac.ruka[stych[0].barva][i].hodnota == 13:
                        stych[3] = hrac.poradi
                        return zahraj_treti_kartu(hrac,pamet,stych,stych[0].barva,i,pocitadlo)
                #mam eso a deset jiz slo, hraji ho
                if hrac.ruka[stych[0].barva][-1].hodnota == 14 and pamet[stych[0].barva][-2] == True:
                    stych[3] = hrac.poradi
                    return zahraj_treti_kartu(hrac,pamet,stych,stych[0].barva,-1,pocitadlo)
            #stych jde za kamaradem, muzu zahrat deset
            if stych[3] > 0 and hrac.poradi > 0:
                for i in range(len(hrac.ruka[stych[0].barva])):
                    if hrac.ruka[stych[0].barva][i].hodnota == 13:
                        return zahraj_treti_kartu(hrac,pamet,stych,stych[0].barva,i,pocitadlo)
            #hledam hodnotu vetsi nez byla hodnota prvni karty
            for i in range(len(hrac.ruka[stych[0].barva])):
                if hrac.ruka[stych[0].barva][i].hodnota > stych[0].hodnota:
                    stych[3] = hrac.poradi
                    return zahraj_treti_kartu(hrac,pamet,stych,stych[0].barva,i,pocitadlo)
            #jinak odhayuji nejslabsi kartu barvy
            return zahraj_treti_kartu(hrac,pamet,stych,stych[0].barva,0,pocitadlo)
    #mam trumfy, nemam barvu
    #nastavim pamet, ze nemam barvu
    if pamet[hrac.poradi+4][stych[0].barva] == False:
        pamet[hrac.poradi+4][stych[0].barva] == True
    #mam trumfy
    if len(hrac.ruka[trumfy]) > 0:
        #mam deset a eso jeste neslo, uhraji ji
        if pamet[trumfy][-1] != True and hrac.ruka[trumfy][-1].hodnota == 13 and (stych[1].barva != trumfy or stych[1].hodnota != 14):
            stych[3] = hrac.poradi
            return zahraj_treti_kartu(hrac,pamet,stych,trumfy,-1,pocitadlo)
        #druhy hrac nehral trumfy, hraji nejslabsi trumf
        elif stych[1].barva != trumfy:
            stych[3] = hrac.poradi
            return zahraj_treti_kartu(hrac,pamet,stych,trumfy,0,pocitadlo)
        #druhy hrac hral trumfy
        else:
            #hledam hodnotu, kterou ho nadhodim
            for i in range(len(hrac.ruka[trumfy])):
                if hrac.ruka[trumfy][i].hodnota > stych[1].hodnota:
                    stych[3] = hrac.poradi
                    return zahraj_treti_kartu(hrac,pamet,stych,trumfy,i,pocitadlo)
            #jinak podhazuji nejslabsim trumfem
            return zahraj_treti_kartu(hrac,pamet,stych,trumfy,0,pocitadlo)
    #nemam nic
    #nastavim pamet, ze nemam trumfy
    if pamet[hrac.poradi+4][trumfy] == False:
        pamet[hrac.poradi+4][trumfy] == True
    #stych bere kamarad
    if stych[3] > 0 and hrac.poradi > 0:
        for i in range(4):
            #mam danou barvu
            if len(hrac.ruka[i]) > 0:
                #zabvuji se plonkove desitky
                for j in range(len(hrac.ruka[i])):
                    if hrac.ruka[i][j].hodnota == 13 and len(hrac.ruka[i]) == 1:
                        return zahraj_treti_kartu(hrac,pamet,stych,i,j,pocitadlo)
                #mazu deset
                for j in range(len(hrac.ruka[i])):
                    if hrac.ruka[i][j].hodnota == 13:
                        return zahraj_treti_kartu(hrac,pamet,stych,i,j,pocitadlo)
                #mazu eso jestli deset uz sla
                if hrac.ruka[i][-1].hodnota == 14 and pamet[i][-2] == True:
                    return zahraj_treti_kartu(hrac,pamet,stych,i,-1,pocitadlo)
    #nemuzu namazat
    #pomocna promenna
    h = 0
    #hledam nejdelsi barvu
    for i in range(4):
        if len(hrac.ruka[i]) > h:
            h = len(hrac.ruka[i])
    if h > 0:
        #hraju nejslabsi nevysokou kartu z nejslabsi barvy
        for i in range(4):
            if len(hrac.ruka[i]) == h and hrac.ruka[i][0].hodnota < 13:
                return zahraj_treti_kartu(hrac,pamet,stych,i,0,pocitadlo)
    #hraju nejslabsi nevysokou kartu z libovolne barvy
    for i in range(4):
        if len(hrac.ruka[i]) > 0 and hrac.ruka[i][0].hodnota < 13:
            return zahraj_treti_kartu(hrac,pamet,stych,i,0,pocitadlo)
    #hraju nejslabsi kartu z libovolne barvy
    for i in range(4):
        if len(hrac.ruka[i]) > 0:
            return zahraj_treti_kartu(hrac,pamet,stych,i,0,pocitadlo)

#funkce spracuje input hrace, kdyz je prvni na rade
def pc_hraje_prvni(hrac,pamet,stych,pocitadlo):
    print("Jsi na tahu!")
    #vypise karty v ruce
    for i in range(4):
        print_karty(hrac.ruka[i])
    #trva dokud hrac nezada kartu, kterou muze zahrat
    while True:
        zahrat = input("Napis jmeno karty, kterou chces zahrat: ")
        if len(zahrat) > 0:
            if zahrat[-1] == 'z':
                for i in range(len(hrac.ruka[0])):
                    if hrac.ruka[0][i].jmeno == zahrat:                  
                        return zahraj_prvni_kartu(hrac,pamet,stych,0,i,pocitadlo)
            elif zahrat[-1] == 's':
                for i in range(len(hrac.ruka[1])):
                    if hrac.ruka[1][i].jmeno == zahrat:
                        return zahraj_prvni_kartu(hrac,pamet,stych,1,i,pocitadlo)
            elif zahrat[-1] == 'l':
                for i in range(len(hrac.ruka[2])):
                    if hrac.ruka[2][i].jmeno == zahrat:
                        return zahraj_prvni_kartu(hrac,pamet,stych,2,i,pocitadlo)
            elif zahrat[-1] == 'k':
                for i in range(len(hrac.ruka[3])):
                    if hrac.ruka[3][i].jmeno == zahrat:
                        return zahraj_prvni_kartu(hrac,pamet,stych,3,i,pocitadlo)
        print("Karta nebyla zahrana podle pravidel.")

# funkce kontrolujici zda hrac nezadal chybne kartu, kdyz je druhy na rade a uklada do pameti zda hrac ma dane barvy ci ne.
def korekce_dva(hrac,pamet,stych,pocitadlo,a,b):
    for i in range(len(hrac.ruka[a])):
                #mam kartu v ruce
                if hrac.ruka[a][i].jmeno == b:
                    #hraju kartu v barve stychu
                    if stych[0].barva == a:
                        #nadhazuji
                        if stych[0].hodnota < hrac.ruka[a][i].hodnota:
                            stych[3] = hrac.poradi
                            return zahraj_druhou_kartu(hrac,pamet,stych,a,i,pocitadlo)
                        #podhazuji
                        else:
                            for j in range(i,len(hrac.ruka[a])):
                                #kontrola jestli neexistuje karta, s kterou bzch mohl nadhodit
                                if hrac.ruka[a][j].hodnota > stych[0].hodnota:
                                    #chybovy return
                                    return 0,0,0,0
                            return zahraj_druhou_kartu(hrac,pamet,stych,a,i,pocitadlo)
                    #nemam barvu stychu a hraji trumfy
                    elif len(hrac.ruka[stych[0].barva]) == 0 and a == trumfy:
                        stych[3] = hrac.poradi
                        #nastavim pamet, ze nemam barvu stychu
                        if pamet[hrac.poradi][stych[0].barva] == False:
                            pamet[hrac.poradi][stych[0].barva] = True
                        return zahraj_druhou_kartu(hrac,pamet,stych,a,i,pocitadlo)
                    elif len(hrac.ruka[stych[0].barva]) == 0 and len(hrac.ruka[trumfy]) == 0:
                        #nastavim pamet, ze nemam barvu stychu
                        if pamet[hrac.poradi][stych[0].barva] == False:
                            pamet[hrac.poradi][stych[0].barva] = True
                        #nastavim pamet, ze nemam trumfy
                        if pamet[hrac.poradi][trumfy] == False:
                            pamet[hrac.poradi][trumfy] = True
                        return zahraj_druhou_kartu(hrac,pamet,stych,a,i,pocitadlo)
                    #chybovy return
                    return 0,0,0,0
    #chybovy return
    return 0,0,0,0

#funkce spracuje input hrace, kdyz je druhy na rade
def pc_hraje_druhy(hrac,pamet,stych,pocitadlo):
    print("Jsi na tahu!")
    #vypise ruku
    for i in range(4):
        print_karty(hrac.ruka[i])
    #dokud hrac nezada spravne kartu
    while True:
        #input hrace jakou chce hrat kartu
        zahrat = input("Napis jmeno karty, kterou chces zahrat: ")
        if len(zahrat) > 0:
            if zahrat[-1] == 'z':
                a,b,c,d = korekce_dva(hrac,pamet,stych,pocitadlo,0,zahrat)
                if a != 0:
                    return a,b,c,d
            elif zahrat[-1] == 's':
                a,b,c,d = korekce_dva(hrac,pamet,stych,pocitadlo,1,zahrat)
                if a != 0:
                    return a,b,c,d
            elif zahrat[-1] == 'l':
                a,b,c,d = korekce_dva(hrac,pamet,stych,pocitadlo,2,zahrat)
                if a != 0:
                    return a,b,c,d
            elif zahrat[-1] == 'k':
                a,b,c,d = korekce_dva(hrac,pamet,stych,pocitadlo,3,zahrat)
                if a != 0:
                    return a,b,c,d
        print("Karta nebyla zahrana podle pravidel.")
#funkce kontrolujici zda hrac nezadal chybne kartu, kdyz je treti na rade a uklada do pameti zda hrac ma dane barvy ci ne.
def korekce_tri(hrac,pamet,stych,pocitadlo,a,b):
    for i in range(len(hrac.ruka[a])):
                #mame kartu v ruce
                if hrac.ruka[a][i].jmeno == b:
                    # hrajem karty v barve stychu
                    if stych[0].barva == a:
                        #druha karta stychu je v barve stychu
                        if stych[0].barva == stych[1].barva:
                            #nadhazujeme
                            if stych[1].hodnota < hrac.ruka[a][i].hodnota and stych[0].hodnota < hrac.ruka[a][i].hodnota:
                                stych[3] = hrac.poradi
                                return zahraj_treti_kartu(hrac,pamet,stych,a,i,pocitadlo)
                            #podhazujeme
                            else:
                                #kontrola jestli v ruce neni karta s hodnotou, abzchom mohli nadhodit
                                for j in range(i,len(hrac.ruka[a])):
                                    if hrac.ruka[a][j].hodnota > stych[1].hodnota and stych[0].hodnota < hrac.ruka[a][i].hodnota:
                                        #chybovy return
                                        return 0,0,0,0
                                return zahraj_treti_kartu(hrac,pamet,stych,a,i,pocitadlo)
                        #druhy hrac hral trumfy
                        elif stych[1].barva == trumfy:
                            return zahraj_treti_kartu(hrac,pamet,stych,a,i,pocitadlo)
                        #druhy hrac shazoval
                        else:
                            #nadhazujeme
                            if stych[0].hodnota < hrac.ruka[a][i].hodnota:
                                stych[3] = hrac.poradi
                                return zahraj_treti_kartu(hrac,pamet,stych,a,i,pocitadlo)
                            #podhazujeme
                            else:
                                #kontrola jestli v ruce neni karta s hodnotou, abychom mohli nadhodit
                                for j in range(i,len(hrac.ruka[a])):
                                    if hrac.ruka[a][j].hodnota > stych[0].hodnota:
                                        #chybovy return
                                        return 0,0,0,0
                                return zahraj_treti_kartu(hrac,pamet,stych,a,i,pocitadlo)
                    # nemame barvu, ale hrajeme trumfy
                    elif len(hrac.ruka[stych[0].barva]) == 0 and a == trumfy:
                        #druhy hrac hral kartu stychu
                        if stych[0].barva == stych[1].barva:
                            stych[3] = hrac.poradi
                            # nastavim pamet, ze nemam barvu
                            if pamet[hrac.poradi+4][stych[0].barva] == False:
                                pamet[hrac.poradi+4][stych[0].barva] = True
                            return zahraj_treti_kartu(hrac,pamet,stych,a,i,pocitadlo)
                        #druhy hrac hral tez trumfovou kartu
                        elif stych[1].barva == trumfy:
                            #nadhazuji
                            if stych[1].hodnota < hrac.ruka[a][i].hodnota:
                                stych[3] = hrac.poradi
                                # nastavim pamet, ze nemam barvu
                                if pamet[hrac.poradi+4][stych[0].barva] == False:
                                    pamet[hrac.poradi+4][stych[0].barva] = True
                                return zahraj_treti_kartu(hrac,pamet,stych,a,i,pocitadlo)
                            #podhazuji
                            else:
                                #kontrola, zda bych nemohl propadne nadhodit
                                for j in range(i,len(hrac.ruka[a])):
                                    if hrac.ruka[a][j].hodnota > stych[1].hodnota:
                                        #chybovy return
                                        return 0,0,0,0
                                # nastavim pamet, ze nemam barvu
                                if pamet[hrac.poradi+4][stych[0].barva] == False:
                                    pamet[hrac.poradi+4][stych[0].barva] = True
                                return zahraj_treti_kartu(hrac,pamet,stych,a,i,pocitadlo)
                        #druhy hrac shazoval, tedy beru
                        else:
                            stych[3] = hrac.poradi
                            # nastavim pamet, ze nemam barvu
                            if pamet[hrac.poradi+4][stych[0].barva] == False:
                                pamet[hrac.poradi+4][stych[0].barva] = True
                            return zahraj_treti_kartu(hrac,pamet,stych,a,i,pocitadlo)
                    #nemam ani trumfy ani stychovou barvu, musim shazovat
                    if len(hrac.ruka[stych[0].barva]) == 0 and len(hrac.ruka[trumfy]) == 0:
                        # nastavim pamet, ze nemam barvu
                        if pamet[hrac.poradi+4][stych[0].barva] == False:
                            pamet[hrac.poradi+4][stych[0].barva] = True
                        #nastavim pamet, ze nemam trumfy
                        if pamet[hrac.poradi+4][trumfy] == False:
                            pamet[hrac.poradi+4][trumfy] = True
                        return zahraj_treti_kartu(hrac,pamet,stych,a,i,pocitadlo)
                    #chybovy return
                    return 0,0,0,0
    #chybovy return
    return 0,0,0,0

#funkce spracuje input hrace, kdyz je treti na rade
def pc_hraje_treti(hrac,pamet,stych,pocitadlo):
    print("Jsi na tahu!")
    #vypise karty v ruce
    for i in range(4):
        print_karty(hrac.ruka[i])
    #trva dokud hrac nezada kartu, kterou muze zahrat
    while True:
        zahrat = input("Napis jmeno karty, kterou chces zahrat: ")
        if len(zahrat) > 0:
            if zahrat[-1] == 'z':
                a,b,c,d = korekce_tri(hrac,pamet,stych,pocitadlo,0,zahrat)
                if a != 0:
                    return a,b,c,d
            elif zahrat[-1] == 's':
                a,b,c,d = korekce_tri(hrac,pamet,stych,pocitadlo,1,zahrat)
                if a != 0:
                    return a,b,c,d
            elif zahrat[-1] == 'l':
                a,b,c,d = korekce_tri(hrac,pamet,stych,pocitadlo,2,zahrat)
                if a != 0:
                    return a,b,c,d
            elif zahrat[-1] == 'k':
                a,b,c,d = korekce_tri(hrac,pamet,stych,pocitadlo,3,zahrat)
                if a != 0:
                    return a,b,c,d
        print("Karta nebyla zahrana podle pravidel.")

#funkce, ktera ovlada prubeh hry, delku stychy, kdo ziskava body...
def hrajeme(hraci):
    #pamet prvni 4 podseznamy ukladaji karty, ktere uz hrou prosli, jednotlive podseznamy patri dane barve, posledni tri podseznamy patri jednotlivym hracum a uklada se do nich zda jeste maji  urcitou barvu
    pamet = [[False]*8,[False]*8,[False]*8,[False]*8,[False]*4,[False]*4,[False]*4]
    #seznam do ktereho se ukladaji body jednotlivych tymu
    pocitadlo = [0,0]
    #nastavi aktera jako hrace, ktery ma byt na tahu
    hraci[0].na_tahu = True
    #hra vzdy trva deset stychu
    for i in range(10):
        #Vypise kolikaty je stych
        print("Zacina "+str(i+1)+". stych")
        #nastavi stych na neurcito
        stych = [0,0,0,0]
        #pro testovani
        '''for j in range(3):
            for k in range(4):
                print_karty(hraci[j].ruka[k])'''
        #najde hrace na tahu
        for j in range(3):
            if hraci[j].na_tahu:
                hraci[j].na_tahu = False
                stych[3] = j
                #urci jak ma hrat prvni hrac
                if hraci[j].ai == True:
                    hraci[j],pamet,stych,pocitadlo = vynes_kartu(hraci[j],pamet,stych,pocitadlo)
                else:
                    hraci[j],pamet,stych,pocitadlo = pc_hraje_prvni(hraci[j],pamet,stych,pocitadlo)
                #urci jak ma hrat druhy hrac
                if hraci[(j+1)%3].ai == True:
                    hraci[(j+1)%3],pamet,stych,pocitadlo = druha_karta_stychu(hraci[(j+1)%3],pamet,stych,pocitadlo)
                else:
                    hraci[(j+1)%3],pamet,stych,pocitadlo = pc_hraje_druhy(hraci[(j+1)%3],pamet,stych,pocitadlo)
                #urci jak ma hrat treti hrac
                if hraci[(j+2)%3].ai == True:
                    hraci[(j+2)%3],pamet,stych,pocitadlo = treti_karta_stychu(hraci[(j+2)%3],pamet,stych,pocitadlo)
                else:
                    hraci[(j+2)%3],pamet,stych,pocitadlo = pc_hraje_treti(hraci[(j+2)%3],pamet,stych,pocitadlo)
        #stych nebere akter
        if stych[3] > 0:
            for i in range(3):
                #pricita body za desitky a esa do pocitadla
                if stych[i].hodnota > 12:
                    pocitadlo[1] += 10
        #stych bere akter
        else:
            for i in range(3):
                #pricita body za desitky a esa do pocitadla
                if stych[i].hodnota > 12:
                    pocitadlo[0] += 10
        #nastavi hrace na tahu na toho, kdo bral stych
        hraci[stych[3]].na_tahu = True
    #pripocita poslednich 10 bodu hraci, ktery bral posledni stych
    for i in range(3):
        if hraci[i].na_tahu:
            if i > 0:
                pocitadlo[1] += 10
            else:
                pocitadlo[0] += 10
    return pocitadlo

#funkce vypise, kdo je vitez a jake bylo vyseldne skore
def a_vitezem_je(hraci,pocitadlo):
    for i in range(3):
        #najde PC hrace
        if hraci[i].ai == False:
            #vypise mu vysledky, aby byly citelne
            if i > 0:
                if pocitadlo[1] > pocitadlo[0]:
                    print("Vyhral jsi: " + str(pocitadlo[1]) + ":" + str(pocitadlo[0])+"!")
                else:
                    print("Prohral jsi: " + str(pocitadlo[1]) + ":" + str(pocitadlo[0])+"!")
            else:
                if pocitadlo[0] > pocitadlo[1]:
                    print("Vyhral jsi: " + str(pocitadlo[0]) + ":" + str(pocitadlo[1])+"!")
                else:
                    print("Prohral jsi: " + str(pocitadlo[0]) + ":" + str(pocitadlo[1])+"!")
    
            
#vytvorime hrace
hraci = svolej_hrace()
#vytvorime karty
balicek = vytvor_balik()
#zamichame karty
balicek = zamichej_balicek(balicek)
#vypiseme hraci kolikaty je pro prehldnost, aby bylo jasne s kym hraje
for i in range(3):
   if hraci[i].ai == False:
       print("Jsi "+str(hraci[i].poradi+1)+". hrac.")
#probehne prvni kolo rozdani karet    
hraci[0].ruka, hraci[1].ruka, hraci[2].ruka = prvni_rozdani(balicek)
#srovname rozdane karty
for i in range(3):
    hraci[i].ruka = srovnej_ruku(hraci[i].ruka)
#vyberou se trumfy
trumfy = vyber_trumfy(hraci[0])
#probehne druhe rozdani karet
hraci[0].ruka, hraci[1].ruka, hraci[2].ruka = druhe_rozdani(balicek, hraci[0].ruka, hraci[1].ruka, hraci[2].ruka)
#srovname ruce hracu
for i in range(3):
    hraci[i].ruka = srovnej_ruku(hraci[i].ruka)

#odhodi se talon
hraci[0] = odstran_talon(hraci[0])
#prubeh hry
pocitadlo = hrajeme(hraci)
#vyhodnoceni hry
a_vitezem_je(hraci,pocitadlo)

