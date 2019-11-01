import numpy as np
class Player:
    #constantes do mapa
    LIVRE = 2
    PAREDE = 0
    INICIO = 1
    INIMIGO = 3
    PLAYER = 999

    MOV_UP = -1
    MOV_DOWN = -2
    MOV_LEFT = -3
    MOV_RIGHt = -4
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vida = 1
        self.fitness = 999

        # mapa[x][y] = self.PLAYER
    # def setMap(self,mapa):
    #     self.mapaPlayer = np.zeros((len(mapa),len(mapa)))
        
        
    def step(self,mapa,movimento):
        
        if(movimento == self.MOV_DOWN):
            if(mapa[self.x][self.y+1] == self.PAREDE):
                
                self.vida = 0
                return False
            else:
                self.y += 1
                
                
        if(movimento == self.MOV_RIGHt):
            if(mapa[self.x +1 ][self.y] == self.PAREDE):
                
                self.vida = 0
                return False
            else:
                if(self.x != len(mapa[0])):
                    self.x += 1
                
        if(movimento == self.MOV_UP):
            if(mapa[self.x][self.y-1] == self.PAREDE ):
                
                self.vida = 0
                return False
            else:
                self.y -= 1
                
        if(movimento == self.MOV_LEFT):
            if(mapa[self.x -1 ][self.y] == self.PAREDE):
                
                self.vida = 0
                return False
            else:
                if(self.x != 0):
                    self.x -= 1
                
        return True
    