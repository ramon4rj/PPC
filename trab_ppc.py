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
        if (LS < 2 * LT and LS < 2 * RT and LS < RS):
            LS.append(self)
        elif (RS < 2 * LT and RS < 2 * RT and RS < LS):
            RS.append(self)
        elif (LT <= RT):
            LT.append(self)
        else:
            RT.append(self)



    # Atualiza o contador de pessoas


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

    def enter_elevator(self):
        #Garantia que o recurso será liberado após o seu uso
        with(self.condition):
            while(True):
            # Se não for o primeiro da fila, dorme
                if(queue.index(self) > 0):
                    s = 'Pessoa {} não entrou por não ser o primeiro ' \
                        'da fila\n-----'.format(self.i)
                    print(s)
                    self.condition.wait()
                    continue