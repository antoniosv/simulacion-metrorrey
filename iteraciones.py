import simulacionmetro
from simulacionmetro import simular

if __name__ == "__main__":

    #### Parametros para la Instancia #####
    freqTren = 0
    while freqTren < 210:
        freqTren = int(raw_input("Frecuencia que se envia un tren: "))
    if type(freqTren) is not int :
        freqTren = 280
    freqRegreso = freqTren+90
    iteraciones = 10
    v = False
    filename = str(freqTren) + '_' + str(freqRegreso)
    f = open(filename, 'w')

    TEM = [[] for _ in xrange(iteraciones)]
    TET = [[] for _ in xrange(iteraciones)]
    NCLL = [[] for _ in xrange(iteraciones)]
    NCE =  [[] for _ in xrange(iteraciones)]
    units =  [[] for _ in xrange(iteraciones)]
    header = 'Envio Trenes:'+ str(freqTren) + '\tRegreso Trenes:' + str(freqRegreso) + '\nTEM\tTET\t\tNCLL\tNCE\tTrenes\n'
    f.write(header)
    for i in range(0,iteraciones):
        instancia = simular(freqTren, freqRegreso, v)
        TEM[i] = instancia[0]
        TET[i] = instancia[1]
        NCLL[i] = instancia[2]
        NCE[i] = instancia[3]
        units[i] = instancia[4]
        
        formato = '{0:.2f}'.format(TEM[i]) + '\t{0:.2f}'.format(TET[i]) + \
            '\t{0}'.format(NCLL[i]) + '\t{0}'.format(NCE[i])+'\t{0}'.format(units[i])+'\n'
        f.write(formato)
    f.close()
