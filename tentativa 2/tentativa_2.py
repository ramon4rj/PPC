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

def print_filas():
    print("Fila LT: {}" .format(LT))
    print("Fila RT: {}" .format(RT))
    print("Fila LS: {}" .format(LS))
    print("Fila RS: {}" .format(RS))

class Skier(Thread):
    def __init__(self, cv, i):
        Thread.__init__(self)
        self.condition = cv
        self.i = i

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
            LS.append(self.i)
            #print("Esquiador {} entrou na fila LS" .format(self))
            print("Esquiador {} entrou na fila LS" .format(self.i))
            print(" ")

        elif (len(RS) < 2 * len(LT) and len(RS) < 2 * len(RT) and len(RS) <= len(LS)):
            RS.append(self.i)
            print("Esquiador {} entrou na fila RS" .format(self.i))
            print(" ")

        elif (len(LT) <= len(RT)):
            LT.append(self.i)
            print("Esquiador {} entrou na fila LT".format(self.i))
            print(" ")

        else:
            RT.append(self.i)
            print("Esquiador {} entrou na fila RT" .format(self.i))
            print(" ")


#    def print_filas():
#        print("Fila LT: {}" .format(LT))
#        print("Fila RT: {}" .format(RT))
#        print("Fila LS: {}" .format(LS))
#        print("Fila RS: {}" .format(RS))

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
                #print('a')
                #random = randint(0,1)
                flag0 = choice(["LT", "RT"])
                print("Flag0: {}" .format(flag0))

                #random = 0
                #print("random: {}" .format(random))
                if (flag0 == "LT"):
                    print("Checagem Condicional 1")
                    if (len(LT) > 2 and NUM_SEATS > 2):
                        for i in range(0, 3):
                            #LT.remove(LT[i-1])
                            LT.pop(0)
                            print("i: {}" .format(i))
                            NUM_SEATS = NUM_SEATS - 1
                            print_filas()
                            #Tempo na fila
                                    
                                #LT = LT[:len(LT)-2]         #### Exception 


                        print("Saiu da fila LT")
                                #print("num seats1: ")
                                #print(NUM_SEATS)

                        lefttriple = True
                        self.condition.wait()
                        continue
                    #elif(lefttriple == False):  #LT vazio -> serve RT até ter pessoas suficientes em LT
                    elif(lefttriple == False):
                        print("Checagem Condicional 2")
                        if (len(RT) > 2 and NUM_SEATS > 2):
                            print("akontece")
                            for i in range(0, 3):
                                RT.pop(0)
                                print("i: {}" .format(i))
                                NUM_SEATS = NUM_SEATS - 1
                                print_filas()
                                        
                                #Tempo na fila
                                    
                            print("Saiu da fila RT")
                                    
                            righttriple = True
                            self.condition.wait()
                            continue
                #Caso LT e RT estejam vazias
                if (lefttriple == False and righttriple == False):
                    #Variáveis de auxílio p/ variar entre as filas
                    
                    leftsingle = False
                    rightsingle = False

                    flag = choice(["LS", "RS"])
                    print("Flag: {}" .format(flag))
                    

                    #Alternar entre RS e LS
                    #while (NUM_SEATS > 0 and (len(LS) > 0 or len(RS)) > 0): #Enquanto houver assentos disponíveis e LS e RS > 0
                    while (NUM_SEATS > 0):  #Enquanto houver assentos disponíveis e LS e RS > 0
                        
                        if (flag == "LS"):
                            if (len(LS) > 0):   #Incluir rightsingle aqui ?????
                                LS.pop(0)
                                NUM_SEATS = NUM_SEATS - 1
                                print_filas()
                                #Tempo na fila

                                print("Saiu da fila LS")

                            leftsingle = True
                            self.condition.wait()
                            continue
                        elif (flag == "RS" or leftsingle == True):
                            if (len(RS) > 0):
                                RS.pop(0)
                                NUM_SEATS = NUM_SEATS - 1
                                print_filas()
                                #Tempo na fila


                                print("Saiu da fila RS")
                                
                            rightsingle = True
                            self.condition.wait()
                            continue
                else:
                    #if (lefttriple == True and len(RS) > 0):
                    if (lefttriple == True and rightsingle == True):      #nao da
                        RS.pop(0)
                        NUM_SEATS = NUM_SEATS - 1
                        print_filas()
                        #Tempo na fila
                        print("Saiu uma LT e uma RS")
                        
                        self.condition.wait()
                        continue

                    #if(righttriple == True and len(LS) > 0):
                    if (righttriple == True and leftsingle == True):
                        LS.pop(0)
                        NUM_SEATS = NUM_SEATS - 1
                        print_filas()
                        #Tempo na fila
                        print("Saiu uma RT e uma LS")
                        
                        self.condition.wait()
                        continue
                
                #Zera a contagem dos bancos, ou seja, chega outro elevador
                print("chegou no notify all")

                break

            NUM_SEATS = 4
            with(self.condition):
                self.condition.notify_all()
                print("######## SLEEP ########")
            sleep(4)

            #Espera 4 segundos e reinicia o processo


class SkiProblem():

    def main(): 
        cv = Condition()
        i = 0

        #e = Elevator(cv)
        #e.start()

        while (True):
            with(cv):
                i = i + 1
                t = Skier(cv, i)
                t.start()
                sleep(1)

                e = Elevator(cv)
                e.start()
                sleep(1)

                #cv.notify_all()
#        for i in range(120):
#            e = Elevator(cv)
#            e.start()

#            #Cria um novo esquiador
#            t = Skier(cv, i)
#            t.start()

#            sleep(1)
#
#            with(cv):
#                cv.notify_all()


#if(__name__ == '__main__'):
#    main()
s = SkiProblem
s.main()