class Inimigo:
    #constantes do mapa
    LIVRE = 2
    PAREDE = 0
    INICIO = 1
    INIMIGO = 3
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
            mapa[self.x][self.y] = 3
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
            mapa[self.x][self.y] = 3
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
            mapa[self.x][self.y] = 3
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
            mapa[self.x][self.y] = 3

                
                
        