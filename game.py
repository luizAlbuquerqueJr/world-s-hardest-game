import pygame, sys
from pygame.locals import *
import numpy as np 
import copy
from random import randint
import matplotlib.pyplot as plt

from inimigo import Inimigo
from player import Player
from neural import Neural
# from neural import Neural
import time



#constante do AG
NUM_CRUZAMENTO_POR_EPOCA = 1
NUM_INVIDUOS_TORNEIO = 50
NUM_POP = 100
TAXA_MUTACAO = 0
# NUM_INVIDUOS_TORNEIO = 50
# NUM_POP = 500
TAXA_MUTACAO = 0
numeroNeuronio = 1


MAX_RODADA = 180

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



def showMap(DISPLAY,matrixMap,players,verbose=0,bestIndviduo = 0):    
    
    
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
    
    for p1, index in zip(players,range(len(players))):
        if(matrixMap[p1.x][p1.y] > INIMIGO):
            p1.vida = 0
            funcaoFitness(p1)
            # print("morreu")
            
        else:
            if(index == bestIndviduo):
                pygame.draw.rect(DISPLAY,(0,255,255),(p1.x*SIZE_OBJECT,p1.y*SIZE_OBJECT,SIZE_OBJECT,SIZE_OBJECT))
            elif(p1.vida == 0):
                pygame.draw.rect(DISPLAY,(128,128,128),(p1.x*SIZE_OBJECT,p1.y*SIZE_OBJECT,SIZE_OBJECT,SIZE_OBJECT))
            else:
                pygame.draw.rect(DISPLAY,(0,255,0),(p1.x*SIZE_OBJECT,p1.y*SIZE_OBJECT,SIZE_OBJECT,SIZE_OBJECT))
    if(verbose == 1):
        pass# TODO : Descomentar
        pygame.display.update() 
    return 1
def funcaoFitness(p1):
    #Posicai do fim do jogo
    XFINAL = 45
    YFINAL = 13
    distIntermediaria = 0
    if(p1.x < 5):
        XIntermediario = 5
        YIntermediario = 33
        distIntermediaria = (pow(pow(p1.x - XIntermediario,2) + pow(p1.y - YIntermediario,2),0.5))
        p1.fitness = distIntermediaria + (pow(pow(XIntermediario - XFINAL,2) + pow(YIntermediario - YFINAL,2),0.5))
    else:
        p1.fitness =pow(pow(p1.x - XFINAL,2) + pow(p1.y - YFINAL,2),0.5)
    


    
def readSensor(DISPLAY,matrixMap,players,sensores,bestIndviduo):
    count = 0
    # print(len(players),len(sensores))
    for p1, sensor, index  in zip(players,sensores,range(len(players))):
        # if(bestIndviduo!=-1):
        #     print('Atualizando sensor ',index,"   melhor ind sensor",bestIndviduo, sensores[bestIndviduo])
    
        count = 0
        while(p1.x+count < 50 and matrixMap[p1.x+count][p1.y] != PAREDE and matrixMap[p1.x+count][p1.y] < INIMIGO):
            count +=1
        pygame.draw.line(DISPLAY, (0,150,0), (p1.x*SIZE_OBJECT, p1.y*SIZE_OBJECT), ((p1.x+ count)*SIZE_OBJECT, p1.y*SIZE_OBJECT))
        sensor['R'] = matrixMap[p1.x + count][p1.y]
        sensor['RCount'] = count
        # if(bestIndviduo == index and bestIndviduo != -1):
        #     print("melhor ind sensor R",count)
        
        

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
        sensor['D'] = matrixMap[p1.x][p1.y+count]
        sensor['DCount'] = count

        count = 0
        while(matrixMap[p1.x][p1.y - count] != PAREDE and matrixMap[p1.x][p1.y - count] < INIMIGO ):
            count +=1
        pygame.draw.line(DISPLAY, (0,150,0), ((p1.x)*SIZE_OBJECT, (p1.y-count)*SIZE_OBJECT), ((p1.x)*SIZE_OBJECT, p1.y*SIZE_OBJECT))
        sensor['U'] = matrixMap[p1.x][p1.y - count]
        sensor['UCount'] = count
        # if(index == 5):
            # print("UCount",sensor['UCount'])

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

