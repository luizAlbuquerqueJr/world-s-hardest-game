
import numpy as np
from tempfile import TemporaryFile
class Neural:
    
    
    #camadas = [5,3,4]
    #nIput =  numero de features

    #         c1    c2    c3
    #         *           *
    #         *     *     *
    # X  -->  *     *     *   --> Y
    #         *     *     *
    #         *           
    def sigmoid(x):                                        
        return 1 / (1 + np.exp(-x))
    def load(self):
        self.camada1 = np.load('bestobject1/camada1.npy')
        self.camada2 = np.load('bestobject1/camada2.npy')
        self.camada3 = np.load('bestobject1/camada3.npy')
        # print("loadcamada1")
        # print(self.camada1)
        # print("camada2")
        # print(self.camada2)
        # print("camada3")
        # print(self.camada3)
    def save(self):
        np.save('camada1', self.camada1)
        np.save('camada2', self.camada2)
        np.save('camada3', self.camada3)
        
        

    def __init__(self,nInput,camadas = np.array([5,3,4])):
        # numero de neuronio e numero de caracteristica 
        if(camadas[0] == 0):
            self.nInput = nInput
            self.camada1 = np.zeros((camadas[0],nInput +1))
            self.camada2 = np.zeros((camadas[1],camadas[0] + 1))
            self.camada3 = np.zeros((camadas[2],camadas[1] + 1))

        
        else:
            self.nInput = nInput
            # np.random.uniform(low=-1, high=1, size=(3,4))
            self.camada1 = np.random.uniform(low = -1,high = 1,size = (camadas[0],nInput +1))
            self.camada2 = np.random.uniform(low = -1,high = 1,size = (camadas[1],camadas[0] + 1))
            self.camada3 = np.random.uniform(low = -1,high = 1,size = (camadas[2],camadas[1] + 1))
        
        
#         self.camada1 = np.zeros((camadas[0],nInput +1))
#         self.camada2 = np.ones((camadas[1],camadas[0] + 1))
#         self.camada3 = np.ones((camadas[2],camadas[1] + 1))
        
        
    def sigmoid(self,x):                                        
      return 1 / (1 + np.exp(-x))
    
    
    def predict(self,X):
        b = np.append([1], X)
        # print(b)
        s0 = b.dot(self.camada1.transpose())
        s0 = self.sigmoid(s0)
        # print(s0)
        

        b = np.append([1], s0)
#         print(b)
        s1 = b.dot(self.camada2.transpose())
        s1 = self.sigmoid(s1)
        # print(s1)
        
        b = np.append([1], s1)
#         print(b)
        s2 = b.dot(self.camada3.transpose())
        
        s2 = self.sigmoid(s2)
        # print(s2)
        
        
        # print(np.argmax(s2))
        return np.argmax(s2)

