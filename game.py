import pygame, sys
from pygame.locals import *
import numpy as np 
import copy
from random import randint

from inimigo import Inimigo
from player import Player
from neural import Neural
# from neural import Neural
import time



#constante do AG
NUM_CRUZAMENTO_POR_EPOCA = 1
NUM_INVIDUOS_TORNEIO = 70
NUM_POP = 100
TAXA_MUTACAO = 10
numeroNeuronio = 1


MAX_RODADA = 200

WIDTH = 50
HEIGHT = 50
SIZE_OBJECT = 10
SCREENW = WIDTH*SIZE_OBJECT
SCREENH =  HEIGHT*SIZE_OBJECT
clock = pygame.time.Clock()
enemy = []

#constantes do mapa
LIVRE = 2
PAREDE = 0
INICIO = 1
INIMIGO = 3
INIMIGOV = 4
INIMIGOVV = 5
INIMIGOH = 6
INIMIGOHH = 7
INIMIGOD = 8
INIMIGODD = 9
INIMIGOD1 = 10
INIMIGOD11 = 11
INIMIGOD2 = 12
INIMIGOD22 = 13
PLAYER = 999
#PLAYER
MOV_UP = -1
MOV_DOWN = -2
MOV_LEFT = -3
MOV_RIGHt = -4

#color
WHITE=(255,255,255)
BLUE=(0,0,255)
RED =(255,0,0)
GREEN =(255,0,0)
YELLOW =(255,255,0)
#sensor



def showMap(DISPLAY,matrixMap,players,verbose=0):    
    
    
    count = 0
    for linha , x in zip(matrixMap,range(WIDTH)):
        for elemento, y in zip(linha,range(HEIGHT)):
            if(elemento == INICIO):
                pygame.draw.rect(DISPLAY,GREEN,(x*SIZE_OBJECT,y*SIZE_OBJECT,SIZE_OBJECT,SIZE_OBJECT))
            if(elemento == PAREDE):
                pygame.draw.rect(DISPLAY,BLUE,(x*SIZE_OBJECT,y*SIZE_OBJECT,SIZE_OBJECT,SIZE_OBJECT))
            if(elemento == LIVRE):
                pygame.draw.rect(DISPLAY,WHITE,(x*SIZE_OBJECT,y*SIZE_OBJECT,SIZE_OBJECT,SIZE_OBJECT))
            if(elemento > INIMIGO):
                pygame.draw.rect(DISPLAY,RED,(x*SIZE_OBJECT,y*SIZE_OBJECT,SIZE_OBJECT,SIZE_OBJECT))
    
            # pygame.display.update()
            # if(elemento == 1):
            #     pygame.draw.rect(DISPLAY,RED,(x*SIZE_OBJECT,y*SIZE_OBJECT,SIZE_OBJECT,SIZE_OBJECT))
                
            count = count +1
    
    for p1 in players:
        if(matrixMap[p1.x][p1.y] > INIMIGO):
            p1.vida = 0
            funcaoFitness(p1)
            
            print("morreu")
            
        else:
            if(p1.vida == 0):
                pygame.draw.rect(DISPLAY,(128,128,128),(p1.x*SIZE_OBJECT,p1.y*SIZE_OBJECT,SIZE_OBJECT,SIZE_OBJECT))
            else:
                pygame.draw.rect(DISPLAY,(0,255,0),(p1.x*SIZE_OBJECT,p1.y*SIZE_OBJECT,SIZE_OBJECT,SIZE_OBJECT))
        if(verbose == 1):
            pygame.display.update() 
    return 1
def funcaoFitness(p1):
    #Posicai do fim do jogo
    XFINAL = 45
    YFINAL = 13

    if(p1.x < 5):
        XFINAL = 5
        YFINAL = 33
        p1.fitness = 1000 *(pow(pow(p1.x - XFINAL,2) + pow(p1.y - YFINAL,2),0.5))
    else:
        p1.fitness =pow(pow(p1.x - XFINAL,2) + pow(p1.y - YFINAL,2),0.5)


    
