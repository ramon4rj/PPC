from threading import Condition, Thread
from time import sleep, time
from random import choice, randint
import numpy as np

NUM_SKIERS = 120
NUM_SEATS = 4

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
        #self.NUM_SEATS = 4


    def str(self):
        return ('Esquiador {}'.format(self.id))

    def run(self):
        #Esquiador chega p/ entrar na fila
        print("Esquiador chega na fila")
        waiting_time = time()

        #Condições p/ escolha de fila

        #Escolhe a fila que vai entrar
        if (len(LS) < 2 * len(LT) and len(LS) < 2 * len(RT) and len(LS) < len(RS)):
            LS.append(self)
            print("Esquiador {} entrou na fila LS" .format(self.i))
        elif (len(RS) < 2 * len(LT) and len(RS) < 2 * len(RT) and len(RS) <= len(LS)):
            RS.append(self)
            print("Esquiador {} entrou na fila RS" .format(self.i))
        elif (len(LT) <= len(RT)):
            LT.append(self)
            print("Esquiador {} entrou na fila LT".format(self.i))
        else:
            RT.append(self)
            print("Esquiador {} entrou na fila RT" .format(self.i))
        
        #self.enter_elevator()
            #sleep(5)
        
        self.enter_elevator()
        sleep(5)
        self.elevator_leave()




    def enter_elevator(self):
        NUM_SEATS = 4
        with(self.condition):
            while(True):
                #Condição p/ Elevador subir apenas com uma tripla
                lefttriple = False
                righttriple = False

                random = randint(0,2)
                #random = 0
                if (random == 0):
                    if (len(LT) > 2 and NUM_SEATS > 2):
                        for i in range(3, 0, -1):
                            LT.remove(LT[i-1])
                            NUM_SEATS = NUM_SEATS - 1
                            #self.NUM_SEATS = self.NUM_SEATS - 1
                            #Tempo na fila
                            elevator.append(self)
                            #print("deu append LT")
                        #LT = LT[:len(self.seats)-2]
                        #NUM_SEATS = NUM_SEATS - 1
                        elevator.append(self)
                        print("Saiu da fila LT")
                        print("num seats1: ")
                        print(NUM_SEATS)
                        #print(ls)
                        elevator.print_elevator()
                        lefttriple = True
                        self.condition.wait()
                        continue
                    else:
                        if (len(RT) > 2 and NUM_SEATS > 2):
                            for i in range(3, 0, -1):
                                RT.remove(RT[i-1])
                                NUM_SEATS = NUM_SEATS - 1
                                #self.NUM_SEATS = self.NUM_SEATS - 1
                                #Tempo na fila
                                elevator.append(self)
                                print("deu append RT")
                                #elevator.remove(self)
                            print("Saiu da fila RT")
                            print("num seats2: ")
                            print(NUM_SEATS)
                            righttriple = True
                            self.condition.wait()
                            continue
                #Caso LT e RT estejam vazias
                if (lefttriple == False and righttriple == False):
                    #Variável de auxílio p/ variar entre as filas
                    random2 = randint(0,2)
                    aux = random2 == 0
                    #Alternar entre RS e LS
                    while (NUM_SEATS > 0 and (len(LS) > 0 or len(RS)) > 0):
                        # conferir
                        
                        if (aux == True):
                            if (len(LS) > 0):
                                LS.remove(LS[0])
                                NUM_SEATS = NUM_SEATS - 1
                                #self.NUM_SEATS = self.NUM_SEATS - 1
                                #Tempo na fila
                                
                                elevator.append(self)
                                print("deu append LS")
                                #elevator.remove(self)
                                print("Saiu da fila LS")
                                print("Num seats3: ")
                                print(NUM_SEATS)
                            aux = False
                            self.condition.wait()
                            continue
                        else:
                            if (len(RS) > 0):
                                RS.remove(RS[0])
                                NUM_SEATS = NUM_SEATS - 1
                                #self.NUM_SEATS = self.NUM_SEATS - 1
                                #Tempo na fila
                                elevator.append(self)
                                print("deu append RS")
                                #elevator.remove(self)
                                print("Saiu da fila RS")
                                print("num seats4: ")
                                print(NUM_SEATS)
                                elevator.print_elevator()
                            aux = True
                            self.condition.wait()
                            continue
                else:
                    if (lefttriple == True and len(RS) > 0):
                        RS.remove(self)
                        #NUM_SEATS = NUM_SEATS - 1
                        self.NUM_SEATS = self.NUM_SEATS - 1
                        #Tempo na fila
                        print("Saiu uma LT e uma RS")
                        elevator.append(self)
                        self.condition.wait()
                        continue

                    if(righttriple == True and len(LS) > 0):
                        LS.remove(self)
                        #NUM_SEATS = NUM_SEATS - 1
                        self.NUM_SEATS = self.NUM_SEATS - 1
                        #Tempo na fila
                        print("Saiu uma RT e uma LS")
                        elevator.append(self)
                        self.condition.wait()
                        continue
                
                #Zera a contagem dos bancos, ou seja, chega outro elevador
                print("chegou no notify all")
                #elevator.append(self)

                break

            NUM_SEATS = 4
            with(self.condition):
                self.condition.notify_all()

                #Espera 4 segundos e reinicia o processo
                #sleep(4)
                #break


    def elevator_leave(self):
        if len(elevator.seats) > 3:
            print("chegou elvator leave")
            #print(ls)
            with(self.condition):
                elevator.seats = elevator.seats[:len(elevator.seats)-2]
                self.condition.notify_all()
            #while len(self.seats) != 0:
            #for i in range(3, 0, -1):
                #with(self.condition):
                    #elevator.remover(self)
                    #elevator.pop(i)
                    #elevator.self.seats.remover() 
                    #self.condition.notify_all()



class Elevator:
    def __init__(self, NUM_SEATS):
        self.seats = []
        self.NUM_SEATS = NUM_SEATS
    
    def append(self, s):
        self.seats.append(s)

    def remover(self, s):
        self.seats.remove(s)

    def print_elevator(self):
        print("Assentos disponíveis: ")
        print(self.seats)

    
elevator = Elevator(NUM_SEATS = NUM_SEATS)
#elevator.print_elevator()


def main():
    cv = Condition()

    #Inicia a Thread do elevador
    #e = Elevator(None, cv)
    #e.start()

    #Inicia a Thread p/ os 120 esquiadores
    for i in range(120):
        t = Skier(cv, i + 1)
        t.start()

        #Tempo de espera p/ chegar um novo esquiador
        sleep(1)

    with(cv):
        cv.notify_all()

if(__name__ == '__main__'):
    main()