def criaInimigos():
    pass
    enemy.append(Inimigo('v',6,25,50,0))
    enemy.append(Inimigo('v',8,25,50,0))
    enemy.append(Inimigo('v',10,25,50,0))
    enemy.append(Inimigo('v',12,25,50,0))
    enemy.append(Inimigo('v',14,25,50,0))
    enemy.append(Inimigo('v',16,25,50,0))
    enemy.append(Inimigo('v',18,25,50,0))
    enemy.append(Inimigo('v',20,25,50,0))
    enemy.append(Inimigo('v',22,25,50,0))
    enemy.append(Inimigo('v',24,25,50,0))
    enemy.append(Inimigo('v',26,25,50,0))
    enemy.append(Inimigo('v',28,25,50,0))
    enemy.append(Inimigo('v',30,25,50,0))
    enemy.append(Inimigo('v',32,25,50,0))
    enemy.append(Inimigo('v',34,25,50,0))
    enemy.append(Inimigo('v',36,25,50,0))
    enemy.append(Inimigo('v',38,25,50,0))
    enemy.append(Inimigo('v',40,25,50,0))
    enemy.append(Inimigo('v',42,25,50,0))

    enemy.append(Inimigo('v',6,20,50,0))
    enemy.append(Inimigo('v',8,20,50,0))
    enemy.append(Inimigo('v',10,20,50,0))
    enemy.append(Inimigo('v',12,20,50,0))
    enemy.append(Inimigo('v',14,20,50,0))
    enemy.append(Inimigo('v',16,20,50,0))
    enemy.append(Inimigo('v',18,20,50,0))
    enemy.append(Inimigo('v',20,20,50,0))
    enemy.append(Inimigo('v',22,20,50,0))
    enemy.append(Inimigo('v',24,20,50,0))
    enemy.append(Inimigo('v',26,20,50,0))
    enemy.append(Inimigo('v',28,20,50,0))
    enemy.append(Inimigo('v',30,20,50,0))
    enemy.append(Inimigo('v',32,20,50,0))
    enemy.append(Inimigo('v',34,20,50,0))
    enemy.append(Inimigo('v',36,20,50,0))
    enemy.append(Inimigo('v',38,20,50,0))
    enemy.append(Inimigo('v',40,20,50,0))
    enemy.append(Inimigo('v',42,20,50,0))

    enemy.append(Inimigo('v',6,20,50,1))
    enemy.append(Inimigo('v',8,20,50,1))
    enemy.append(Inimigo('v',10,20,50,1))
    enemy.append(Inimigo('v',12,20,50,1))
    enemy.append(Inimigo('v',14,20,50,1))
    enemy.append(Inimigo('v',16,20,50,1))
    enemy.append(Inimigo('v',18,20,50,1))
    enemy.append(Inimigo('v',20,20,50,1))
    enemy.append(Inimigo('v',22,20,50,1))
    enemy.append(Inimigo('v',24,20,50,1))
    enemy.append(Inimigo('v',26,20,50,1))
    enemy.append(Inimigo('v',28,20,50,1))
    enemy.append(Inimigo('v',30,20,50,1))
    enemy.append(Inimigo('v',32,20,50,1))
    enemy.append(Inimigo('v',34,20,50,1))
    enemy.append(Inimigo('v',36,20,50,1))
    enemy.append(Inimigo('v',38,20,50,1))
    enemy.append(Inimigo('v',40,20,50,1))
    enemy.append(Inimigo('v',42,20,50,1))

    enemy.append(Inimigo('v',6,15,50,1))
    enemy.append(Inimigo('v',8,15,50,1))
    enemy.append(Inimigo('v',10,15,50,1))
    enemy.append(Inimigo('v',12,15,50,1))
    enemy.append(Inimigo('v',14,15,50,1))
    enemy.append(Inimigo('v',16,15,50,1))
    enemy.append(Inimigo('v',18,15,50,1))
    enemy.append(Inimigo('v',20,15,50,1))
    enemy.append(Inimigo('v',22,15,50,1))
    enemy.append(Inimigo('v',24,15,50,1))
    enemy.append(Inimigo('v',26,15,50,1))
    enemy.append(Inimigo('v',28,15,50,1))
    enemy.append(Inimigo('v',30,15,50,1))
    enemy.append(Inimigo('v',32,15,50,1))
    enemy.append(Inimigo('v',34,15,50,1))
    enemy.append(Inimigo('v',36,15,50,1))
    enemy.append(Inimigo('v',38,15,50,1))
    enemy.append(Inimigo('v',40,15,50,1))
    enemy.append(Inimigo('v',42,15,50,1))

    enemy.append(Inimigo('v',6,30,50,1))
    enemy.append(Inimigo('v',8,30,50,1))
    enemy.append(Inimigo('v',10,30,50,1))
    enemy.append(Inimigo('v',12,30,50,1))
    enemy.append(Inimigo('v',14,30,50,1))
    enemy.append(Inimigo('v',16,30,50,1))
    enemy.append(Inimigo('v',18,30,50,1))
    enemy.append(Inimigo('v',20,30,50,1))
    enemy.append(Inimigo('v',22,30,50,1))
    enemy.append(Inimigo('v',24,30,50,1))
    enemy.append(Inimigo('v',26,30,50,1))
    enemy.append(Inimigo('v',28,30,50,1))
    enemy.append(Inimigo('v',30,30,50,1))
    enemy.append(Inimigo('v',32,30,50,1))
    enemy.append(Inimigo('v',34,30,50,1))
    enemy.append(Inimigo('v',36,30,50,1))
    enemy.append(Inimigo('v',38,30,50,1))
    enemy.append(Inimigo('v',40,30,50,1))
    enemy.append(Inimigo('v',42,30,50,1))

    

    enemy.append(Inimigo('v',20,25,50,1))
    enemy.append(Inimigo('v',21,25,50,1))
    enemy.append(Inimigo('v',22,25,50,1))
    enemy.append(Inimigo('v',23,25,50,1))
    enemy.append(Inimigo('v',24,25,50,1))
    enemy.append(Inimigo('v',25,25,50,1))
    enemy.append(Inimigo('v',26,25,50,1))
    enemy.append(Inimigo('v',27,25,50,1))

    enemy.append(Inimigo('h',24,20,50,1))
    enemy.append(Inimigo('h',24,21,50,1))
    enemy.append(Inimigo('h',24,22,50,1))
    enemy.append(Inimigo('h',24,23,50,1))
    enemy.append(Inimigo('h',24,24,50,1))
    enemy.append(Inimigo('h',24,25,50,1))
    enemy.append(Inimigo('h',24,26,50,1))
    enemy.append(Inimigo('h',24,27,50,1))

    # enemy.append(Inimigo('v',7,25,50,1))
    # enemy.append(Inimigo('v',9,25,50,1))
    # enemy.append(Inimigo('v',11,25,50,1))
    # enemy.append(Inimigo('v',13,25,50,1))
    # enemy.append(Inimigo('v',15,25,50,1))
    # enemy.append(Inimigo('v',17,25,50,1))
    # enemy.append(Inimigo('v',19,25,50,1))
    # enemy.append(Inimigo('v',21,25,50,1))
    # enemy.append(Inimigo('v',23,25,50,1))
    # enemy.append(Inimigo('v',25,25,50,1))
    # enemy.append(Inimigo('v',27,25,50,1))
    # enemy.append(Inimigo('v',29,25,50,1))
    # enemy.append(Inimigo('v',31,25,50,1))
    # enemy.append(Inimigo('v',33,25,50,1))
    # enemy.append(Inimigo('v',35,25,50,1))
    # enemy.append(Inimigo('v',37,25,50,1))
    # enemy.append(Inimigo('v',39,25,50,1))
    # enemy.append(Inimigo('v',41,25,50,1))
    


    enemy.append(Inimigo('h',20,12,18,0))
    enemy.append(Inimigo('h',20,14,18,0))
    enemy.append(Inimigo('h',20,16,18,0))
    enemy.append(Inimigo('h',20,18,18,0))
    enemy.append(Inimigo('h',20,20,18,0))
    enemy.append(Inimigo('h',20,22,18,0))
    enemy.append(Inimigo('h',20,24,18,0))
    enemy.append(Inimigo('h',20,26,18,0))
    enemy.append(Inimigo('h',20,28,18,0))
    enemy.append(Inimigo('h',20,30,18,0))
    enemy.append(Inimigo('h',20,30,18,0))
    enemy.append(Inimigo('h',20,32,18,0))
    enemy.append(Inimigo('h',20,34,18,0))
     
    enemy.append(Inimigo('h',20,12,18,1))
    enemy.append(Inimigo('h',20,14,18,1))
    enemy.append(Inimigo('h',20,16,18,1))
    enemy.append(Inimigo('h',20,18,18,1))
    enemy.append(Inimigo('h',20,20,18,1))
    enemy.append(Inimigo('h',20,22,18,1))
    enemy.append(Inimigo('h',20,24,18,1))
    enemy.append(Inimigo('h',20,26,18,1))
    enemy.append(Inimigo('h',20,28,18,1))
    enemy.append(Inimigo('h',20,30,18,1))
    enemy.append(Inimigo('h',20,30,18,1))
    enemy.append(Inimigo('h',20,32,18,1))
    enemy.append(Inimigo('h',20,34,18,1))

    enemy.append(Inimigo('h',28,12,18,0))
    enemy.append(Inimigo('h',28,14,18,0))
    enemy.append(Inimigo('h',28,16,18,0))
    enemy.append(Inimigo('h',28,18,18,0))
    enemy.append(Inimigo('h',28,20,18,0))
    enemy.append(Inimigo('h',28,22,18,0))
    enemy.append(Inimigo('h',28,24,18,0))
    enemy.append(Inimigo('h',28,26,18,0))
    enemy.append(Inimigo('h',28,28,18,0))
    enemy.append(Inimigo('h',28,30,18,0))
    enemy.append(Inimigo('h',28,30,18,0))
    enemy.append(Inimigo('h',28,32,18,0))
    enemy.append(Inimigo('h',28,34,18,0))
     
    enemy.append(Inimigo('h',28,12,18,1))
    enemy.append(Inimigo('h',28,14,18,1))
    enemy.append(Inimigo('h',28,16,18,1))
    enemy.append(Inimigo('h',28,18,18,1))
    enemy.append(Inimigo('h',28,20,18,1))
    enemy.append(Inimigo('h',28,22,18,1))
    enemy.append(Inimigo('h',28,24,18,1))
    enemy.append(Inimigo('h',28,26,18,1))
    enemy.append(Inimigo('h',28,28,18,1))
    enemy.append(Inimigo('h',28,30,18,1))
    enemy.append(Inimigo('h',28,30,18,1))
    enemy.append(Inimigo('h',28,32,18,1))
    enemy.append(Inimigo('h',28,34,18,1))

    enemy.append(Inimigo('h',24,12,18,0))
    enemy.append(Inimigo('h',24,14,18,0))
    enemy.append(Inimigo('h',24,16,18,0))
    enemy.append(Inimigo('h',24,18,18,0))
    enemy.append(Inimigo('h',24,20,18,0))
    enemy.append(Inimigo('h',24,22,18,0))
    enemy.append(Inimigo('h',24,24,18,0))
    enemy.append(Inimigo('h',24,26,18,0))
    enemy.append(Inimigo('h',24,28,18,0))
    enemy.append(Inimigo('h',24,30,18,0))
    enemy.append(Inimigo('h',24,30,18,0))
    enemy.append(Inimigo('h',24,32,18,0))
    enemy.append(Inimigo('h',24,34,18,0))

    

    enemy.append(Inimigo('h',24,12,18,1))
    enemy.append(Inimigo('h',24,14,18,1))
    enemy.append(Inimigo('h',24,16,18,1))
    enemy.append(Inimigo('h',24,18,18,1))
    enemy.append(Inimigo('h',24,20,18,1))
    enemy.append(Inimigo('h',24,22,18,1))
    enemy.append(Inimigo('h',24,24,18,1))
    enemy.append(Inimigo('h',24,26,18,1))
    enemy.append(Inimigo('h',24,28,18,1))
    enemy.append(Inimigo('h',24,30,18,1))
    enemy.append(Inimigo('h',24,30,18,1))
    enemy.append(Inimigo('h',24,32,18,1))
    enemy.append(Inimigo('h',24,34,18,1))
    
    
    
    enemy.append(Inimigo('d1',7,25,50,1))
    enemy.append(Inimigo('d1',9,25,50,1))
    enemy.append(Inimigo('d1',11,25,50,1))
    enemy.append(Inimigo('d1',13,25,50,1))
    enemy.append(Inimigo('d1',15,25,50,1))
    enemy.append(Inimigo('d1',17,25,50,1))
    enemy.append(Inimigo('d1',19,25,50,1))
    enemy.append(Inimigo('d1',21,25,50,1))
    enemy.append(Inimigo('d1',23,25,50,1))
    enemy.append(Inimigo('d1',25,25,50,1))
    enemy.append(Inimigo('d1',27,25,50,1))
    enemy.append(Inimigo('d1',29,25,50,1))
    enemy.append(Inimigo('d1',31,25,50,1))
    enemy.append(Inimigo('d1',33,25,50,1))
    enemy.append(Inimigo('d1',35,25,50,1))
    enemy.append(Inimigo('d1',37,25,50,1))
    enemy.append(Inimigo('d1',39,25,50,1))
    enemy.append(Inimigo('d1',41,25,50,1))


    
    
    enemy.append(Inimigo('d2',7,25,50,1))
    enemy.append(Inimigo('d2',9,25,50,1))
    enemy.append(Inimigo('d2',11,25,50,1))
    enemy.append(Inimigo('d2',13,25,50,1))
    enemy.append(Inimigo('d2',15,25,50,1))
    enemy.append(Inimigo('d2',17,25,50,1))
    enemy.append(Inimigo('d2',19,25,50,1))
    enemy.append(Inimigo('d2',21,25,50,1))
    enemy.append(Inimigo('d2',23,25,50,1))
    enemy.append(Inimigo('d2',25,25,50,1))
    enemy.append(Inimigo('d2',27,25,50,1))
    enemy.append(Inimigo('d2',29,25,50,1))
    enemy.append(Inimigo('d2',31,25,50,1))
    enemy.append(Inimigo('d2',33,25,50,1))
    enemy.append(Inimigo('d2',35,25,50,1))
    enemy.append(Inimigo('d2',37,25,50,1))
    enemy.append(Inimigo('d2',39,25,50,1))
    enemy.append(Inimigo('d2',41,25,50,1))

    


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
        
        newIndividuo10 = Neural(p1_redes[0].nInput,np.array([0,0,0]))
        newIndividuo20 = Neural(p1_redes[0].nInput,np.array([0,0,0]))
        
    
        isEqual = False
        while(np.array_equal(newIndividuo10.camada1, newIndividuo20.camada1) and np.array_equal(newIndividuo10.camada2, newIndividuo20.camada2) and np.array_equal(newIndividuo10.camada3, newIndividuo20.camada3) ) :
            # print('asdds')
            isEqual = True
            individuosSelecionados = np.random.choice(NUM_POP, NUM_INVIDUOS_TORNEIO, replace=False)    
            
            a = np.argsort(fitness[individuosSelecionados])
            
            a = a[:2] #pega os dois mais aptos
            newIndividuo1 = copy.deepcopy(p1_redes[individuosSelecionados][a[0]])
            newIndividuo10 = copy.deepcopy(p1_redes[individuosSelecionados][a[0]])
            newIndividuo11 = copy.deepcopy(p1_redes[individuosSelecionados][a[0]])
            newIndividuo12 = copy.deepcopy(p1_redes[individuosSelecionados][a[0]])
            
            newIndividuo2 = copy.deepcopy(p1_redes[individuosSelecionados][a[1]])
            newIndividuo20 = copy.deepcopy(p1_redes[individuosSelecionados][a[1]])
            newIndividuo21 = copy.deepcopy(p1_redes[individuosSelecionados][a[1]])
            newIndividuo22 = copy.deepcopy(p1_redes[individuosSelecionados][a[1]])

        # print("\tPai 1: ")
        # print("camada1: ",newIndividuo1.camada1)
        # print("camada2: ",newIndividuo1.camada2)
        # print("camada3: ",newIndividuo1.camada3)    
        # print("\tPai 2: ")
        # print("camada1: ",newIndividuo2.camada1)
        # print("camada2: ",newIndividuo2.camada2)
        # print("camada3: ",newIndividuo2.camada3)

        newIndividuo10.camada1 = copy.deepcopy(newIndividuo2.camada1)
        newIndividuo11.camada2 = copy.deepcopy(newIndividuo2.camada2)
        newIndividuo12.camada3 = copy.deepcopy(newIndividuo2.camada3)

        newIndividuo20.camada1 = copy.deepcopy(newIndividuo1.camada1)
        newIndividuo21.camada2 = copy.deepcopy(newIndividuo1.camada2)
        newIndividuo22.camada3 = copy.deepcopy(newIndividuo1.camada3)
        # print("\tnewindviduo10: ")
        # print("camada1: ",newIndividuo10.camada1)
        # print("camada2: ",newIndividuo10.camada2)
        # print("camada3: ",newIndividuo10.camada3)
        # print("\tnewindviduo11: ")
        # print("camada1: ",newIndividuo11.camada1)
        # print("camada2: ",newIndividuo11.camada2)
        # print("camada3: ",newIndividuo11.camada3)
        # print("\tnewindviduo12: ")
        # print("camada1: ",newIndividuo12.camada1)
        # print("camada2: ",newIndividuo12.camada2)
        # print("camada3: ",newIndividuo12.camada3)
        # print("\tnewindviduo20: ")
        # print("camada1: ",newIndividuo20.camada1)
        # print("camada2: ",newIndividuo20.camada2)
        # print("camada3: ",newIndividuo20.camada3)
        # print("\tnewindviduo21: ")
        # print("camada1: ",newIndividuo21.camada1)
        # print("camada2: ",newIndividuo21.camada2)
        # print("camada3: ",newIndividuo21.camada3)
        # print("\tnewindviduo22: ")
        # print("camada1: ",newIndividuo22.camada1)
        # print("camada2: ",newIndividuo22.camada2)
        # print("camada3: ",newIndividuo22.camada3)
        
        # if(randint(0,1)):
        #     newIndividuo2.camada1, newIndividuo1.camada1 = newIndividuo1.camada1 , newIndividuo2.camada1
        # elif(randint(0,1)):
        #     newIndividuo2.camada2, newIndividuo1.camada2 = newIndividuo1.camada2 , newIndividuo2.camada2
        # else:
        #     newIndividuo2.camada3, newIndividuo1.camada3 = newIndividuo1.camada3 , newIndividuo2.camada3

        # a = randint(1,3)
        # if(a == 1):
            
        #     newIndividuo1.camada1 = (newIndividuo1.camada1 + newIndividuo2.camada1)/2
        #     newIndividuo2.camada1 = (newIndividuo1.camada1 + newIndividuo2.camada1)/2
        # if(a == 2):
        #     newIndividuo1.camada2 = (newIndividuo1.camada2 + newIndividuo2.camada2)/2
        #     newIndividuo2.camada2 = (newIndividuo1.camada2 + newIndividuo2.camada2)/2
        # if(a == 3):
        #     newIndividuo1.camada3 = (newIndividuo1.camada3 + newIndividuo2.camada3)/2
        #     newIndividuo2.camada3 = (newIndividuo1.camada3 + newIndividuo2.camada3)/2
            
        
     
        

        p1_redes = np.append(copy.deepcopy(newIndividuo10), p1_redes)
        p1_redes = np.append(copy.deepcopy(newIndividuo11), p1_redes)
        p1_redes = np.append(copy.deepcopy(newIndividuo12), p1_redes)
        p1_redes = np.append(copy.deepcopy(newIndividuo20), p1_redes)
        p1_redes = np.append(copy.deepcopy(newIndividuo21), p1_redes)
        p1_redes = np.append(copy.deepcopy(newIndividuo22), p1_redes)
        # print(p1_redes.shape)
        
        return p1_redes
