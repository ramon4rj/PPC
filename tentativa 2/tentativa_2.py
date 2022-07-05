from threading import Condition, Thread
from time import sleep, time
from random import choice, randint
import numpy as np

NUM_SKIERS = 120
#NUM_SEATS = 4
#Lista p/ guardar os esquiadores que entraram no elevador
cont_skier = []

#Lista p/ guadar os incrementos de subida do elevador
cont_elevator = []

#Filas
LS = []
LT = []
RT = []
RS = []

#Lista p/ juntar o tempo de espera em fila dos esquiadores
skier_waiting_time = []

def print_filas():
    #Imprime os esquiadores que estão nas filas
    print("Fila LT: {}" .format(LT))
    print("Fila RT: {}" .format(RT))
    print("Fila LS: {}" .format(LS))
    print("Fila RS: {}" .format(RS))

def print_filas_len():
    #Imprime a quantidade de esquiadores nas filas
    print("Fila LT: {} pessoas" .format(len(LT)))
    print("Fila RT: {} pessoas" .format(len(RT)))
    print("Fila LS: {} pessoas" .format(len(LS)))
    print("Fila RS: {} pessoas" .format(len(RS)))
    print(" ")

class Skier(Thread):
    def __init__(self, cv, i):
        Thread.__init__(self)
        self.condition = cv
        self.i = i

    def run(self):
        #Esquiador chega p/ entrar na fila
        print("Esquiador chega na fila")
        print(" ")
        start_waiting_time = time()

        #Condições p/ escolha de fila

        #Escolhe a fila que vai entrar
        if (len(LS) < 2 * len(LT) and len(LS) < 2 * len(RT) and len(LS) < len(RS)):
            LS.append(self.i)
            #print("Esquiador {} entrou na fila LS" .format(self))
            print("Esquiador {} entrou na fila LS" .format(self.i))
            skier_waiting_time.append(time() - start_waiting_time)
            print(" ")
            print_filas_len()

        elif (len(RS) < 2 * len(LT) and len(RS) < 2 * len(RT) and len(RS) <= len(LS)):
            RS.append(self.i)
            print("Esquiador {} entrou na fila RS" .format(self.i))
            skier_waiting_time.append(time() - start_waiting_time)
            print(" ")
            print_filas_len()

        elif (len(LT) <= len(RT)):
            LT.append(self.i)
            print("Esquiador {} entrou na fila LT".format(self.i))
            skier_waiting_time.append(time() - start_waiting_time)
            print(" ")
            print_filas_len()

        else:
            RT.append(self.i)
            print("Esquiador {} entrou na fila RT" .format(self.i))
            skier_waiting_time.append(time() - start_waiting_time)
            print(" ")
            print_filas_len()


class Elevator(Thread):
    def __init__(self, cv):
        Thread.__init__(self)
        self.condition = cv
        #self.i = i

    def run(self):
        #Variável p/ contar os esquiadores que entraram no elevador
        cont_skier.append(1)
        NUM_SEATS = 4
        with(self.condition):
            while(True):
                #Condição p/ Elevador subir apenas com uma tripla
                lefttriple = False
                righttriple = False

                flag0 = choice(["LT", "RT"])

                if (flag0 == "LT"):
                    if (len(LT) > 2 and NUM_SEATS > 2):
                        for i in range(0, 3):
                            LT.pop(0)
                            NUM_SEATS = NUM_SEATS - 1

                        print(" ")
                        print("Saiu da fila LT")
                        print_filas_len()

                        lefttriple = True
                        self.condition.wait()
                        continue

                    #LT vazio -> serve RT até ter pessoas suficientes em LT
                    elif(lefttriple == False):
                        if (len(RT) > 2 and NUM_SEATS > 2):
                            for i in range(0, 3):
                                RT.pop(0)
                                NUM_SEATS = NUM_SEATS - 1

                            print(" ")
                            print("Saiu da fila RT")
                            print_filas_len()
                                    
                            righttriple = True
                            self.condition.wait()
                            continue

                #Caso LT e RT estejam vazias
                elif (lefttriple == False and righttriple == False):

                    #Variáveis de auxílio p/ variar entre as filas
                    leftsingle = False
                    rightsingle = False

                    flag = choice(["LS", "RS"])
                    

                    #Alternar entre RS e LS
                    while (NUM_SEATS > 0):  #Enquanto houver assentos disponíveis e LS e RS > 0
                        
                        if (flag == "LS"):
                            if (len(LS) > 0):
                                LS.pop(0)
                                NUM_SEATS = NUM_SEATS - 1
                                #Tempo na fila
                                print(" ")
                                print("Saiu da fila LS")
                                print_filas_len()

                            leftsingle = True
                            self.condition.wait()
                            continue
                        elif (flag == "RS" or leftsingle == True):
                            if (len(RS) > 0):
                                RS.pop(0)
                                NUM_SEATS = NUM_SEATS - 1
                                #Tempo na fila
                                print(" ")
                                print("Saiu da fila RS")
                                print_filas_len()

                            rightsingle = True
                            self.condition.wait()
                            continue

                #Contador para quantas vezes o elevador subiu
                cont_elevator.append(1)

                #Fim da checagem de condições
                #Acorda as threads em wait
                with(self.condition):
                    self.condition.notify_all()
                                        
                break

class SkiProblem():

    def main(): 
        cv = Condition()
        i = 0

        #while (True):
        for i in range(NUM_SKIERS):
            with(cv):
                i = i + 1
                t = Skier(cv, i)
                t.start()
                sleep(1)

                e = Elevator(cv)
                e.start()
                #sleep(1)
        
        #Variáveis usadas para o cálculo do tempo médio em fila
        time_sum = sum(skier_waiting_time)
        time_spent = time_sum / len(skier_waiting_time)
        print("Tempo médio que o esquiador espera em fila: {} " .format(time_spent))
        print(" ")

        #Cálculo da taxa de aproveitamento
        taxa_aproveitamento = len(cont_skier) / (len(cont_elevator) * 4)
        print(" ")
        print("Taxa de aproveitamento: {}" .format(taxa_aproveitamento))
        print(" ")
    


s = SkiProblem
s.main()