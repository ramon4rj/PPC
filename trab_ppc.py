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
    def _init_(self, cv):
        Thread._init_(self)
        self.condition = cv
        self.time = 0

class Skier(Thread):
    def _init_(self, cv, i):
        Thread._init_(self)
        self.condition = cv
        self.i = i

    def _str_(self):
        return ('Esquiador {}'.format(self.id))

    def run(self):
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


class Elevator(Thread):
    def _init_(self, cv):
        Thread._init_(self)
        self.condition = cv

    def enter_elevator(self):
        with(self.condition):
            while(True):
                #Condição p/ Elevador subir apenas com uma tripla
                lefttriple = False
                righttriple = False

                random = randint()

                if (random == 0):
                    if (len(LT) > 2 and NUM_SEATS > 2):
                        for i in range(3):
                            LT.remove(self)
                            NUM_SEATS = NUM_SEATS - 1
                            #Tempo na fila
                        print("Entrou uma LT")
                        lefttriple = True
                        self.condition.wait()
                        continue
                    else:
                        if (len(RT) > 2 and NUM_SEATS > 2):
                            for i in range(3):
                                RT.remove(self)
                                NUM_SEATS = NUM_SEATS - 1
                                #Tempo na fila
                        print("Entrou  uma RT")
                        righttriple = True
                        self.condition.wait()
                        continue
                #Caso LT e RT estejam vazias
                if (lefttriple == False and righttriple == False):
                    #Variável de auxílio p/ variar entre as filas
                    random2 = randint()
                    #Alternar entre RS e LS
                    while (NUM_SEATS > 0 and (len(LS) > 0 or len(RS)) > 0):
                        # conferir
                        if (random2):
                            if (len(LS) > 0):
                                LS.remove(self)
                                NUM_SEATS = NUM_SEATS - 1
                                #Tempo na fila
                                print("Entrou uma LS")
                            random2 = False
                            self.condition.wait()
                            continue
                        else:
                            if (len(RS) > 0):
                                RS.remove(self)
                                NUM_SEATS = NUM_SEATS - 1
                                #Tempo na fila
                                print("Entrou uma RS")
                            random2 = True
                            self.condition.wait()
                            continue
                else:
                    if (lefttriple and len(RS) > 0):
                        RS.remove(self)
                        NUM_SEATS = NUM_SEATS - 1
                        #Tempo na fila
                        print("Entrou uma LT e uma RS")
                        self.condition.wait()
                        continue

                    if(righttriple and len(LS) > 0):
                        LS.remove(self)
                        NUM_SEATS = NUM_SEATS - 1
                        #Tempo na fila
                        print("Entrou uma RT e uma LS")
                        self.condition.wait()
                        continue
                #Zera a contagem dos bancos, ou seja, chega outro elevador
                NUM_SEATS = 4
                self.condition.notify_all()

                #Espera 4 segundos e reinicia o processo
                sleep(4)




def main():
    cv = Condition()

    #Inicia a Thread p/ os 120 esquiadores
    for i in range(NUM_SKIERS):
        t = Skier(cv, i + 1)
        t.start()

        #Tempo de espera p/ chegar um novo esquiador
        sleep(1)