import pygame, sys
from pygame.locals import *
import numpy as np 
from inimigo import Inimigo
from player import Player

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

def showMap(DISPLAY,matrixMap,p1):
    
    
    
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
    
    
    if(matrixMap[p1.x][p1.y] > INIMIGO):
        print("morreu")
    else:
        pygame.draw.rect(DISPLAY,YELLOW,(p1.x*SIZE_OBJECT,p1.y*SIZE_OBJECT,SIZE_OBJECT,SIZE_OBJECT))
    readSensor(DISPLAY,matrixMap,p1,sensor)
    pygame.display.update()
    
def readSensor(DISPLAY,matrixMap,p1,sensor):
    count = 0
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

    print(sensor['UL'],count)
    


def criaInimigos():
    enemy.append(Inimigo('v',16,25,10))
    enemy.append(Inimigo('v',18,25,10))
    enemy.append(Inimigo('v',20,25,10))
    enemy.append(Inimigo('v',22,25,10))
    enemy.append(Inimigo('v',24,25,10))
    enemy.append(Inimigo('v',26,25,10))
    enemy.append(Inimigo('v',28,25,10))
    enemy.append(Inimigo('v',30,25,10))
    enemy.append(Inimigo('v',30,25,10))

    enemy.append(Inimigo('h',25,16,10))
    enemy.append(Inimigo('h',25,18,10))
    enemy.append(Inimigo('h',25,20,10))
    enemy.append(Inimigo('h',25,22,10))
    enemy.append(Inimigo('h',25,24,10))
    enemy.append(Inimigo('h',25,26,10))
    enemy.append(Inimigo('h',25,28,10))
    enemy.append(Inimigo('h',25,30,10))
    enemy.append(Inimigo('h',25,30,10))

    enemy.append(Inimigo('d1',25,16,10))
    enemy.append(Inimigo('d1',25,18,10))
    enemy.append(Inimigo('d1',25,20,10))
    enemy.append(Inimigo('d1',25,22,10))
    enemy.append(Inimigo('d1',25,24,10))
    enemy.append(Inimigo('d1',25,26,10))
    enemy.append(Inimigo('d1',25,28,10))
    enemy.append(Inimigo('d1',25,30,10))
    enemy.append(Inimigo('d1',25,30,10))


    
    
    enemy.append(Inimigo('d2',25,18,10))
    enemy.append(Inimigo('d2',25,20,10))
    enemy.append(Inimigo('d2',25,22,10))
    enemy.append(Inimigo('d2',25,24,10))
    enemy.append(Inimigo('d2',25,26,10))
    enemy.append(Inimigo('d2',25,28,10))
    enemy.append(Inimigo('d2',25,30,10))
    enemy.append(Inimigo('d2',25,30,10))
    
    
    enemy.append(Inimigo('v',22,30,50))
    enemy.append(Inimigo('h',10,30,10))
def criaMapa(WIDTH,HEIGHT):
    mapa = np.loadtxt(open("mapa.csv", "rb"), delimiter=",", skiprows=1)
    mapa = np.transpose(mapa)
    print(mapa.shape)
    
    
    
    

    return mapa


def main():
    
    pygame.init()
    DISPLAY = pygame.display.set_mode((SCREENW,SCREENH))
    pygame.display.set_caption('O jogo mais dificl do mundo')
    
    criaInimigos()
    # mapa
    mapa = criaMapa(WIDTH,HEIGHT)
    
    ####
    
    
    WHITE=(255,255,255)
    DISPLAY.fill(WHITE)

    #cria player
    p1 = Player(mapa,1,12)
    readSensor(DISPLAY, mapa,p1,sensor)# já configura os sensoress
    

    count = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); #sys.exit() if sys is imported
            if event.type == pygame.KEYDOWN:
                if event.key == 276:
                    if(not(p1.step(mapa,MOV_LEFT))):
                        print("GAME OVER")
                if event.key == 275:
                    if(not(p1.step(mapa,MOV_RIGHt))):
                        print("GAME OVER")
                if event.key == 273:
                    if(not(p1.step(mapa,MOV_UP))):
                        print("GAME OVER")
                if event.key == 274:
                    if(not(p1.step(mapa,MOV_DOWN))):
                        print("GAME OVER")
                    
        for a in enemy:
            a.step(mapa)

        
        
        showMap(DISPLAY,mapa,p1)
        
        # clock.tick(3)

main()