def readSensor(DISPLAY,matrixMap,players,sensores):
    count = 0
    
    for p1, sensor  in zip(players,sensores):
        while(matrixMap[p1.x+count][p1.y] != PAREDE and matrixMap[p1.x+count][p1.y] < INIMIGO and p1.x+count < 50):
            count +=1
        pygame.draw.line(DISPLAY, (0,150,0), (p1.x*SIZE_OBJECT, p1.y*SIZE_OBJECT), ((p1.x+ count)*SIZE_OBJECT, p1.y*SIZE_OBJECT))
        sensor['R'] = matrixMap[p1.x+count][p1.y]
        sensor['RCount'] = count
        

        count = 0
        while(matrixMap[p1.x-count][p1.y] != PAREDE and matrixMap[p1.x-count][p1.y] < INIMIGO):
            count +=1
        pygame.draw.line(DISPLAY, (0,150,0), ((p1.x-count)*SIZE_OBJECT, p1.y*SIZE_OBJECT), ((p1.x)*SIZE_OBJECT, p1.y*SIZE_OBJECT))
        sensor['L'] = matrixMap[p1.x-count][p1.y]
        sensor['LCount'] = count
        
        
        count = 0
        while(matrixMap[p1.x][p1.y + count] != PAREDE and matrixMap[p1.x][p1.y + count] < INIMIGO ):
            count +=1
        pygame.draw.line(DISPLAY, (0,150,0), ((p1.x)*SIZE_OBJECT, (p1.y+count)*SIZE_OBJECT), ((p1.x)*SIZE_OBJECT, p1.y*SIZE_OBJECT))
        sensor['U'] = matrixMap[p1.x][p1.y+count]
        sensor['UCount'] = count

        count = 0
        while(matrixMap[p1.x][p1.y - count] != PAREDE and matrixMap[p1.x][p1.y - count] < INIMIGO ):
            count +=1
        pygame.draw.line(DISPLAY, (0,150,0), ((p1.x)*SIZE_OBJECT, (p1.y-count)*SIZE_OBJECT), ((p1.x)*SIZE_OBJECT, p1.y*SIZE_OBJECT))
        sensor['D'] = matrixMap[p1.x][p1.y - count]
        sensor['DCount'] = count

        count = 0
        while(matrixMap[p1.x - count][p1.y + count] != PAREDE and matrixMap[p1.x-count][p1.y + count] < INIMIGO ):
            count +=1
        pygame.draw.line(DISPLAY, (0,150,0), ((p1.x-count)*SIZE_OBJECT, (p1.y+count)*SIZE_OBJECT), ((p1.x)*SIZE_OBJECT, p1.y*SIZE_OBJECT))
        sensor['DL'] = matrixMap[p1.x-count][p1.y + count]
        sensor['DLCount'] = count

        count = 0
        while(matrixMap[p1.x + count][p1.y + count] != PAREDE and matrixMap[p1.x+count][p1.y + count] < INIMIGO ):
            count +=1
        pygame.draw.line(DISPLAY, (0,150,0), ((p1.x+count)*SIZE_OBJECT, (p1.y+count)*SIZE_OBJECT), ((p1.x)*SIZE_OBJECT, p1.y*SIZE_OBJECT))
        sensor['DR'] = matrixMap[p1.x+count][p1.y + count]
        sensor['DRCount'] = count
        
        count = 0
        while(matrixMap[p1.x + count][p1.y - count] != PAREDE and matrixMap[p1.x+count][p1.y - count] < INIMIGO ):
            count +=1
        pygame.draw.line(DISPLAY, (0,150,0), ((p1.x + count)*SIZE_OBJECT, (p1.y-count)*SIZE_OBJECT), ((p1.x)*SIZE_OBJECT, p1.y*SIZE_OBJECT))
        sensor['UR'] = matrixMap[p1.x+count][p1.y - count]
        sensor['URCount'] = count

        count = 0
        while(matrixMap[p1.x - count][p1.y - count] != PAREDE and matrixMap[p1.x-count][p1.y - count] < INIMIGO ):
            count +=1
        pygame.draw.line(DISPLAY, (0,150,0), ((p1.x - count)*SIZE_OBJECT, (p1.y-count)*SIZE_OBJECT), ((p1.x)*SIZE_OBJECT, p1.y*SIZE_OBJECT))
        sensor['UL'] = matrixMap[p1.x-count][p1.y - count]
        sensor['ULCount'] = count
    # pygame.display.update() 

    # print(sensor)
    


