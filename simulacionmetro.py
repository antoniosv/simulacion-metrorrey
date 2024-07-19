import math
import random
import time
class Metro:
    def __init__(self):
        self.cola = [[],[],[]]
        [self.cola.append(0) for _ in xrange(12)]
        self.deployed = 0

class Tren:
    def __init__(self, aidi):
        self.clientes = [0 for _ in xrange(12)]
        self.capacidad = [36, 28, 20, 20, 28, 36]
        self.capacidad = [40, 32, 24, 24, 32, 40]
        for i in range(0, len(self.capacidad)):
            self.capacidad.append(self.capacidad[i])
        self.estacion = -1
        self.movimiento = None
        self.tMov = 9999
        self.key = aidi        

    def subirPasajero(self, vagon, cantidad):
        if self.capacidad[vagon] >= self.clientes[vagon]+cantidad:
            self.clientes[vagon]+= cantidad
            return True
        else:
            return False

    def bajarPasajero(self, vagon, cantidad):
        if self.clientes[vagon]-cantidad >= 0:        
            self.clientes[vagon]-= cantidad
            return True
        else:
            return False

def TLL(lambd):
    return random.expovariate(lambd)*(23/lambd)
    #return random.random()*10

def servicio(mean, sigma):
    return random.gauss(mean, sigma)
    #return (random.random()*5) +15

def incrementTET(TET, d, cola):
    for i in cola:
        for j in i:
            TET = TET + (j*d)
    return TET

def simular(inter, rec, verbose):

    #### Parametros de Simulacion ####
    reloj = 0
    limite = 7200
    intervalo = inter
    recuperacion = rec
    ############################################

    #### Variables Endogenas ####
    TET = 0
    NCLL = 0
    NCE = [[0]for _ in xrange(3)]
    TEM = 0
    #############################
    
    #### Datos del Sistema ####
    TT = [84, 66] # tiempo de transportacion
    unidades=11

    ###########################

    #### Parametros de las variables aleatorias ####
    lambd = 2.94
    mean = 18.2
    sigma = 2.71

    ################################################


    cola = [[],[],[]]
    for c in cola:
        [c.append(0) for _ in xrange(12)]
    top = 9999
    TS = top
    TLE = top
    TLL1 = TLL(lambd)
    TLL2 = TLL(lambd)
    TLL3 = TLL(lambd)
    TLT = intervalo
    TRT = recuperacion
    sistema = Metro()
    tren = Tren(sistema.deployed)
    sistema.deployed+=1
    flag = False
    olvidados = 0
    while reloj <= limite:
        delta = min([TLL1, TLL2, TLL3, TS, TLT, TLE, TRT])
        reloj+= delta
        
        if flag:
            #wait = raw_input("PRESS TO CONTINUE")
            flag = False
        TET = incrementTET(TET, delta, cola)

        TLL1 -= delta
        TLL2 -= delta
        TLL3 -= delta
        TLE -= delta
        TLT -= delta
        TS -= delta

        if TLL1==0:
            NCLL+=1
            cola[0][cola[0].index(min(cola[0]))]+=1
            TLL1 = TLL(lambd)

        if TLL2==0:
            NCLL+=1
            cola[1][cola[1].index(min(cola[1]))]+=1
            TLL2 = TLL(lambd)

        if TLL3==0:
            NCLL+=1
            cola[2][cola[2].index(min(cola[2]))]+=1
            TLL3 = TLL(lambd)

        if TLT==0:
            if unidades > 0:
                tren.estacion=0
                tren.movimiento = False
                unidades-=1
                TLT = intervalo
                TS = servicio(mean, sigma)        
                flag = True
            else:
                TLT = TRT+1
            
        if TLE==0:
            tren.estacion+=1
            tren.movimiento = False
            TS = servicio(mean, sigma)
            TLE = top

        if TS==0:
            for vagon in range(0, len(tren.capacidad)):
                capacidad = tren.capacidad[vagon]
                abordo = tren.clientes[vagon]
                cupo = capacidad - abordo
                esperando = cola[tren.estacion][vagon]
                if cupo >= esperando:
                    tren.clientes[vagon]+= esperando
                    cola[tren.estacion][vagon] -= esperando
                else:
                    suben = esperando - cupo
                    tren.clientes[vagon]+= suben
                    cola[tren.estacion][vagon] -= suben
                    olvidados += cola[tren.estacion][vagon]
            NCE[tren.estacion].append(olvidados)
            olvidados = 0
            if tren.estacion==0 or tren.estacion==1:
                TLE = TT[tren.estacion]        
                tren.movimiento = True
                #flag = True
            else:
                tren = Tren(sistema.deployed)
                sistema.deployed+=1                
            TS = top

        TRT -= delta
        if TRT==0:
            unidades+=1
            TRT=recuperacion
            flag = True

        if verbose:
            print 'Reloj: ', '{0:.2f}'.format(reloj), ' de ', limite
            print 'Tiempos: TLL1 ', '{0:.2f}'.format(TLL1), '\tTLL2 ', '{0:.2f}'.format(TLL2), '\tTLL3 ', '{0:.2f}'.format(TLL3)
            print 'TS: ', '{0:.2f}'.format(TS), '\tTLT ','{0:.2f}'.format(TLT), '\tTLE ', '{0:.2f}'.format(TLE), '\nTRT ', '{0:.2f}'.format(TRT)
            print 'Unidades:', unidades, '\tEstacion ', tren.estacion, '\tID: ', tren.key
            print 'Estacion 1: ', cola[0], '\n\tNo abordaron:', NCE[0][tren.key]
            print 'Estacion 2: ', cola[1], '\n\tNo abordaron:', NCE[1][tren.key]
            print 'Estacion 3: ', cola[2], '\n\tNo abordaron:', NCE[2][tren.key]
            print 'Tren: ', tren.clientes
            print 'Clientes que han llegado:',NCLL
            print '\n\n\n'
            time.sleep(0.03)
            if NCE[2][tren.key] < 0:
                r = raw_input()

    TEM = TET/limite
    for n in range(0,len(NCE)):
        NCE[n] = sum(NCE[n])/len(NCE[n])
    if verbose:
        print 'Tiempo de Espera Total:', '{0:.2f}'.format(TET)
        print 'Tiempo de Espera Promedio:', '{0:.2f}'.format(TEM)
        print 'Clientes que no alcanzaron a subir:', sum(NCE)
    tup = (TEM, TET, NCLL, sum(NCE), tren.key)
    return tup 

if __name__ == "__main__":

    #### Parametros para la Instancia #####
    freqTren = 0
    while freqTren < 210:
        freqTren = int(raw_input("Frecuencia que se envia un tren: "))
    if type(freqTren) is not int :
        freqTren = 280
    freqRegreso = freqTren+90
    v = True

    instancia = simular(freqTren, freqRegreso, v)