def selecaoNatural(p1_redes,fitness):
    a = []
    for i in range(6):
        
        ocorencias = np.where(fitness == fitness[i])
        # if(len(ocorencias[0])!=1):
        #     a.append(i)
        # else:
        #     print("gerou ind diferente")

        for indexOcorrencia in ocorencias[0]:
            # a.append(i)
            # break
            isNew = True
            # if( i !=indexOcorrencia and  np.array_equal(p1_redes[i].camada1, p1_redes[indexOcorrencia].camada1)):
            if( i !=indexOcorrencia and (np.array_equal(p1_redes[i].camada1, p1_redes[indexOcorrencia].camada1) or np.array_equal(p1_redes[i].camada2, p1_redes[indexOcorrencia].camada2) or np.array_equal(p1_redes[i].camada3, p1_redes[indexOcorrencia].camada3))):            
                pass
                a.append(i)
                break
            else:
                isNew = False
        if(isNew):
            print("novo ind")
                        
    print("a")
    print(a)
    p1_redes = np.delete(p1_redes, a, axis = 0)
    fitness = np.delete(fitness, a, axis = 0)


        


    for _ in range(NUM_CRUZAMENTO_POR_EPOCA):
        if(len(a)!=6):
            b = np.argsort(fitness)
            # print(fitness)
            b = b[-(6-len(a)):] #pega os dois menos aptos
            # b = b[-6:] #pega os dois menos aptos
            # print(b)
            p1_redes = np.delete(p1_redes, b, axis = 0)
            fitness = np.delete(fitness, b, axis = 0)
        return p1_redes
        