def criaInimigos():
    enemy.append(Inimigo('v',16,25,20))
    enemy.append(Inimigo('v',18,25,20))
    enemy.append(Inimigo('v',20,25,20))
    enemy.append(Inimigo('v',22,25,20))
    enemy.append(Inimigo('v',24,25,20))
    enemy.append(Inimigo('v',26,25,20))
    enemy.append(Inimigo('v',28,25,20))
    enemy.append(Inimigo('v',30,25,20))
    enemy.append(Inimigo('v',30,25,20))


    # enemy.append(Inimigo('h',25,16,10))
    # enemy.append(Inimigo('h',25,18,10))
    # enemy.append(Inimigo('h',25,20,10))
    # enemy.append(Inimigo('h',25,22,10))
    # enemy.append(Inimigo('h',25,24,10))
    # enemy.append(Inimigo('h',25,26,10))
    # enemy.append(Inimigo('h',25,28,10))
    # enemy.append(Inimigo('h',25,30,10))
    # enemy.append(Inimigo('h',25,30,10))

    # enemy.append(Inimigo('d1',25,16,10))
    # enemy.append(Inimigo('d1',25,18,10))
    # enemy.append(Inimigo('d1',25,20,10))
    # enemy.append(Inimigo('d1',25,22,10))
    # enemy.append(Inimigo('d1',25,24,10))
    # enemy.append(Inimigo('d1',25,26,10))
    # enemy.append(Inimigo('d1',25,28,10))
    # enemy.append(Inimigo('d1',25,30,10))
    # enemy.append(Inimigo('d1',25,30,10))


    
    
    # enemy.append(Inimigo('d2',25,18,10))
    # enemy.append(Inimigo('d2',25,20,10))
    # enemy.append(Inimigo('d2',25,22,10))
    # enemy.append(Inimigo('d2',25,24,10))
    # enemy.append(Inimigo('d2',25,26,10))
    # enemy.append(Inimigo('d2',25,28,10))
    # enemy.append(Inimigo('d2',25,30,10))
    # enemy.append(Inimigo('d2',25,30,10))
    
    
    # enemy.append(Inimigo('v',22,30,50))
    # enemy.append(Inimigo('h',10,30,10))
def criaMapa(WIDTH,HEIGHT):
    mapa = np.loadtxt(open("mapa.csv", "rb"), delimiter=",", skiprows=1)
    mapa = np.transpose(mapa)
    return mapa
def movimentaPlayer(p1,mapa,movimento):
    if movimento == 276 or movimento == 0:
        if(not(p1.step(mapa,MOV_LEFT))):
            # print("GAME OVER L")
            p1.vida = 0
            funcaoFitness(p1)
    if movimento == 275 or movimento == 1:
        if(not(p1.step(mapa,MOV_RIGHt))):
            # print("GAME OVER R")
            p1.vida = 0      
            funcaoFitness(p1)      
    if movimento == 273 or movimento == 2:
        if(not(p1.step(mapa,MOV_UP))):
            # print("GAME OVER")
            p1.vida = 0
            funcaoFitness(p1)
    if movimento == 274 or movimento == 3:
        if(not(p1.step(mapa,MOV_DOWN))):
            # print("GAME OVER")
            p1.vida = 0
            funcaoFitness(p1)

################################################################################################################################################################################

