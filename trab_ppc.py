from threading import Condition, Thread
from time import sleep, time
from random import choice, randint
import numpy as np

NUM_SKIERS = 120
NUM_SEATS = 4
#queue = []
LS = []
LT = []
RT = []
RS = []


#1) Escolhe a fila LS se o tamanho da fila LS for:
    #a) Menor que 2 * tamanho da fila LT, E
    #b) Menor que 2 * tamanho da fila RT, E
    #c) Menor que o tamanho da fila RS.
#2) Escolhe a fila RS se o tamanho da fila RS for:
    #a) Menor que 2 * tamanho da fila LT, E
    #b) Menor que 2 * tamanho da fila RT, E
    #c) Menor ou igual ao tamanho da fila LS.
#3) Escolhe a fila LT se o comprimento da fila LT for menor ou igual ao tamanho da fila RT, senão,
#4) Escolhe a fila RT

class Timer(Thread):
    def __init__(self, cv):
        Thread.__init__(self)
        self.condition = cv
        self.time = 0

class Skier(Thread):
    def __init__(self, cv, i):
        Thread.__init__(self)
        self.condition = cv
        self.i = i

    def __str__(self):
        return ('Pessoa {}'.format(self.id))

    def start(self):
        #Esquiador chega p/ entrar na fila
        print("Esquiador entra na fila")
        waiting_time = time()

        #Condições p/ escolha de fila

        #Escolhe a fila que vai entrar
        if (len(LS) < 2 * len(LT) and len(LS) < 2 * len(RT) and len(LS) < len(RS)):
            LS.append(self)
            print("Esquiador entrou na fila LS")
        elif (len(RS) < 2 * len(LT) and len(RS) < 2 * len(RT) and len(RS) < len(LS)):
            RS.append(self)
            print("Esquiador entrou na fila RS")
        elif (len(LT) <= len(RT)):
            LT.append(self)
            print("Esquiador entrou na fila LT")
        else:
            RT.append(self)
            print("Esquiador entrou na fila RT")



    # Atualiza o contador de pessoas


#1°) LT e RT tem prioridade if (LT e RT > 2 )
#    cadeira == ocupada quando
#           append LT or RT 1 vez and
#           append RT or RS 1 vez
#    -LT: while LT <= 2:
#               servir RT
#     
#    if LT and RT <=2:
#           servir LS e RS até
#           cadeira == ocupada
#
#    if LS and RS == 0:
#           if cadeira == 3 pessoas
#                   cadeira viaja


#     Se LT estiver "vazia" é colocado em wait() ???


#As filas LT e RT tem a prioridade sobre as filas LS e RS que são servidas alternadamente quando ambas não
#estão vazias. Quer dizer, se LT está vazio, vai servir RT seguidamente até ter pessoas suficiente na fila LT. Se as
#filas LT ou RT tiver uma ou duas pessoas, ela é considerada vazia, é necessário ter um mínimo de três pessoas
#para servir as filas LT e RT.
#Como a cadeira tem quatro lugares, a quarta posição será ocupada por um esquiador das filas LS ou RS
#alternadamente. Novamente, se uma fila estiver vazia, a outra fila é servida continuamente.
#Se as filas LT e RT estiverem vazias é permitido atender as filas LS e RS até preencher todos as quatro posições.
#Caso as filas LS e RS estejam vazias é permitido que a cadeira viaje com apenas três pessoas sentadas.

    def enter_elevator(self):
#        #Garantia que o recurso será liberado após o seu uso
#        with(self.condition):
#            while(True):
#            # Se não for o primeiro da fila, dorme
#                if(queue.index(self) > 0):
#                    s = 'Pessoa {} não entrou por não ser o primeiro ' \
#                        'da fila\n-----'.format(self.i)
#                    print(s)
#                    self.condition.wait()
#                    continue

        with(self.condition):
            while(True):
                #Condição p/ Elevador subir apenas com uma tripla
                lefttriple = False
                righttriple = False

                random = randint()

                if (random == 0):
                    if (len(LT) > 2 and NUM_SEATS > 2):
                        for i in range(2):
                            LT.remove()
                            NUM_SEATS = NUM_SEATS - 1
                            #Tempo na fila
                        print("Elevador subiu com uma LT")
                        lefttriple = True
                    else:
                        if (len(RT) > 2 and NUM_SEATS > 2):
                            for i in range(2):
                                RT.remove()
                                NUM_SEATS = NUM_SEATS - 1
                                #Tempo na fila
                        print("Elevador subiu com uma RT")
                        righttriple = True
                #Caso LT e RT estejam vazias
                if (lefttriple == False and righttriple == False):
                    #Variável de auxílio p/ variar entre as filas
                    random2 = randint()
                    #Alternar entre RS e LS
                    while (NUM_SEATS > 0 and (len(LS) > 0 or len(RS)) > 0):
                        # conferir
                        if (random2):
                            if (len(LS) > 0):
                                LS.remove()
                                NUM_SEATS = NUM_SEATS - 1
                                #Tempo na fila
                                print("Elevador subiu com uma LS")
                            random2 = False
                        else:
                            if (len(RS) > 0):
                                RS.remove()
                                NUM_SEATS = NUM_SEATS - 1
                                #Tempo na fila
                                print("Elevador subiu com uma RS")
                            random2 = True
                else:
                    if (lefttriple):
                        if (len(RS) > 0):
                            RS.remove()
                            NUM_SEATS = NUM_SEATS - 1
                            #Tempo na fila
                        print("Elevador subiu com uma LT e uma RS")
                    if(righttriple):
                        if (len(LS) > 0):
                            LS.remove()
                            NUM_SEATS = NUM_SEATS - 1
                            #Tempo na fila
                        print("Elevador subiu com uma RT e uma LS")



