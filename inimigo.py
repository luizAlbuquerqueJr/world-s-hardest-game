class Inimigo:
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
    def __init__(self, nome,x,y,depth,sentido = 0):
        
        self.id = nome
        self.x = x
        self.y = y
        self.XMin = x - depth
        self.YMin = y - depth
        self.XMax = x + depth
        self.YMax = y + depth
        self.sentido = sentido
    
    def step(self,mapa):
        mapa[self.x][self.y] = 2
        if(self.id == 'v'):
            if(self.sentido == 0):
                if(self.YMax == self.y or mapa[self.x][self.y + 1] == self.PAREDE):
                    # print('mudou e sub')
                    self.sentido = 1
                    self.y -= 1    
                else:
                    # print('add')
                    self.y += 1    
            else:
                if(self.YMin == self.y or mapa[self.x][self.y - 1] == self.PAREDE):
                    # print('mudou e add')
                    self.sentido = 0
                    self.y += 1    
                else:
                    # print('sub')
                    self.y -= 1
            if(self.sentido == 0 ):
                mapa[self.x][self.y] = self.INIMIGOV
            else:
                mapa[self.x][self.y] = self.INIMIGOV
        if(self.id == 'h'):
            if(self.sentido == 0):
                if(self.XMax == self.x or mapa[self.x + 1][self.y] == self.PAREDE):
                    # print('mudou e sub')
                    self.sentido = 1
                    self.x -= 1    
                else:
                    # print('add')
                    self.x += 1    
            else:
                if(self.XMin == self.x or  mapa[self.x -1][self.y] == self.PAREDE):
                    # print('mudou e add')
                    self.sentido = 0
                    self.x += 1    
                else:
                    # print('sub')
                    self.x -= 1    
            
            if(self.sentido == 0 ):
                mapa[self.x][self.y] = self.INIMIGOH
            else:
                mapa[self.x][self.y] = self.INIMIGOHH
        if(self.id == 'd1'):
            if(self.sentido == 0):
                if(self.XMax == self.x or mapa[self.x + 1][self.y + 1] == 0):
                    # print('mudou e sub')
                    self.sentido = 1
                    self.x -= 1    
                    self.y -= 1
                else:
                    # print('add')
                    self.x += 1
                    self.y += 1    
            else:
                if(self.XMin == self.x or  mapa[self.x -1][self.y-1] == 0):
                    # print('mudou e add')
                    self.sentido = 0
                    self.x += 1
                    self.y += 1    
                else:
                    # print('sub')
                    self.x -= 1    
                    self.y -= 1
            
            if(self.sentido == 0 ):
                mapa[self.x][self.y] = self.INIMIGOD1
            else:
                mapa[self.x][self.y] = self.INIMIGOD11
        if(self.id == 'd2'):
            if(self.sentido == 0):
                if(self.XMin == self.x or mapa[self.x - 1][self.y + 1] == 0):
                    # print('mudou e sub')
                    self.sentido = 1
                    self.x += 1    
                    self.y -= 1
                else:
                    # print('add')
                    self.x -= 1
                    self.y += 1    
            else:
                if(self.XMax == self.x or  mapa[self.x +1][self.y-1] == 0):
                    # print('mudou e add')
                    self.sentido = 0
                    self.x -= 1
                    self.y += 1    
                else:
                    # print('sub')
                    self.x += 1    
                    self.y -= 1
            
            if(self.sentido == 0 ):
                mapa[self.x][self.y] = self.INIMIGOD1
            else:
                mapa[self.x][self.y] = self.INIMIGOD11
            

                
                
        