# Algoritmo Genetico
def combinacao_torneio(p1_redes,fitness):
    for _ in range(NUM_CRUZAMENTO_POR_EPOCA):
        
        newIndividuo1 = Neural(p1_redes[0].nInput,np.array([0,0,0]))
        newIndividuo2 = Neural(p1_redes[0].nInput,np.array([0,0,0]))
        
    
        isEqual = False
        while(np.array_equal(newIndividuo1.camada1, newIndividuo2.camada1) ) :
            isEqual = True
            individuosSelecionados = np.random.choice(NUM_POP, NUM_INVIDUOS_TORNEIO, replace=False)    
            
            a = np.argsort(fitness[individuosSelecionados])
            copy.deepcopy(p1_redes[individuosSelecionados][a[0]])
            a = a[:2] #pega os dois mais aptos
            newIndividuo1 = copy.deepcopy(p1_redes[individuosSelecionados][a[0]])
            newIndividuo2 = copy.deepcopy(p1_redes[individuosSelecionados][a[1]])
        
        if(randint(0,1)):
            newIndividuo2.camada1, newIndividuo1.camada1 = newIndividuo1.camada1 , newIndividuo2.camada1
        elif(randint(0,1)):
            newIndividuo2.camada2, newIndividuo1.camada2 = newIndividuo1.camada2 , newIndividuo2.camada2
        else:
            newIndividuo2.camada3, newIndividuo1.camada3 = newIndividuo1.camada3 , newIndividuo2.camada3

        a = randint(1,3)
        if(a == 1):
            
            newIndividuo1.camada1 = (newIndividuo1.camada1 + newIndividuo2.camada1)/2
            newIndividuo2.camada1 = (newIndividuo1.camada1 + newIndividuo2.camada1)/2
        if(a == 2):
            newIndividuo1.camada2 = (newIndividuo1.camada2 + newIndividuo2.camada2)/2
            newIndividuo2.camada2 = (newIndividuo1.camada2 + newIndividuo2.camada2)/2
        if(a == 3):
            newIndividuo1.camada3 = (newIndividuo1.camada3 + newIndividuo2.camada3)/2
            newIndividuo2.camada3 = (newIndividuo1.camada3 + newIndividuo2.camada3)/2
            
        
     
        

        p1_redes = np.append(newIndividuo1, p1_redes)
        p1_redes = np.append(newIndividuo2, p1_redes)
        print(p1_redes.shape)
        
        return p1_redes
def selecaoNatural(p1_redes,fitness):
    for _ in range(NUM_CRUZAMENTO_POR_EPOCA):
        a = np.argsort(fitness)
        # print(fitness)
        a = a[-2:] #pega os dois menos aptos
        # print(a)
        p1_redes = np.delete(p1_redes, a, axis = 0)
        return p1_redes
        


def fitness(p1_redes,verbose = 0):
    players , sensores = inicializaPlayers(p1_redes.shape[0])
    mainGame(players,p1_redes,sensores,True,verbose)
    fitness = []
    for p1 in players:
        fitness.append(p1.fitness) 
    return  np.array(fitness)
    
    


    
def mutacao(p1_redes):
    for p1_rede, _ in zip(p1_redes,range(100)):
        a = randint(1,100)
        if(a <= TAXA_MUTACAO*100 ):
            for _ in range(numeroNeuronio):
                c = randint(1,3)
                camada = getattr(p1_rede, 'camada'+str(c))
                n = randint(0,camada.shape[0]-1)
                peso =randint(0,camada.shape[1]-1)
                camada[n][peso] = np.random.rand(1)[0]
            
    return p1_redes


                
    

