from threading import Condition, Thread
from time import sleep, time
from random import choice, randint
import numpy as np

NUM_SKIERS = 120
#NUM_SEATS = 4

LS = []
LT = []
RT = []
RS = []

class Skier(Thread):
    def __init__(self, cv):
        Thread.__init__(self)
        self.condition = cv
        #self.i = i

#    def Skier(self):
#        self.skier = self

    def run(self):
        #Esquiador chega p/ entrar na fila
        print("Esquiador chega na fila")
        print(" ")
        waiting_time = time()

        #Condições p/ escolha de fila

        #Escolhe a fila que vai entrar
        if (len(LS) < 2 * len(LT) and len(LS) < 2 * len(RT) and len(LS) < len(RS)):
            LS.append(self)
            print("Esquiador {} entrou na fila LS" .format(self))
            print(" ")

        elif (len(RS) < 2 * len(LT) and len(RS) < 2 * len(RT) and len(RS) <= len(LS)):
            RS.append(self)
            print("Esquiador {} entrou na fila RS" .format(self))
            print(" ")

        elif (len(LT) <= len(RT)):
            LT.append(self)
            print("Esquiador {} entrou na fila LT".format(self))
            print(" ")

        else:
            RT.append(self)
            print("Esquiador {} entrou na fila RT" .format(self))
            print(" ")


        print("Fila LT: {}" .format(LT))
        print("Fila RT: {}" .format(RT))
        print("Fila LS: {}" .format(LS))
        print("Fila RS: {}" .format(RS))

class Elevator(Thread):
    #print('i')
    def __init__(self, cv):
        Thread.__init__(self)
        self.condition = cv
        #self.i = i

    def run(self):
        print("chegou aqui")
        NUM_SEATS = 4
        with(self.condition):
            while(True):
                #Condição p/ Elevador subir apenas com uma tripla
                lefttriple = False
                righttriple = False
                print('a')
                random = randint(0,1)
                #random = 0
                if (random == 0):
                    print("Checagem Condicional 1")
                    if (len(LT) > 2 and NUM_SEATS > 2):
                        for i in range(3, 0, -1):
                            #LT.remove(LT[i-1])
                            LT.pop()
                            NUM_SEATS = NUM_SEATS - 1
                            #Tempo na fila
                        
                        #LT = LT[:len(LT)-2]         #### Exception 


                        print("Saiu da fila LT")
                        #print("num seats1: ")
                        #print(NUM_SEATS)

                        lefttriple = True
                        self.condition.wait()
                        continue
                    else:
                        print("Checagem Condicional 2")
                        if (len(RT) > 2 and NUM_SEATS > 2):
                            for i in range(3, 0, -1):
                                #RT.remove(RT[i-1])
                                RT.pop()
                                NUM_SEATS = NUM_SEATS - 1
                                
                                #Tempo na fila
                            
                            print("Saiu da fila RT")
                            #print("num seats2: ")
                            #print(NUM_SEATS)
                            
                            righttriple = True
                            self.condition.wait()
                            continue
                #Caso LT e RT estejam vazias
                if (lefttriple == False and righttriple == False):
                    #Variável de auxílio p/ variar entre as filas
                    
                    #random2 = randint(0,1)
                    #aux = random2 == 0

                    flag = choice(["LS", "RS"])

                    #Alternar entre RS e LS
                    while (NUM_SEATS > 0 and (len(LS) > 0 or len(RS)) > 0):
                        # conferir
                        
                        if (flag == "LS"):
                            if (len(LS) > 0):
                                #LS.remove(LS[0])
                                LS.pop()
                                NUM_SEATS = NUM_SEATS - 1
                                #self.NUM_SEATS = self.NUM_SEATS - 1
                                #Tempo na fila

                                print("Saiu da fila LS")
                                #print("Num seats3: ")
                                #print(NUM_SEATS)

                            #aux = False
                            self.condition.wait()
                            continue
                        elif (flag == "RS"):
                            if (len(RS) > 0):
                                #RS.remove(RS[0])
                                RS.pop()
                                NUM_SEATS = NUM_SEATS - 1
                                #self.NUM_SEATS = self.NUM_SEATS - 1
                                #Tempo na fila


                                print("Saiu da fila RS")
                                #print("num seats4: ")
                                #print(NUM_SEATS)
                                
                            #aux = True
                            self.condition.wait()
                            continue
                else:
                    if (lefttriple == True and len(RS) > 0):
                        #RS.remove(self)
                        RS.pop()
                        NUM_SEATS = NUM_SEATS - 1
                        #self.NUM_SEATS = self.NUM_SEATS - 1
                        #Tempo na fila
                        print("Saiu uma LT e uma RS")
                        
                        self.condition.wait()
                        continue

                    if(righttriple == True and len(LS) > 0):
                        #LS.remove(self)
                        LS.pop()
                        NUM_SEATS = NUM_SEATS - 1
                        #self.NUM_SEATS = self.NUM_SEATS - 1
                        #Tempo na fila
                        print("Saiu uma RT e uma LS")
                        
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
            sleep(4)
                #break


class SkiProblem():

    def main(): 
        cv = Condition()

            #e = Elevator(cv)
            #e.start()

        while (True):
            e = Elevator(cv)
            e.start()

            #Cria um novo esquiador
            t = Skier(cv)
            t.start()

            sleep(1)

            with(cv):
                cv.notify_all()

#if(__name__ == '__main__'):
#    main()
s = SkiProblem
s.main()