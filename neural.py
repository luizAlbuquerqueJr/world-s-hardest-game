
import numpy as np
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
        

    def __init__(self,nInput,camadas = np.array([5,3,4])):
        # numero de neuronio e numero de caracteristica 
        if(camadas[0] == 0):
            self.nInput = nInput
            self.camada1 = np.zeros((camadas[0],nInput +1))
            self.camada2 = np.zeros((camadas[1],camadas[0] + 1))
            self.camada3 = np.zeros((camadas[2],camadas[1] + 1))

        
        else:
            self.nInput = nInput
            self.camada1 = np.random.rand(camadas[0],nInput +1)
            self.camada2 = np.random.rand(camadas[1],camadas[0] + 1)
            self.camada3 = np.random.rand(camadas[2],camadas[1] + 1)
        
        
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