def main():
    p1_redes = []
    

    sensor = {
        'U':0,
        'UCount':0,
        'L':0,
        'LCount':0,
        'R':0,
        'RCount':0,
        'D':0,
        'DCount':0,
        'UR':0,
        'URCount':0,
        'DR':0,
        'DRCount':0,
        'DL':0,
        'DLCount':0,
        'UL':0,
        'ULCount':0
    }
    
    
    #caso queira jogar só
    if(0):
        players = []
        sensores = []
        players.append(Player(1,12))
        p1_redes.append(Neural(len(sensor.values()),np.array([5,3,4])))
        
        # while(1):
        players[0].vida = True
        mainGame(players,p1_redes,sensores,False)
    

    
    else:
        
        # Inicializa pop
        for _ in range(NUM_POP):
            p1_redes.append(Neural(len(sensor.values()),np.array([5,3,4])))

        p1_redes = np.array(p1_redes)    
        
        #Inicio de uma geração
        geracao = 0
        while(geracao < 100000):
            
            
            fitnessArray   = fitness(p1_redes)
            p1_redes = mutacao(p1_redes)

            p1_redes = combinacao_torneio(p1_redes,fitnessArray)
            fitnessArray   = fitness(p1_redes)

            
            
            p1_redes = selecaoNatural(p1_redes,fitnessArray)            
            fitnessArray   = fitness(p1_redes,1)
            print(np.mean(fitnessArray))
            print(np.min(fitnessArray))
            geracao += 1

        

        
        #fim de uma geração






################################################################################################################################################################################
def inicializaPlayers(size = 0):
    sensor = {
        'U':0,
        'UCount':0,
        'L':0,
        'LCount':0,
        'R':0,
        'RCount':0,
        'D':0,
        'DCount':0,
        'UR':0,
        'URCount':0,
        'DR':0,
        'DRCount':0,
        'DL':0,
        'DLCount':0,
        'UL':0,
        'ULCount':0
    }
    players = []
    sensores = []
    
    for _ in range(size):
        players.append(Player(1,12))
        sensores.append(sensor)
    return players,sensores
def mainGame(players,p1_redes,sensores,isMaquina,verbose):
    
    pygame.init()
    DISPLAY = pygame.display.set_mode((SCREENW,SCREENH))
    pygame.display.set_caption('O jogo mais dificl do mundo')
    global enemy
    enemy = []
    criaInimigos()
    # mapa
    mapa = criaMapa(WIDTH,HEIGHT)
    
    ####
    
    
    WHITE=(255,255,255)
    DISPLAY.fill(WHITE)

    #condigura player
    # p1.setMap(mapa)
    
    
    

    count = 0
    fimJogo = False
    NUMERO_RODADA = 0
    while not(fimJogo):
        if(NUMERO_RODADA > MAX_RODADA ):
            for p1 in players:
                if(p1.vida == 1): 
                    funcaoFitness(p1)
                    p1.vida = 0
            print(players[0].fitness)
            print("num maximo de rodada")
            break
        #Vez do player
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); #sys.exit() if sys is imported
            if event.type == pygame.KEYDOWN:
                # print(event.key)
                # pause = p
                if event.key == 112:                    
                    print(p1.__dict__)
                if event.key == 115:                    
                    print(sensor)
                if(movimentaPlayer(players[0],mapa,event.key) == 0): 
                    fimJogo = True
                
                
                

        # Vez do inimigo                    
        for a in enemy:
            a.step(mapa)
        # Vez da Maquina
        readSensor(DISPLAY, mapa,players,sensores)# já configura os sensoress
        if(isMaquina):
            for p1,p1_rede,sensor in zip(players,p1_redes,sensores):
                # print("a")
                if(p1.vida == 1):
                    # print("movimenta")
                    movimento = p1_rede.predict(np.array(list(sensor.values())))
                    movimentaPlayer(p1,mapa,movimento)
                    
        fimJogo = True
        for p1 in players:
            if(p1.vida == 1): 
                fimJogo = False

        showMap(DISPLAY,mapa,players,verbose) 
        
            
        # distancia =pow(pow(p1.x - XFINAL,2) + pow(p1.y - YFINAL,2),0.5)
        # print(distancia)
        
        clock.tick(1000000)
    # retorna o fitness
    
        NUMERO_RODADA += 1
    return 1
    

main()