def fitness(p1_redes,verbose = 0,bestIndviduo=-1):
    players , sensores = inicializaPlayers(p1_redes.shape[0])
    mainGame(players,p1_redes,sensores,True,verbose,bestIndviduo)
    fitness = []
    for p1 in players:
        fitness.append(p1.fitness) 
    return  np.array(fitness)
    
    


    
def mutacao(p1_redes,fitnessArray):
    # print(fitnessArray[:10])
    fit = np.argsort(fitnessArray)
    fit = fit[:20] #pega os 5 melhores
    print(fit)
    print(fitnessArray[fit])
    for p1_rede, index in zip(p1_redes,range(len(p1_redes))):
        if not(index in fit):
            a = randint(1,100)

            if(a <= TAXA_MUTACAO*100 ):
                for _ in range(numeroNeuronio):
                    c = randint(1,3)
                    camada = getattr(p1_rede, 'camada'+str(c))
                    n = randint(0,camada.shape[0]-1)
                    
                    camada[n] = np.random.uniform(low = -1,high = 1,size = (1,len(camada[n])))
                
                
                
            
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
        players , sensores = inicializaPlayers(1)
        # players.append(Player(1,12))
        
        p1_redes.append(Neural(len(sensor.values()),np.array([5,3,4])))
        
        # while(1):
        players[0].vida = True
        mainGame(players,p1_redes,sensores,False,1)
            
    else:
        
        # Inicializa pop
        for index in range(NUM_POP):
            # p1_redes.append(Neural(len(sensor.values()),np.array([2,2,4])))
            p1_redes.append(Neural(len(sensor.values()),np.array([10,10,4])))
            if(index < 1):
                p1_redes[index].load()

        p1_redes = np.array(p1_redes)    
        
        #Inicio de uma geração
        geracao = 0
        fitness_avg = []
        fitness_min = []
        fitness_max = []
        while(geracao < 100000):
            
            
            if(geracao ==0):
                fitnessArray   = fitness(p1_redes,0)
            else:
                fitnessArray   = fitness(p1_redes,1,np.argmin(fitnessArray))    
            fitness_avg.append(np.mean(fitnessArray))
            fitness_min.append(np.min(fitnessArray))
            fitness_max.append(np.max(fitnessArray))
            if(geracao > 2):
                name = 'Stage2Geracao'+str(0)
                plt.figure(figsize=(10, 4))
                plt.title(name)
                plt.xlabel('Geração')
                plt.ylabel('Fitness')
                plt.grid(True)
                plt.plot(fitness_avg, color='#17a589') # green
                plt.plot(fitness_min, color='#175189')
                plt.plot(fitness_max, color='#ff0000')
                plt.savefig('imgs/' + name + '.png')
            
            p1_redes[np.argmin(fitnessArray)].save()
            print('Geracao: ',geracao)
            
            print('Média da populacao: ',np.mean(fitnessArray))
            print('Melhor fitness: ', np.min(fitnessArray))
            
            # fitnessArray   = fitness(p1_redes,1,5)
            

            p1_redes = combinacao_torneio(p1_redes,fitnessArray)
            # print("passou torneio")
            fitnessArray   = fitness(p1_redes,0)
            p1_redes = mutacao(p1_redes,fitnessArray)
            fitnessArray   = fitness(p1_redes,0,np.argmin(fitnessArray))
            
            p1_redes = selecaoNatural(p1_redes,fitnessArray)            
            
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
        sensores.append(copy.deepcopy(sensor))
    return players,sensores
def mainGame(players,p1_redes,sensores,isMaquina,verbose,bestIndviduo=-1):
    
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
    # bestIndviduo = 5
    while not(fimJogo):
        if(isMaquina and NUMERO_RODADA > MAX_RODADA ):
            for p1 in players:
                if(p1.vida == 1): 
                    funcaoFitness(p1)
                    p1.vida = 0
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
                    readSensor(DISPLAY, mapa,players,sensores,-1)# já configura os sensoress
                    print(sensores)
                if(movimentaPlayer(players[0],mapa,event.key) == 0): 
                    fimJogo = True
                
                
                

        # Vez do inimigo                    
        for a in enemy:
            a.step(mapa)
        # Vez da Maquina
        
        if(isMaquina):
            for p1,p1_rede,sensor,index in zip(players,p1_redes,sensores,range(len(players))):        
                if(p1.vida == 1):    
                    movimento = p1_rede.predict(np.array(list(sensor.values())))
                    movimentaPlayer(p1,mapa,movimento)
                    
                    
        fimJogo = True
        for p1 in players:
            if(p1.vida == 1): 
                fimJogo = False
        
        
        
        showMap(DISPLAY,mapa,players,verbose,bestIndviduo) 
        readSensor(DISPLAY, mapa,players,sensores,bestIndviduo)# já configura os sensoress        
        # time.sleep(3)  
        # clock.tick(2)
    
        NUMERO_RODADA += 1
    return 1
    
main()